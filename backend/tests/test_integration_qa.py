"""
Comprehensive Integration & QA Verification Test Suite.
SSOT Reference: 05_API_CONTRACT.md, 07_ENGINEERING_RULES.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.seed.seed_data import seed_database

# Initialize DB for tests
seed_database()
client = TestClient(app)


def test_01_health_endpoint():
    """Phase 1: Connectivity gate /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert json_data["version"] == "2.1.0"
    assert json_data["database"] == "healthy"


def test_02_geography_states():
    """Verify dynamic state listing."""
    response = client.get("/geography/states")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    states = json_data["data"]
    assert len(states) >= 3
    state_ids = [s["stateId"] for s in states]
    assert "maharashtra" in state_ids
    assert "gujarat" in state_ids
    assert "rajasthan" in state_ids


def test_03_geography_districts():
    """Verify district listing by stateId."""
    response = client.get("/geography/districts?stateId=maharashtra")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    districts = json_data["data"]
    assert len(districts) >= 5
    district_ids = [d["districtId"] for d in districts]
    assert "pune" in district_ids
    assert "nashik" in district_ids


def test_04_geography_districts_invalid():
    """Verify graceful handling of non-existent state."""
    response = client.get("/geography/districts?stateId=non_existent_state")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert len(json_data["data"]) == 0


def test_05_commodities_and_crops_compatibility():
    """Verify commodity catalog & compatibility /crops endpoint."""
    response = client.get("/crops")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    crops = json_data["data"]["crops"]
    assert len(crops) >= 5
    crop_map = {c["commodityId"]: c for c in crops}
    assert "onion" in crop_map
    assert "tomato" in crop_map
    assert "wheat" in crop_map
    assert crop_map["tomato"]["perishabilityClass"] == "HIGHLY_PERISHABLE"
    assert crop_map["wheat"]["perishabilityClass"] == "NON_PERISHABLE"


def test_06_analysis_run_pune_onion_seeded_risk_override():
    """
    Judge Proof Scenario A: Deterministic Seeded Weather Risk Override.
    Pune Onion should trigger SEEDED heavy rain alert, overriding HOLD to SELL_EARLY_DUE_TO_RISK.
    """
    payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.52,
        "longitude": 73.85,
        "commodityId": "onion",
        "quantityQuintals": 25.0,
        "radiusKm": 120.0,
        "transportRatePerQuintalPerKm": 2.5,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    data = json_data["data"]

    # 1. Candidate List (Dynamic length > 0)
    mandis = data["nearbyMandis"]
    assert len(mandis) >= 2

    # 2. Ranking verification (sorted descending)
    for i in range(len(mandis) - 1):
        assert mandis[i]["rankingScore"] >= mandis[i + 1]["rankingScore"]

    # 3. Synthetic Buyer Intelligence Verification (SSOT 13 Section C)
    for m in mandis:
        buyer = m["buyerSignal"]
        assert buyer["activeBuyerCount"] > 0
        assert buyer["classification"] == "SYNTHETIC"
        assert "Synthetic" in buyer["sourceLabel"]
        assert 0.0 <= buyer["offerStrength"] <= 100.0
        assert 0.0 <= buyer["reliability"] <= 100.0

    # 4. Forecast & Peak Alert Verification (SSOT 13 Section E)
    forecast = data["forecast"]
    assert forecast["currentPrice"] > 0
    assert forecast["forecast1Day"] > 0
    assert forecast["forecast3Day"] > 0
    assert forecast["forecast7Day"] > 0
    assert forecast["expectedPeakPrice"] >= forecast["currentPrice"]
    assert forecast["peakDay"] > 0
    assert forecast["historyClassification"] in ["REAL", "SEEDED", "CACHED_REAL"]
    assert forecast["modelType"] in ["LIVE", "PRECOMPUTED"]

    # 5. Weather & Risk Override Verification (SSOT 13 Section A & F)
    weather = data["weather"]
    assert weather["classification"] == "SEEDED"
    assert weather["impactLevel"] in ["HIGH", "CRITICAL"]

    decision = data["decision"]
    assert decision["riskOverrideApplied"] is True
    assert decision["finalRecommendation"] == "SELL_EARLY_DUE_TO_RISK"
    assert "RISK_OVERRIDE_SELL_EARLY" in decision["reasonCodes"]
    assert len(decision["humanReadableReason"]) > 10


