"""
Weather & Meteorological Alert Service.
SSOT Reference: 02_DATA_AND_ML_SSOT.md, 03_DECISION_ENGINE_SSOT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.db.models import WeatherEventModel
from app.schemas.weather import WeatherSignal, WeatherEventDetail
from app.schemas.common import DataClassification, RiskLevel
from app.config.constants import SEEDED_RISK_OVERRIDE_SCENARIO_ENABLED


class WeatherService:
    @staticmethod
    def get_weather_signal(
        latitude: float,
        longitude: float,
        district_id: Optional[str] = None,
        state_id: Optional[str] = None,
        db: Optional[Session] = None,
        force_scenario: Optional[str] = None,
    ) -> WeatherSignal:
        """
        Retrieves weather status and alerts for the specified location.
        Supports honest classification: REAL, SEEDED, or UNAVAILABLE.
        Includes deterministic SEEDED severe risk scenario for Judge Proof.
        """
        # Force scenario override for testing/demo
        if force_scenario == "UNAVAILABLE":
            return WeatherSignal(
                status="UNAVAILABLE",
                impact_level=RiskLevel.LOW,
                events=[],
                classification=DataClassification.UNAVAILABLE,
                source_label="Weather Service Signal Unavailable / Offline",
            )

        if force_scenario == "NORMAL":
            return WeatherSignal(
                status="ACTIVE",
                impact_level=RiskLevel.LOW,
                events=[],
                classification=DataClassification.SEEDED,
                source_label="Baseline Agro-Meteorological Advisory (Normal Conditions)",
            )

        # Check for active seeded weather events in database
        if db:
            query = db.query(WeatherEventModel).filter(WeatherEventModel.active == True)
            
            # Match by district or state if provided
            if district_id:
                event = query.filter(WeatherEventModel.district_id == district_id.lower().strip()).first()
            elif state_id:
                event = query.filter(WeatherEventModel.state_id == state_id.lower().strip()).first()
            else:
                event = query.first()

            if event:
                return WeatherSignal(
                    status="ACTIVE",
                    impact_level=RiskLevel(event.severity),
                    events=[
                        WeatherEventDetail(
                            event_id=event.event_id,
                            event_type=event.event_type,
                            severity=RiskLevel(event.severity),
                            event_date=event.event_date,
                            description=f"Active alert: {event.event_type.replace('_', ' ').title()}",
                            classification=DataClassification(event.classification),
                            source_label=event.source_label,
                        )
                    ],
                    classification=DataClassification(event.classification),
                    source_label=event.source_label,
                )

        # Deterministic Pune demo seeded scenario fallback if enabled in constants
        if SEEDED_RISK_OVERRIDE_SCENARIO_ENABLED:
            # If coordinates are around Pune (lat ~18.5, lon ~73.8) or district is pune
            if (district_id and district_id.lower() == "pune") or (
                18.0 <= latitude <= 19.5 and 73.0 <= longitude <= 74.5
            ):
                return WeatherSignal(
                    status="ACTIVE",
                    impact_level=RiskLevel.HIGH,
                    events=[
                        WeatherEventDetail(
                            event_id="demo_pune_rain_event",
                            event_type="HEAVY_RAIN_AND_WATERLOGGING",
                            severity=RiskLevel.HIGH,
                            event_date="2026-08-21",
                            description="Severe waterlogging and localized flash flooding reported near transport corridors",
                            classification=DataClassification.SEEDED,
                            source_label="Deterministic seeded severe weather scenario for judge demo",
                        )
                    ],
                    classification=DataClassification.SEEDED,
                    source_label="Deterministic seeded severe weather scenario for judge demo",
                )

        # Baseline active normal condition
        return WeatherSignal(
            status="ACTIVE",
            impact_level=RiskLevel.LOW,
            events=[],
            classification=DataClassification.SEEDED,
            source_label="Baseline Agro-Meteorological Advisory (Normal Conditions)",
        )
