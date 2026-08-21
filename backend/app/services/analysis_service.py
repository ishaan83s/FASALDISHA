"""
Analysis Orchestrator Service: Top-level composer for FasalDisha.
SSOT Reference: 01_SYSTEM_ARCHITECTURE.md, 03_DECISION_ENGINE_SSOT.md, 05_API_CONTRACT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisResult,
    FarmerContext,
    SearchMetadata,
    CandidateMandi,
    RiskSummary,
    DataProvenance,
)
from app.schemas.geography import Commodity, Mandi
from app.schemas.common import DataClassification, RiskLevel
from app.services.geography_service import GeographyService
from app.services.mandi_service import MandiService
from app.services.forecast_service import ForecastService
from app.services.weather_service import WeatherService
from app.services.buyer_service import BuyerService
from app.services.transport_service import TransportService
from app.services.risk_service import RiskService
from app.services.ranking_service import RankingService
from app.services.decision_engine import DecisionEngine


class AnalysisService:
    @staticmethod
    def run_analysis(request: AnalysisRequest, db: Session) -> AnalysisResult:
        """
        Executes end-to-end analysis:
        1. Resolve commodity metadata
        2. Find nearby commodity-eligible mandis (coordinate-based, cross-boundary)
        3. Retrieve baseline prices, forecasts, transport, buyer signals, and risks
        4. Rank mandis
        5. Evaluate base decision and risk overrides
        6. Assemble and return AnalysisResult
        """
        # 1. Commodity Metadata
        commodity = GeographyService.get_commodity_by_id(request.commodity_id, db)
        if not commodity:
            raise ValueError(f"Commodity '{request.commodity_id}' not found in catalog")

        farmer_context = FarmerContext(
            state_id=request.state_id,
            district_id=request.district_id,
            latitude=request.latitude,
            longitude=request.longitude,
            quantity_quintals=request.quantity_quintals,
            radius_km=request.radius_km,
        )

        # 2. Weather Signal for Farmer Location
        weather = WeatherService.get_weather_signal(
            latitude=request.latitude,
            longitude=request.longitude,
            district_id=request.district_id,
            state_id=request.state_id,
            db=db,
        )

        # 3. Discover Nearby Mandis (within radius)
        nearby_raw = MandiService.find_nearby_mandis(
            latitude=request.latitude,
            longitude=request.longitude,
            commodity_id=request.commodity_id,
            radius_km=request.radius_km,
            db=db,
        )

        # Check local mandi (closest in farmer district or closest overall)
        local_raw = MandiService.find_local_mandi(
            latitude=request.latitude,
            longitude=request.longitude,
            district_id=request.district_id,
            commodity_id=request.commodity_id,
            db=db,
        )
        local_mandi = MandiService.to_schema(local_raw[0]) if local_raw else None

        # Check if cross-boundary candidates are present
        cross_boundary = any(
            m.district_id != request.district_id.lower().strip() or m.state_id != request.state_id.lower().strip()
            for m, _ in nearby_raw
        )

        # 4. Generate Top-level Commodity Forecast
        top_level_forecast = ForecastService.get_forecast_for_mandi(
            commodity_id=request.commodity_id,
            mandi_id=local_mandi.mandi_id if local_mandi else None,
            db=db,
        )

        # 5. Process Candidates
        candidates: List[CandidateMandi] = []
        for m_model, dist_km in nearby_raw:
            mandi_schema = MandiService.to_schema(m_model)

            # Forecast for this specific mandi
            mandi_forecast = ForecastService.get_forecast_for_mandi(
                commodity_id=request.commodity_id,
                mandi_id=m_model.mandi_id,
                db=db,
            )

            # Transport calculation
            cost_per_q, total_transport = TransportService.calculate_transport(
                distance_km=dist_km,
                quantity_quintals=request.quantity_quintals,
                custom_rate_per_quintal_per_km=request.transport_rate_per_quintal_per_km,
            )

            # Economics (7-day forecast price)
            expected_price = mandi_forecast.forecast_7_day
            expected_revenue = round(expected_price * request.quantity_quintals, 2)
            net_return = round(expected_revenue - total_transport, 2)

            # Synthetic Buyer Signal
            buyer_signal = BuyerService.get_buyer_signal(
                mandi_id=m_model.mandi_id,
                commodity_id=request.commodity_id,
                db=db,
            )

            # Weather & Risk
            mandi_weather = WeatherService.get_weather_signal(
                latitude=m_model.latitude,
                longitude=m_model.longitude,
                district_id=m_model.district_id,
                state_id=m_model.state_id,
                db=db,
            )

            risk_score, risk_level, _ = RiskService.calculate_mandi_risk(
                commodity=commodity,
                weather=mandi_weather,
                distance_km=dist_km,
                forecast=mandi_forecast,
                db=db,
            )

            risk_adjusted_return = RiskService.calculate_risk_adjusted_return(
                net_return=net_return,
                risk_score=risk_score,
            )

            candidate = CandidateMandi(
                rank=1,  # will be assigned by ranking service
                mandi=mandi_schema,
                distance_km=dist_km,
                commodity_available=True,
                current_price=mandi_forecast.current_price,
                forecast=mandi_forecast,
                transport_cost_per_quintal=cost_per_q,
                total_transport_cost=total_transport,
                expected_revenue=expected_revenue,
                net_return=net_return,
                risk_score=risk_score,
                risk_level=risk_level,
                risk_adjusted_return=risk_adjusted_return,
                buyer_signal=buyer_signal,
                weather_impact=mandi_weather,
                ranking_breakdown=None,  # type: ignore
                ranking_score=0.0,
                data_classification={
                    "price": "SEEDED",
                    "forecast": mandi_forecast.model_type.value,
                    "buyers": "SYNTHETIC",
                    "weather": mandi_weather.classification.value,
                },
            )
            candidates.append(candidate)

        # 6. Rank Candidates
        ranked_mandis = RankingService.rank_candidates(candidates)

        # 7. Evaluate Decision & Risk Override
        decision = DecisionEngine.evaluate_decision(
            commodity=commodity,
            farmer_context=farmer_context,
            local_mandi=local_mandi,
            ranked_mandis=ranked_mandis,
            general_forecast=top_level_forecast,
            general_weather=weather,
        )

        # 8. Overall Risk Summary
        if ranked_mandis:
            avg_risk = sum(c.risk_score for c in ranked_mandis) / float(len(ranked_mandis))
        else:
            avg_risk = 20.0
        avg_risk = round(avg_risk, 1)
        risk_lvl = (
            RiskLevel.LOW if avg_risk <= 25.0
            else RiskLevel.MODERATE if avg_risk <= 50.0
            else RiskLevel.HIGH if avg_risk <= 75.0
            else RiskLevel.CRITICAL
        )

        risk_summary = RiskSummary(
            overall_risk_score=avg_risk,
            risk_level=risk_lvl,
            data_completeness=1.0,
            risk_factors=[e.description for e in weather.events if e.description],
        )

        search_metadata = SearchMetadata(
            candidate_count=len(ranked_mandis),
            search_status="OK" if ranked_mandis else "NO_ELIGIBLE_MANDI_IN_RADIUS",
            cross_boundary_candidates_included=cross_boundary,
        )

        data_provenance = DataProvenance(
            coverage={
                "states": ["Rajasthan", "Gujarat", "Maharashtra"],
                "activeCatalogStatus": "Representative Seeded APMC Catalog",
            },
            buyer_data_classification=DataClassification.SYNTHETIC,
        )

        return AnalysisResult(
            commodity=commodity,
            farmer_context=farmer_context,
            search=search_metadata,
            local_mandi=local_mandi,
            forecast=top_level_forecast,
            weather=weather,
            risk_summary=risk_summary,
            nearby_mandis=ranked_mandis,
            data_provenance=data_provenance,
            decision=decision,
        )
