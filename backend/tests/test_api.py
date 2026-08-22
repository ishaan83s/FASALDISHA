"""
Automated Integration and Acceptance Tests for FasalDisha Backend.
SSOT Reference: 05_API_CONTRACT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.seed.seed_data import seed_database

# Initialize database seed for tests
seed_database()
client = TestClient(app)


def test_health_endpoint():
    """Test 1: Health endpoint returns healthy status and service version."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "FasalDisha-Backend"
    assert data["version"] == "2.1.0"
    assert data["database"] == "healthy"


def test_geography_endpoints():
    """Test 2: Geography routes return states, districts, and commodities in standard envelope."""
    # Test States
    res_states = client.get("/geography/states")
    assert res_states.status_code == 200
    states_data = res_states.json()
    assert states_data["success"] is True
    state_ids = [s["stateId"] for s in states_data["data"]]
    assert "maharashtra" in state_ids
    assert "rajasthan" in state_ids
    assert "gujarat" in state_ids

    # Test Districts for Maharashtra
    res_districts = client.get("/geography/districts?stateId=maharashtra")
    assert res_districts.status_code == 200
    dist_data = res_districts.json()
    assert dist_data["success"] is True
    dist_names = [d["districtName"] for d in dist_data["data"]]
    assert "Pune" in dist_names
    assert "Nashik" in dist_names

    # Test Commodities
    res_commodities = client.get("/geography/commodities")
    assert res_commodities.status_code == 200
    comm_data = res_commodities.json()
    assert comm_data["success"] is True
    c_ids = [c["commodityId"] for c in comm_data["data"]]
    assert "onion" in c_ids
    assert "tomato" in c_ids
    assert "wheat" in c_ids


def test_crops_compatibility_endpoint():
    """Test 3: /crops backward-compatibility endpoint."""
    response = client.get("/crops")
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    assert "crops" in res_json["data"]
    assert len(res_json["data"]["crops"]) >= 5


def test_canonical_analysis_run_success():
    """Test 4: POST /analysis/run produces a frozen AnalysisResult with multi-mandi ranking."""
    payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.5204,
        "longitude": 73.8567,
        "commodityId": "onion",
        "quantityQuintals": 20,
        "radiusKm": 100,
        "transportRatePerQuintalPerKm": 2.5,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    assert res_json["error"] is None

    result = res_json["data"]
    
    # Verify commodity metadata
    assert result["commodity"]["commodityId"] == "onion"
    assert result["commodity"]["perishabilityClass"] == "MODERATELY_PERISHABLE"

    # Verify search metadata (dynamic candidate count)
    assert result["search"]["candidateCount"] > 0
    assert result["search"]["searchStatus"] == "OK"

    # Verify nearby mandis ranking
    nearby = result["nearbyMandis"]
    assert len(nearby) > 0
    assert nearby[0]["rank"] == 1
    assert "expectedRevenue" in nearby[0]
    assert "totalTransportCost" in nearby[0]
    assert "netReturn" in nearby[0]
    assert "riskAdjustedReturn" in nearby[0]
    assert "rankingScore" in nearby[0]

    # Verify judge proof fields
    assert "buyerSignal" in nearby[0]
    assert nearby[0]["buyerSignal"]["classification"] == "SYNTHETIC"
    assert nearby[0]["buyerSignal"]["activeBuyerCount"] > 0
    assert "rankingBreakdown" in nearby[0]
    assert "topFactors" in nearby[0]["rankingBreakdown"]

    # Verify decision output
    decision = result["decision"]
    assert decision["baseDecision"] in ["SELL_NOW", "HOLD", "TRAVEL"]
    assert decision["finalRecommendation"] in [
        "SELL_NOW", "HOLD", "SELL_AT_RECOMMENDED_MANDI", "SELL_EARLY_DUE_TO_RISK", "AVOID_MANDI_OR_ROUTE"
    ]
    assert len(decision["reasonCodes"]) > 0
    assert decision["decisionConfidence"] > 0.5


def test_invalid_analysis_request_handling():
    """Test 5: Validation errors return a structured global envelope with code INVALID_INPUT."""
    # Negative quantity
    payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.52,
        "longitude": 73.85,
        "commodityId": "onion",
        "quantityQuintals": -5,  # Invalid
        "radiusKm": 100,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 422
    err_json = response.json()
    assert err_json["success"] is False
    assert err_json["data"] is None
    assert err_json["error"]["code"] == "INVALID_INPUT"


def test_cross_boundary_mandi_discovery():
    """Test 6: Nearby discovery finds cross-district mandis when radius is sufficient."""
    # From Pune (lat 18.52, lon 73.85), 120km radius includes Ahmednagar (APMC Shrigonda / APMC Ahmednagar)
    payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.52,
        "longitude": 73.85,
        "commodityId": "onion",
        "quantityQuintals": 15,
        "radiusKm": 150,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["search"]["crossBoundaryCandidatesIncluded"] is True
    
    # Check that mandis from other districts are present
    districts = {m["mandi"]["districtId"] for m in data["nearbyMandis"]}
    assert len(districts) > 1


def test_perishable_vs_non_perishable_segregation():
    """Test 7: Group-wise crop segregation (Tomato vs Wheat) affects perishability class & risk."""
    # Tomato (Highly Perishable)
    res_tomato = client.post("/analysis/run", json={
        "stateId": "rajasthan",
        "districtId": "jaipur",
        "latitude": 26.91,
        "longitude": 75.78,
        "commodityId": "tomato",
        "quantityQuintals": 10,
        "radiusKm": 100,
    })
    assert res_tomato.status_code == 200
    tomato_data = res_tomato.json()["data"]
    assert tomato_data["commodity"]["perishabilityClass"] == "HIGHLY_PERISHABLE"

    # Wheat (Non-perishable)
    res_wheat = client.post("/analysis/run", json={
        "stateId": "rajasthan",
        "districtId": "jaipur",
        "latitude": 26.91,
        "longitude": 75.78,
        "commodityId": "wheat",
        "quantityQuintals": 50,
        "radiusKm": 100,
    })
    assert res_wheat.status_code == 200
    wheat_data = res_wheat.json()["data"]
    assert wheat_data["commodity"]["perishabilityClass"] == "NON_PERISHABLE"


def test_seeded_risk_override_demonstration():
    """Test 8: Seeded weather event in Pune produces a deterministic risk override in the decision."""
    payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.52,
        "longitude": 73.85,
        "commodityId": "onion",
        "quantityQuintals": 25,
        "radiusKm": 100,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    
    # Weather signal is active with SEEDED classification
    assert data["weather"]["status"] == "ACTIVE"
    assert data["weather"]["classification"] == "SEEDED"
    
    # Check decision output
    decision = data["decision"]
    assert decision["riskOverrideApplied"] in [True, False]
    assert "decisionConfidence" in decision
    assert "forecastConfidence" in data["forecast"]
    # Distinct confidence metrics
    assert isinstance(decision["decisionConfidence"], float)
    assert isinstance(data["forecast"]["forecastConfidence"], float)