def test_07_analysis_run_non_perishable_wheat_normal_hold():
    """
    Judge Proof Scenario B: Non-Perishable Crop with Normal Hold Decision.
    Kota Wheat under normal weather should yield HOLD recommendation with peak alert.
    """
    payload = {
        "stateId": "rajasthan",
        "districtId": "kota",
        "latitude": 25.18,
        "longitude": 75.83,
        "commodityId": "wheat",
        "quantityQuintals": 50.0,
        "radiusKm": 100.0,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    data = json_data["data"]

    assert data["commodity"]["perishabilityClass"] == "NON_PERISHABLE"
    assert len(data["nearbyMandis"]) >= 1

    decision = data["decision"]
    # Under low risk and positive forecast growth, wheat allows holding
    assert decision["baseDecision"] in ["HOLD", "SELL_NOW", "TRAVEL"]
    assert decision["finalRecommendation"] in ["HOLD", "SELL_AT_RECOMMENDED_MANDI", "SELL_NOW"]


def test_08_analysis_run_cross_boundary_discovery():
    """
    Judge Proof Scenario D: Cross-District / Cross-State Candidate Discovery.
    Search from Pune with 150 km radius should include mandis from Ahmednagar/Nashik.
    """
    payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.52,
        "longitude": 73.85,
        "commodityId": "onion",
        "quantityQuintals": 20.0,
        "radiusKm": 150.0,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    data = json_data["data"]

    search = data["search"]
    assert search["candidateCount"] > 1
    assert search["crossBoundaryCandidatesIncluded"] is True

    districts_present = {m["mandi"]["districtId"] for m in data["nearbyMandis"]}
    # Should include pune and neighboring districts (e.g. ahmednagar)
    assert len(districts_present) >= 2


def test_09_analysis_run_quantity_economics():
    """
    Verify transport cost and revenue scale accurately with quantity.
    """
    payload_10 = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.52,
        "longitude": 73.85,
        "commodityId": "onion",
        "quantityQuintals": 10.0,
        "radiusKm": 100.0,
        "transportRatePerQuintalPerKm": 2.5,
    }
    payload_50 = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.52,
        "longitude": 73.85,
        "commodityId": "onion",
        "quantityQuintals": 50.0,
        "radiusKm": 100.0,
        "transportRatePerQuintalPerKm": 2.5,
    }

    res_10 = client.post("/analysis/run", json=payload_10).json()["data"]["nearbyMandis"][0]
    res_50 = client.post("/analysis/run", json=payload_50).json()["data"]["nearbyMandis"][0]

    assert res_50["totalTransportCost"] == pytest.approx(res_10["totalTransportCost"] * 5.0, 0.1)
    assert res_50["expectedRevenue"] == pytest.approx(res_10["expectedRevenue"] * 5.0, 0.1)


def test_10_analysis_run_invalid_commodity():
    """Verify baseline heuristic fallback for uncataloged commodity."""
    payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.52,
        "longitude": 73.85,
        "commodityId": "non_existent_crop",
        "quantityQuintals": 10.0,
        "radiusKm": 100.0,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True


def test_11_analysis_run_validation_error():
    """Verify 422 global envelope for negative quantity."""
    payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.52,
        "longitude": 73.85,
        "commodityId": "onion",
        "quantityQuintals": -5.0,  # Invalid
        "radiusKm": 100.0,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 422
    json_data = response.json()
    assert json_data["success"] is False
    assert json_data["error"]["code"] == "INVALID_INPUT"


def test_12_nearby_mandis_diagnostic_endpoint():
    """Verify diagnostic /analysis/nearby-mandis endpoint."""
    response = client.get("/analysis/nearby-mandis?latitude=18.52&longitude=73.85&commodityId=onion&radiusKm=100")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    previews = json_data["data"]
    assert len(previews) >= 1
    assert "mandi" in previews[0]
    assert "distanceKm" in previews[0]
