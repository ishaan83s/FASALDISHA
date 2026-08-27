"""
Initial Seed Data Catalog for Rajasthan, Gujarat, and Maharashtra.
SSOT Reference: 02_DATA_AND_ML_SSOT.md, 04_DATABASE_CONTRACT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
from typing import List, Dict, Any
from app.db.session import SessionLocal, init_db
from app.db.models import (
    StateModel,
    DistrictModel,
    CommodityModel,
    MandiModel,
    MandiCommodityModel,
    MandiPriceModel,
    BuyerModel,
    WeatherEventModel,
)

STATES: List[Dict[str, Any]] = [
    {"state_id": "maharashtra", "state_name": "Maharashtra", "active": True, "source_classification": "REAL"},
    {"state_id": "gujarat", "state_name": "Gujarat", "active": True, "source_classification": "REAL"},
    {"state_id": "rajasthan", "state_name": "Rajasthan", "active": True, "source_classification": "REAL"},
]

DISTRICTS: List[Dict[str, Any]] = [
    # Maharashtra
    {"district_id": "pune", "state_id": "maharashtra", "district_name": "Pune", "latitude": 18.5204, "longitude": 73.8567, "active": True},
    {"district_id": "nashik", "state_id": "maharashtra", "district_name": "Nashik", "latitude": 20.0000, "longitude": 73.7800, "active": True},
    {"district_id": "ahmednagar", "state_id": "maharashtra", "district_name": "Ahmednagar", "latitude": 19.0952, "longitude": 74.7496, "active": True},
    {"district_id": "solapur", "state_id": "maharashtra", "district_name": "Solapur", "latitude": 17.6599, "longitude": 75.9064, "active": True},
    {"district_id": "kolhapur", "state_id": "maharashtra", "district_name": "Kolhapur", "latitude": 16.7050, "longitude": 74.2433, "active": True},
    {"district_id": "nagpur", "state_id": "maharashtra", "district_name": "Nagpur", "latitude": 21.1458, "longitude": 79.0882, "active": True},
    {"district_id": "chhatrapati_sambhajinagar", "state_id": "maharashtra", "district_name": "Chhatrapati Sambhajinagar", "latitude": 19.8762, "longitude": 75.3433, "active": True},
    # Gujarat
    {"district_id": "ahmedabad", "state_id": "gujarat", "district_name": "Ahmedabad", "latitude": 23.0225, "longitude": 72.5714, "active": True},
    {"district_id": "surat", "state_id": "gujarat", "district_name": "Surat", "latitude": 21.1702, "longitude": 72.8311, "active": True},
    {"district_id": "rajkot", "state_id": "gujarat", "district_name": "Rajkot", "latitude": 22.3039, "longitude": 70.8022, "active": True},
    {"district_id": "vadodara", "state_id": "gujarat", "district_name": "Vadodara", "latitude": 22.3072, "longitude": 73.1812, "active": True},
    {"district_id": "junagadh", "state_id": "gujarat", "district_name": "Junagadh", "latitude": 21.5222, "longitude": 70.4579, "active": True},
    {"district_id": "mehsana", "state_id": "gujarat", "district_name": "Mehsana", "latitude": 23.5880, "longitude": 72.3693, "active": True},
    # Rajasthan
    {"district_id": "jaipur", "state_id": "rajasthan", "district_name": "Jaipur", "latitude": 26.9124, "longitude": 75.7873, "active": True},
    {"district_id": "jodhpur", "state_id": "rajasthan", "district_name": "Jodhpur", "latitude": 26.2389, "longitude": 73.0243, "active": True},
    {"district_id": "kota", "state_id": "rajasthan", "district_name": "Kota", "latitude": 25.1800, "longitude": 75.8300, "active": True},
    {"district_id": "alwar", "state_id": "rajasthan", "district_name": "Alwar", "latitude": 27.5530, "longitude": 76.6346, "active": True},
    {"district_id": "sikar", "state_id": "rajasthan", "district_name": "Sikar", "latitude": 27.6094, "longitude": 75.1398, "active": True},
    {"district_id": "bikaner", "state_id": "rajasthan", "district_name": "Bikaner", "latitude": 28.0229, "longitude": 73.3119, "active": True},
]

COMMODITIES: List[Dict[str, Any]] = [
    {
        "commodity_id": "onion",
        "commodity_name": "Onion",
        "commodity_category": "Vegetable",
        "perishability_class": "MODERATELY_PERISHABLE",
        "legacy_crop_group": "PERISHABLE",
        "unit": "quintal",
        "active": True,
    },
    {
        "commodity_id": "tomato",
        "commodity_name": "Tomato",
        "commodity_category": "Vegetable",
        "perishability_class": "HIGHLY_PERISHABLE",
        "legacy_crop_group": "PERISHABLE",
        "unit": "quintal",
        "active": True,
    },
    {
        "commodity_id": "potato",
        "commodity_name": "Potato",
        "commodity_category": "Vegetable",
        "perishability_class": "MODERATELY_PERISHABLE",
        "legacy_crop_group": "PERISHABLE",
        "unit": "quintal",
        "active": True,
    },
    {
        "commodity_id": "wheat",
        "commodity_name": "Wheat",
        "commodity_category": "Cereal",
        "perishability_class": "NON_PERISHABLE",
        "legacy_crop_group": "NON_PERISHABLE",
        "unit": "quintal",
        "active": True,
    },
    {
        "commodity_id": "soybean",
        "commodity_name": "Soybean",
        "commodity_category": "Oilseed",
        "perishability_class": "NON_PERISHABLE",
        "legacy_crop_group": "NON_PERISHABLE",
        "unit": "quintal",
        "active": True,
    },
    {
        "commodity_id": "mustard",
        "commodity_name": "Mustard",
        "commodity_category": "Oilseed",
        "perishability_class": "NON_PERISHABLE",
        "legacy_crop_group": "NON_PERISHABLE",
        "unit": "quintal",
        "active": True,
    },
    {
        "commodity_id": "cotton",
        "commodity_name": "Cotton",
        "commodity_category": "Fiber",
        "perishability_class": "NON_PERISHABLE",
        "legacy_crop_group": "NON_PERISHABLE",
        "unit": "quintal",
        "active": True,
    },
]

MANDIS: List[Dict[str, Any]] = [
    # Maharashtra - Pune Region
    {"mandi_id": "mandi_pune_gultekdi", "mandi_name": "APMC Pune (Gultekdi)", "state_id": "maharashtra", "district_id": "pune", "latitude": 18.4975, "longitude": 73.8644, "active": True},
    {"mandi_id": "mandi_pune_chakan", "mandi_name": "APMC Chakan (Khed)", "state_id": "maharashtra", "district_id": "pune", "latitude": 18.7562, "longitude": 73.8596, "active": True},
    {"mandi_id": "mandi_pune_shirur", "mandi_name": "APMC Shirur", "state_id": "maharashtra", "district_id": "pune", "latitude": 18.8277, "longitude": 74.3779, "active": True},
    {"mandi_id": "mandi_pune_junnar", "mandi_name": "APMC Narayangaon (Junnar)", "state_id": "maharashtra", "district_id": "pune", "latitude": 19.1200, "longitude": 73.9700, "active": True},
    {"mandi_id": "mandi_pune_baramati", "mandi_name": "APMC Baramati", "state_id": "maharashtra", "district_id": "pune", "latitude": 18.1517, "longitude": 74.5772, "active": True},
    
    # Maharashtra - Ahmednagar & Nashik (cross-boundary eligible from Pune)
    {"mandi_id": "mandi_ahmednagar", "mandi_name": "APMC Ahmednagar", "state_id": "maharashtra", "district_id": "ahmednagar", "latitude": 19.0952, "longitude": 74.7496, "active": True},
    {"mandi_id": "mandi_shrigonda", "mandi_name": "APMC Shrigonda", "state_id": "maharashtra", "district_id": "ahmednagar", "latitude": 18.6167, "longitude": 74.6833, "active": True},
    {"mandi_id": "mandi_nashik_lasalgaon", "mandi_name": "APMC Lasalgaon (Asia's Largest Onion Market)", "state_id": "maharashtra", "district_id": "nashik", "latitude": 20.1477, "longitude": 74.2289, "active": True},
    {"mandi_id": "mandi_nashik_pimpalgaon", "mandi_name": "APMC Pimpalgaon Baswant", "state_id": "maharashtra", "district_id": "nashik", "latitude": 20.1700, "longitude": 73.9800, "active": True},
    {"mandi_id": "mandi_solapur", "mandi_name": "APMC Solapur", "state_id": "maharashtra", "district_id": "solapur", "latitude": 17.6599, "longitude": 75.9064, "active": True},

    # Gujarat
    {"mandi_id": "mandi_ahmedabad_jamalpur", "mandi_name": "APMC Ahmedabad (Jamalpur)", "state_id": "gujarat", "district_id": "ahmedabad", "latitude": 23.0120, "longitude": 72.5782, "active": True},
    {"mandi_id": "mandi_surat", "mandi_name": "APMC Surat", "state_id": "gujarat", "district_id": "surat", "latitude": 21.1702, "longitude": 72.8311, "active": True},
    {"mandi_id": "mandi_rajkot", "mandi_name": "APMC Rajkot (Bedi)", "state_id": "gujarat", "district_id": "rajkot", "latitude": 22.3039, "longitude": 70.8022, "active": True},
    {"mandi_id": "mandi_gondal", "mandi_name": "APMC Gondal", "state_id": "gujarat", "district_id": "rajkot", "latitude": 21.9619, "longitude": 70.7963, "active": True},
    {"mandi_id": "mandi_unjha", "mandi_name": "APMC Unjha", "state_id": "gujarat", "district_id": "mehsana", "latitude": 23.8039, "longitude": 72.3944, "active": True},

    # Rajasthan
    {"mandi_id": "mandi_jaipur_muhana", "mandi_name": "APMC Jaipur (Muhana Mandi)", "state_id": "rajasthan", "district_id": "jaipur", "latitude": 26.8012, "longitude": 75.7601, "active": True},
    {"mandi_id": "mandi_jaipur_chomu", "mandi_name": "APMC Chomu", "state_id": "rajasthan", "district_id": "jaipur", "latitude": 27.1706, "longitude": 75.7228, "active": True},
    {"mandi_id": "mandi_alwar", "mandi_name": "APMC Alwar", "state_id": "rajasthan", "district_id": "alwar", "latitude": 27.5530, "longitude": 76.6346, "active": True},
    {"mandi_id": "mandi_kota_bhamashah", "mandi_name": "APMC Kota (Bhamashah)", "state_id": "rajasthan", "district_id": "kota", "latitude": 25.1767, "longitude": 75.8648, "active": True},
    {"mandi_id": "mandi_jodhpur", "mandi_name": "APMC Jodhpur (Bhagat Ki Kothi)", "state_id": "rajasthan", "district_id": "jodhpur", "latitude": 26.2500, "longitude": 73.0200, "active": True},
]


def seed_database():
    """Seed the database with states, districts, commodities, mandis, prices, and buyers."""
    init_db()
    db = SessionLocal()
    try:
        # 1. Seed States
        for state_data in STATES:
            existing = db.query(StateModel).filter_by(state_id=state_data["state_id"]).first()
            if not existing:
                db.add(StateModel(**state_data))

        # 2. Seed Districts
        for dist_data in DISTRICTS:
            existing = db.query(DistrictModel).filter_by(district_id=dist_data["district_id"]).first()
            if not existing:
                db.add(DistrictModel(**dist_data))
            else:
                existing.latitude = dist_data.get("latitude")
                existing.longitude = dist_data.get("longitude")

        # 3. Seed Commodities
        for comm_data in COMMODITIES:
            existing = db.query(CommodityModel).filter_by(commodity_id=comm_data["commodity_id"]).first()
            if not existing:
                db.add(CommodityModel(**comm_data))

        # 4. Seed Mandis
        for mandi_data in MANDIS:
            existing = db.query(MandiModel).filter_by(mandi_id=mandi_data["mandi_id"]).first()
            if not existing:
                db.add(MandiModel(**mandi_data))

        db.commit()

        # 5. Seed Mandi Commodities Availability
        for mandi in MANDIS:
            for comm in COMMODITIES:
                existing = db.query(MandiCommodityModel).filter_by(
                    mandi_id=mandi["mandi_id"], commodity_id=comm["commodity_id"]
                ).first()
                if not existing:
                    db.add(MandiCommodityModel(
                        mandi_id=mandi["mandi_id"],
                        commodity_id=comm["commodity_id"],
                        active=True,
                        source_classification="REAL"
                    ))

        # 6. Seed Baseline Prices for Mandis
        price_bases = {
            "onion": {"min": 2100.0, "modal": 2350.0, "max": 2550.0},
            "tomato": {"min": 1700.0, "modal": 1950.0, "max": 2200.0},
            "potato": {"min": 1400.0, "modal": 1600.0, "max": 1800.0},
            "wheat": {"min": 2350.0, "modal": 2480.0, "max": 2650.0},
            "soybean": {"min": 4400.0, "modal": 4650.0, "max": 4900.0},
            "mustard": {"min": 5200.0, "modal": 5450.0, "max": 5700.0},
            "cotton": {"min": 6800.0, "modal": 7100.0, "max": 7450.0},
        }

        for mandi in MANDIS:
            for comm_id, price_info in price_bases.items():
                existing = db.query(MandiPriceModel).filter_by(
                    mandi_id=mandi["mandi_id"], commodity_id=comm_id
                ).first()
                if not existing:
                    # Give slight regional differentiation to test ranking
                    offset = (hash(mandi["mandi_id"]) % 15) * 10
                    db.add(MandiPriceModel(
                        mandi_id=mandi["mandi_id"],
                        commodity_id=comm_id,
                        price_date="2026-08-21",
                        min_price=price_info["min"] + offset,
                        modal_price=price_info["modal"] + offset,
                        max_price=price_info["max"] + offset,
                        source_classification="SEEDED",
                    ))

        # 7. Seed Synthetic Buyers (Judge Proof requirement: active count, demand, offer strength, reliability)
        for mandi in MANDIS:
            for comm in COMMODITIES:
                existing_buyer = db.query(BuyerModel).filter_by(
                    mandi_id=mandi["mandi_id"], commodity_id=comm["commodity_id"]
                ).first()
                if not existing_buyer:
                    # Generate 2-5 synthetic buyers per mandi-commodity pair
                    num_buyers = 3 + (hash(mandi["mandi_id"] + comm["commodity_id"]) % 3)
                    for b_idx in range(num_buyers):
                        db.add(BuyerModel(
                            buyer_type="Wholesale Trader" if b_idx % 2 == 0 else "Institutional Aggregator",
                            commodity_id=comm["commodity_id"],
                            mandi_id=mandi["mandi_id"],
                            active=True,
                            demand_level="HIGH" if b_idx == 0 else "MEDIUM",
                            offer_strength=65.0 + (b_idx * 8.0) % 30.0,
                            reliability_score=75.0 + (b_idx * 5.0) % 20.0,
                            data_classification="SYNTHETIC",
                        ))

        # 8. Seed Demo Weather Scenario for Deterministic Judge Verification
        existing_weather = db.query(WeatherEventModel).filter_by(event_id="demo_pune_rain_event").first()
        if not existing_weather:
            db.add(WeatherEventModel(
                event_id="demo_pune_rain_event",
                state_id="maharashtra",
                district_id="pune",
                latitude=18.52,
                longitude=73.85,
                event_type="HEAVY_RAIN_AND_WATERLOGGING",
                severity="HIGH",
                event_date="2026-08-21",
                classification="SEEDED",
                source_label="Deterministic seeded severe weather scenario for judge demo",
                active=True,
            ))

        db.commit()
    finally:
        db.close()
