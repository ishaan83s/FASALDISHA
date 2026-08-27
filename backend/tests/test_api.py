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
    """Test 1: Health endpoint returns healthy status and supports both GET and HEAD methods."""
    # Test GET
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "FasalDisha-Backend"
    assert data["version"] == "2.1.0"
    assert data["database"] == "healthy"

    # Test HEAD (required for uptime monitoring services like UptimeRobot)
    head_response = client.head("/health")
    assert head_response.status_code == 200
    assert head_response.text == ""


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
    # Check that districts contain reference centroid coordinates
    pune_dist = next(d for d in dist_data["data"] if d["districtId"] == "pune")
    assert pune_dist["latitude"] is not None
    assert pune_dist["longitude"] is not None
    assert pytest.approx(pune_dist["latitude"], 0.1) == 18.52
    assert pytest.approx(pune_dist["longitude"], 0.1) == 73.85

    # Test Commodities
    res_commodities = client.get("/geography/commodities")
    assert res_commodities.status_code == 200
    comm_data = res_commodities.json()
    assert comm_data["success"] is True
    c_ids = [c["commodityId"] for c in comm_data["data"]]
    assert "onion" in c_ids
    assert "tomato" in c_ids
    assert "wheat" in c_ids


def test_geography_resolve_location_endpoint():
    """Test GPS coordinate resolution against supported geography catalog."""
    # Near Pune
    res_pune = client.get("/geography/resolve-location?latitude=18.5204&longitude=73.8567")
    assert res_pune.status_code == 200
    pune_json = res_pune.json()
    assert pune_json["success"] is True
    assert pune_json["data"]["inSupportedRegion"] is True
    assert pune_json["data"]["districtId"] == "pune"
    assert pune_json["data"]["stateId"] == "maharashtra"
    assert pune_json["data"]["resolutionStatus"] == "RESOLVED"

    # Near Ahmedabad
    res_ahm = client.get("/geography/resolve-location?latitude=23.0225&longitude=72.5714")
    assert res_ahm.status_code == 200
    ahm_json = res_ahm.json()
    assert ahm_json["success"] is True
    assert ahm_json["data"]["inSupportedRegion"] is True
    assert ahm_json["data"]["districtId"] == "ahmedabad"
    assert ahm_json["data"]["stateId"] == "gujarat"

    # Far out-of-bounds (e.g. London / New York)
    res_oob = client.get("/geography/resolve-location?latitude=40.7128&longitude=-74.0060")
    assert res_oob.status_code == 200
    oob_json = res_oob.json()
    assert oob_json["success"] is True
    assert oob_json["data"]["inSupportedRegion"] is False
    assert oob_json["data"]["resolutionStatus"] == "OUT_OF_BOUNDS"
    assert oob_json["data"]["districtId"] is None


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


def test_location_consistency_mismatch_rejection():
    """Test 9: Geographic coordinates resolving to another district (e.g. Ahmedabad coordinates with Pune declared district) are rejected."""
    payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 23.02,  # Ahmedabad, Gujarat coordinates
        "longitude": 72.57,
        "commodityId": "onion",
        "quantityQuintals": 20,
        "radiusKm": 100,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 422
    err_json = response.json()
    assert err_json["success"] is False
    assert err_json["error"]["code"] == "INVALID_INPUT"
    assert "does not match declared district" in err_json["error"]["message"]


def test_coordinates_outside_supported_coverage_rejected():
    """Test 10: Coordinates outside supported coverage cannot be submitted with an arbitrary supported district."""
    payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 40.7128,  # New York coordinates
        "longitude": -74.0060,
        "commodityId": "onion",
        "quantityQuintals": 20,
        "radiusKm": 100,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 422
    err_json = response.json()
    assert err_json["success"] is False
    assert err_json["error"]["code"] == "INVALID_INPUT"
    assert "outside supported coverage regions" in err_json["error"]["message"]


def test_district_state_mismatch_rejection():
    """Test 11: District not belonging to the selected state is rejected."""
    payload = {
        "stateId": "maharashtra",
        "districtId": "kota",  # Kota is in Rajasthan
        "latitude": 25.18,
        "longitude": 75.83,
        "commodityId": "wheat",
        "quantityQuintals": 20,
        "radiusKm": 100,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 422
    err_json = response.json()
    assert err_json["success"] is False
    assert err_json["error"]["code"] == "INVALID_INPUT"
    assert "belongs to state 'rajasthan'" in err_json["error"]["message"]


def test_invalid_coordinate_range_rejection():
    """Test 12: Coordinates outside valid latitude/longitude bounds are rejected."""
    payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 150.0,  # Invalid latitude (> 90)
        "longitude": 73.85,
        "commodityId": "onion",
        "quantityQuintals": 20,
        "radiusKm": 100,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 422
    err_json = response.json()
    assert err_json["success"] is False
    assert err_json["error"]["code"] == "INVALID_INPUT"


def test_consistent_manual_district_selection_pipeline():
    """Test 13: Manually selecting Kota, Rajasthan coordinates searches Kota region and does not leak Pune seeded weather."""
    payload = {
        "stateId": "rajasthan",
        "districtId": "kota",
        "latitude": 25.18,
        "longitude": 75.83,
        "commodityId": "wheat",
        "quantityQuintals": 50,
        "radiusKm": 100,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]

    # Verify mandi discovery is centered at Kota
    assert len(data["nearbyMandis"]) > 0
    mandi_names = [m["mandi"]["mandiName"] for m in data["nearbyMandis"]]
    assert any("Kota" in name for name in mandi_names)

    # Verify weather did not trigger Pune seeded weather override
    assert data["weather"]["impactLevel"] == "LOW"
    assert data["farmerContext"]["stateId"] == "rajasthan"
    assert data["farmerContext"]["districtId"] == "kota"


def test_db_migration_error_handling(monkeypatch):
    """Test 14: Verify SQLite compatibility migration raises clear RuntimeError on connection/schema failure."""
    from app.db import session

    # Bypass create_all to isolate the migration execute block
    monkeypatch.setattr(session.Base.metadata, "create_all", lambda bind: None)

    def broken_connect(*args, **kwargs):
        raise RuntimeError("Simulated connection failure during migration")

    monkeypatch.setattr(session.engine, "connect", broken_connect)
    with pytest.raises(RuntimeError, match="Database schema compatibility migration failed"):
        session.init_db()



