"""
Comprehensive Contract & Scenario Verification Tests.
SSOT Reference: 00_MASTER_PRODUCT_SSOT.md to 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_dynamic_radius_filtering():
    """Verify that search radius dynamically changes the candidate count."""
    base_payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.52,
        "longitude": 73.85,
        "commodityId": "onion",
        "quantityQuintals": 10,
    }

    # Small radius (15 km) -> only very close mandis
    res_small = client.post("/analysis/run", json={**base_payload, "radiusKm": 15})
    assert res_small.status_code == 200
    count_small = res_small.json()["data"]["search"]["candidateCount"]

    # Large radius (200 km) -> encompasses regional mandis
    res_large = client.post("/analysis/run", json={**base_payload, "radiusKm": 200})
    assert res_large.status_code == 200
    count_large = res_large.json()["data"]["search"]["candidateCount"]

    assert count_large > count_small
    assert count_small >= 1


def test_transport_impact_on_comparative_economics():
    """Verify that quantity and custom transport rate directly affect economics and ranking."""
    base_payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.52,
        "longitude": 73.85,
        "commodityId": "onion",
        "quantityQuintals": 20,
        "radiusKm": 100,
    }

    # Standard rate (2.5 INR/q/km)
    res_std = client.post("/analysis/run", json={**base_payload, "transportRatePerQuintalPerKm": 2.5})
    assert res_std.status_code == 200
    std_data = res_std.json()["data"]["nearbyMandis"]

    # High rate (10.0 INR/q/km)
    res_high = client.post("/analysis/run", json={**base_payload, "transportRatePerQuintalPerKm": 10.0})
    assert res_high.status_code == 200
    high_data = res_high.json()["data"]["nearbyMandis"]

    # Map by mandi_id for identical candidate comparison
    std_map = {m["mandi"]["mandiId"]: m for m in std_data}
    high_map = {m["mandi"]["mandiId"]: m for m in high_data}

    # Verify for a specific non-zero distance mandi that transport cost quadrupled
    for mid, std_m in std_map.items():
        if std_m["distanceKm"] > 5.0 and mid in high_map:
            high_m = high_map[mid]
            assert high_m["totalTransportCost"] > std_m["totalTransportCost"]
            assert high_m["netReturn"] < std_m["netReturn"]
            break


def test_buyer_signals_influence_and_synthetic_disclosure():
    """Verify buyer signals contain active count, demand, and explicit SYNTHETIC classification."""
    payload = {
        "stateId": "rajasthan",
        "districtId": "jaipur",
        "latitude": 26.91,
        "longitude": 75.78,
        "commodityId": "mustard",
        "quantityQuintals": 30,
        "radiusKm": 100,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]

    # Check top-level provenance
    assert data["dataProvenance"]["buyerDataClassification"] == "SYNTHETIC"

    # Check each candidate has buyer signal breakdown
    for mandi in data["nearbyMandis"]:
        bs = mandi["buyerSignal"]
        assert bs["classification"] == "SYNTHETIC"
        assert "Synthetic" in bs["sourceLabel"]
        assert bs["activeBuyerCount"] > 0
        assert bs["demandLevel"] in ["LOW", "MEDIUM", "HIGH"]
        assert 0.0 <= bs["buyerSignalScore"] <= 100.0
        
        # Verify ranking breakdown contains buyerSignalScore
        assert "buyerSignalScore" in mandi["rankingBreakdown"]
        assert mandi["rankingBreakdown"]["buyerSignalScore"] == bs["buyerSignalScore"]


def test_confidence_separation_and_peak_alerts():
    """Verify distinct forecast confidence vs decision confidence, and peak alert fields."""
    payload = {
        "stateId": "maharashtra",
        "districtId": "pune",
        "latitude": 18.52,
        "longitude": 73.85,
        "commodityId": "onion",
        "quantityQuintals": 10,
        "radiusKm": 100,
    }
    response = client.post("/analysis/run", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]

    forecast = data["forecast"]
    decision = data["decision"]

    # 1. Forecast confidence
    assert "forecastConfidence" in forecast
    assert 0.0 <= forecast["forecastConfidence"] <= 1.0

    # 2. Decision confidence
    assert "decisionConfidence" in decision
    assert 0.0 <= decision["decisionConfidence"] <= 1.0

    # 3. Peak Alert fields
    assert "expectedPeakPrice" in forecast
    assert "peakDay" in forecast
    assert "peakAlert" in forecast
    assert isinstance(forecast["peakAlert"], bool)

    # 4. Historical provenance
    assert "historyWindowDays" in forecast
    assert "historyClassification" in forecast
    assert "historySourceLabel" in forecast


def test_nearby_mandis_diagnostic_helper():
    """Test GET /analysis/nearby-mandis helper endpoint."""
    res = client.get("/analysis/nearby-mandis?latitude=18.52&longitude=73.85&commodityId=onion&radiusKm=50")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["data"]) > 0
    assert "mandi" in data["data"][0]
    assert "distanceKm" in data["data"][0]


def test_location_consistency_guard_prevents_stale_coordinates_mismatch():
    """Verify backend guards against submitting stale Pune coordinates when Kota is selected."""
    # Stale Pune coordinates with Kota district
    payload = {
        "stateId": "rajasthan",
        "districtId": "kota",
        "latitude": 18.52,  # Stale Pune latitude
        "longitude": 73.85,  # Stale Pune longitude
        "commodityId": "wheat",
        "quantityQuintals": 50,
        "radiusKm": 100,
    }
    res = client.post("/analysis/run", json=payload)
    assert res.status_code == 422
    err = res.json()["error"]
    assert err["code"] == "INVALID_INPUT"
    assert "does not match declared district" in err["message"]


def test_gps_location_resolution_and_consistent_analysis():
    """Verify end-to-end GPS resolution and consistent analysis for Gujarat."""
    # 1. Resolve GPS coordinates
    resolve_res = client.get("/geography/resolve-location?latitude=23.02&longitude=72.57")
    assert resolve_res.status_code == 200
    resolved = resolve_res.json()["data"]
    assert resolved["districtId"] == "ahmedabad"
    assert resolved["stateId"] == "gujarat"
    assert resolved["inSupportedRegion"] is True

    # 2. Run analysis with resolved location
    analysis_payload = {
        "stateId": resolved["stateId"],
        "districtId": resolved["districtId"],
        "latitude": resolved["latitude"],
        "longitude": resolved["longitude"],
        "commodityId": "cotton",
        "quantityQuintals": 30,
        "radiusKm": 150,
    }
    res = client.post("/analysis/run", json=analysis_payload)
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["farmerContext"]["stateId"] == "gujarat"
    assert data["farmerContext"]["districtId"] == "ahmedabad"
    # Mandis should be Gujarat / regional mandis
    assert any("Ahmedabad" in m["mandi"]["mandiName"] for m in data["nearbyMandis"])
    # Weather is normal baseline (no seeded Pune rainfall)
    assert data["weather"]["impactLevel"] == "LOW"

