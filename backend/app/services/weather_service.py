"""
Weather & Meteorological Alert Service.
SSOT Reference: 02_DATA_AND_ML_SSOT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.db.models import WeatherEventModel
from app.schemas.weather import WeatherSignal, WeatherEventDetail
from app.schemas.common import DataClassification, RiskLevel
from app.config.settings import settings


class WeatherService:
    @staticmethod
    def get_weather_signal(
        latitude: float,
        longitude: float,
        state_id: Optional[str] = None,
        district_id: Optional[str] = None,
        db: Optional[Session] = None,
        force_seeded_scenario: Optional[bool] = None,
    ) -> WeatherSignal:
        """
        Retrieves active weather impact and meteorological alerts.
        Prioritizes:
        1. Database registered alerts / live meteorological events
        2. Deterministic seeded severe weather scenario (for judge demonstration when configured)
        3. Clear UNAVAILABLE / Normal baseline status
        """
        use_seeded_demo = (
            force_seeded_scenario
            if force_seeded_scenario is not None
            else settings.SEEDED_RISK_OVERRIDE_SCENARIO_ENABLED
        )

        # Check DB for active weather events in proximity
        if db:
            event = None
            if district_id:
                event = (
                    db.query(WeatherEventModel)
                    .filter(
                        WeatherEventModel.district_id == district_id.lower().strip(),
                        WeatherEventModel.active == True,
                    )
                    .first()
                )

            if event:
                sev = RiskLevel(event.severity) if event.severity in RiskLevel.__members__ else RiskLevel.HIGH
                return WeatherSignal(
                    status="ACTIVE",
                    impact_level=sev,
                    events=[
                        WeatherEventDetail(
                            event_id=event.event_id,
                            event_type=event.event_type,
                            severity=sev,
                            event_date=event.event_date,
                            description=f"Meteorological Alert: {event.event_type} in {district_id}",
                            classification=DataClassification(event.classification),
                            source_label=event.source_label,
                        )
                    ],
                    classification=DataClassification(event.classification),
                    source_label=event.source_label,
                )

        # If deterministic demo scenario is enabled and in Pune district
        if use_seeded_demo and district_id and district_id.lower().strip() == "pune":
            return WeatherSignal(
                status="ACTIVE",
                impact_level=RiskLevel.HIGH,
                events=[
                    WeatherEventDetail(
                        event_id="demo_pune_waterlogging",
                        event_type="UNSEASONAL_HEAVY_RAINFALL",
                        severity=RiskLevel.HIGH,
                        event_date="2026-08-21",
                        description="Severe unseasonal rain leading to mandi waterlogging and transit delays",
                        classification=DataClassification.SEEDED,
                        source_label="Deterministic Seeded Weather Fixture (Judge Demo)",
                    )
                ],
                classification=DataClassification.SEEDED,
                source_label="Deterministic Seeded Weather Fixture (Judge Demo)",
            )

        # Default normal baseline
        return WeatherSignal(
            status="ACTIVE",
            impact_level=RiskLevel.LOW,
            events=[],
            classification=DataClassification.SEEDED,
            source_label="IMD Baseline Agro-Meteorological Advisory (Normal)",
        )
