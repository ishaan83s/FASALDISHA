"""
Top-Level Analysis Orchestrator Service.
SSOT Reference: 01_SYSTEM_ARCHITECTURE.md, 03_DECISION_ENGINE_SSOT.md, 05_API_CONTRACT.md
"""
from typing import Optional, List, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisResult,
    FarmerContext,
    SearchMetadata,
    DataProvenance,
    CandidateMandi,
)
from app.schemas.common import DataClassification
from app.services.geography_service import GeographyService
from app.services.mandi_service import MandiService, haversine_distance
from app.services.market_data_service import MarketDataService
from app.services.forecast_service import ForecastService
from app.services.transport_service import TransportService
from app.services.weather_service import WeatherService
from app.services.buyer_service import BuyerService
from app.services.risk_service import RiskService
from app.services.ranking_service import RankingService
from app.services.decision_engine import DecisionEngine


class AnalysisService:
    @staticmethod
    def run_analysis(request: AnalysisRequest, db: Session) -> AnalysisResult:
        """
        End-to-End Analysis Pipeline:
        1. Validate & Canonicalize Location Context (Guards against contradictory coordinates/districts)
        2. Resolve Commodity Metadata
        3. Dynamic Coordinate-based Nearby Mandi Discovery (Cross-Boundary)
        4. Market Price, Forecast, Transport & Synthetic Buyer Aggregation
        5. Unified Weather, Perishability & Route Risk Calculation
        6. Quantity-aware Comparative Economics & Transparent Multi-Factor Ranking
        7. Explainable Decision Engine with Deterministic Risk Override Capability
        8. Returns Frozen AnalysisResult Contract
        """
        # Step 1: Validate Geographic Context & Consistency against Geography Catalog
        district = GeographyService.get_district_by_id(request.district_id, db)
        if not district:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid district '{request.district_id}'. Please select a supported district from the geography catalog.",
            )

        if district.state_id != request.state_id.lower().strip():
            raise HTTPException(
                status_code=422,
                detail=f"District '{district.district_name}' belongs to state '{district.state_id}', not '{request.state_id}'.",
            )

        # Resolve submitted coordinates against the single authoritative geography catalog
        resolved_loc = GeographyService.resolve_location(request.latitude, request.longitude, db)
        if not resolved_loc.in_supported_region or resolved_loc.resolution_status != "RESOLVED":
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Geographic coordinates ({request.latitude:.4f}°N, {request.longitude:.4f}°E) fall outside "
                    f"supported coverage regions (Maharashtra, Gujarat, Rajasthan) and cannot be associated with district '{district.district_name}'."
                ),
            )

        if (
            resolved_loc.state_id != request.state_id.lower().strip()
            or resolved_loc.district_id != request.district_id.lower().strip()
        ):
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Location consistency error: Submitted coordinates ({request.latitude:.4f}°N, {request.longitude:.4f}°E) "
                    f"resolve to district '{resolved_loc.district_name}' ({resolved_loc.state_name}), "
                    f"which does not match declared district '{district.district_name}' ({district.state_id.capitalize()})."
                ),
            )

        # Step 2: Resolve Commodity Metadata
        commodity = GeographyService.get_commodity_by_id(request.commodity_id, db)
        if not commodity:
            # Fallback commodity metadata if not in DB yet
            from app.schemas.common import PerishabilityClass, CropGroup
            commodity = GeographyService.get_commodities(db=db)[0] if GeographyService.get_commodities(db=db) else None
            if not commodity:
                from app.schemas.geography import Commodity
                commodity = Commodity(
                    commodity_id=request.commodity_id,
                    commodity_name=request.commodity_id.capitalize(),
                    commodity_category="Agriculture",
                    perishability_class=PerishabilityClass.MODERATELY_PERISHABLE,
                    crop_group=CropGroup.PERISHABLE,
                    unit="quintal",
                    active=True,
                )

        # Step 2: Discover Eligible Nearby Mandis within radius (authoritative coordinate search)
        nearby_matches = MandiService.find_nearby_mandis(
            latitude=request.latitude,
            longitude=request.longitude,
            commodity_id=request.commodity_id,
            radius_km=request.radius_km,
            db=db,
        )

        cross_boundary = any(
            (m.district_id != request.district_id.lower().strip() or m.state_id != request.state_id.lower().strip())
            for m, _ in nearby_matches
        )

        search_meta = SearchMetadata(
            candidate_count=len(nearby_matches),
            search_status="OK" if nearby_matches else "NO_ELIGIBLE_MANDI_IN_RADIUS",
            cross_boundary_candidates_included=cross_boundary,
        )

        # Farmer context
        farmer_context = FarmerContext(
            state_id=request.state_id,
            district_id=request.district_id,
            latitude=request.latitude,
            longitude=request.longitude,
            quantity_quintals=request.quantity_quintals,
            radius_km=request.radius_km,
        )

        # Step 3: Farmer Origin Weather & Risk Summary
        origin_weather = WeatherService.get_weather_signal(
            latitude=request.latitude,
            longitude=request.longitude,
            state_id=request.state_id,
            district_id=request.district_id,
            db=db,
        )

        # Gather per-mandi raw candidates
        raw_candidates: List[Dict[str, Any]] = []
        for mandi_model, dist_km in nearby_matches:
            mandi_schema = MandiService.to_schema(mandi_model)
            current_price, price_class = MarketDataService.get_latest_price(
                mandi_id=mandi_model.mandi_id,
                commodity_id=request.commodity_id,
                db=db,
            )
            forecast = ForecastService.get_forecast(
                commodity_id=request.commodity_id,
                mandi_id=mandi_model.mandi_id,
                current_price_override=current_price,
            )
            transport_per_q, total_transport = TransportService.calculate_transport(
                distance_km=dist_km,
                quantity_quintals=request.quantity_quintals,
                custom_rate=request.transport_rate_per_quintal_per_km,
            )
            buyer_sig = BuyerService.get_buyer_signal(
                mandi_id=mandi_model.mandi_id,
                commodity_id=request.commodity_id,
                db=db,
            )
            mandi_weather = WeatherService.get_weather_signal(
                latitude=mandi_model.latitude,
                longitude=mandi_model.longitude,
                state_id=mandi_model.state_id,
                district_id=mandi_model.district_id,
                db=db,
            )
            risk_score, risk_lvl, _ = RiskService.calculate_mandi_risk(
                weather_signal=mandi_weather,
                distance_km=dist_km,
                perishability_class=commodity.perishability_class,
                forecast_confidence=forecast.forecast_confidence,
                forecast=forecast,
            )

            raw_candidates.append({
                "mandi": mandi_schema,
                "distance_km": dist_km,
                "current_price": current_price,
                "forecast": forecast,
                "transport_cost_per_quintal": transport_per_q,
                "total_transport_cost": total_transport,
                "buyer_signal": buyer_sig,
                "weather_impact": mandi_weather,
                "risk_score": risk_score,
                "risk_level": risk_lvl,
            })

        # Step 4: Process Economics & Multi-Criteria Ranking
        ranked_candis = RankingService.process_and_rank_candidates(
            raw_candidates=raw_candidates,
            quantity_quintals=request.quantity_quintals,
        )

        # Step 5: Resolve Local Mandi
        local_mandi_schema = None
        local_candidate = None
        if nearby_matches:
            # find candidate with lowest distance
            closest = min(ranked_candis, key=lambda c: c.distance_km) if ranked_candis else None
            if closest:
                local_mandi_schema = closest.mandi
                local_candidate = closest

        # Primary forecast to expose at top-level
        top_forecast = (
            ranked_candis[0].forecast
            if ranked_candis
            else ForecastService.get_forecast(request.commodity_id)
        )

        # Step 6: Origin Risk Summary
        risk_summary = RiskService.build_risk_summary(
            weather_signal=origin_weather,
            perishability_class=commodity.perishability_class,
            forecast_confidence=top_forecast.forecast_confidence,
            forecast=top_forecast,
        )

        # Step 7: Evaluate Explainable Decision
        decision_out = DecisionEngine.evaluate_decision(
            commodity=commodity,
            local_mandi=local_candidate,
            ranked_candidates=ranked_candis,
            risk_summary=risk_summary,
        )

        # Step 8: Assemble Provenance Metadata
        provenance = DataProvenance(
            coverage={
                "supportedStates": ["Rajasthan", "Gujarat", "Maharashtra"],
                "activeCommodity": commodity.commodity_name,
                "radiusKm": request.radius_km,
                "candidatesFound": len(ranked_candis),
            },
            buyer_data_classification=DataClassification.SYNTHETIC,
        )

        return AnalysisResult(
            commodity=commodity,
            farmer_context=farmer_context,
            search=search_meta,
            local_mandi=local_mandi_schema,
            forecast=top_forecast,
            weather=origin_weather,
            risk_summary=risk_summary,
            nearby_mandis=ranked_candis,
            data_provenance=provenance,
            decision=decision_out,
        )
