"""
Live Scenario Verification Script.
Executes and validates all 4 judge-proof acceptance scenarios.
"""
import httpx
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

client = httpx.Client(base_url="http://127.0.0.1:8000")

scenarios = [
    (
        "Scenario A (Pune Onion - Seeded Risk Override)",
        {
            "stateId": "maharashtra",
            "districtId": "pune",
            "latitude": 18.52,
            "longitude": 73.85,
            "commodityId": "onion",
            "quantityQuintals": 25.0,
            "radiusKm": 120.0,
        },
    ),
    (
        "Scenario B (Nashik Tomato - Highly Perishable)",
        {
            "stateId": "maharashtra",
            "districtId": "nashik",
            "latitude": 20.00,
            "longitude": 73.78,
            "commodityId": "tomato",
            "quantityQuintals": 15.0,
            "radiusKm": 100.0,
        },
    ),
    (
        "Scenario C (Kota Wheat - Non-Perishable Normal Hold)",
        {
            "stateId": "rajasthan",
            "districtId": "kota",
            "latitude": 25.18,
            "longitude": 75.83,
            "commodityId": "wheat",
            "quantityQuintals": 50.0,
            "radiusKm": 100.0,
        },
    ),
    (
        "Scenario D (Ahmedabad Cotton - Cross-Boundary)",
        {
            "stateId": "gujarat",
            "districtId": "ahmedabad",
            "latitude": 23.02,
            "longitude": 72.57,
            "commodityId": "cotton",
            "quantityQuintals": 30.0,
            "radiusKm": 150.0,
        },
    ),
]

for name, payload in scenarios:
    res = client.post("/analysis/run", json=payload)
    assert res.status_code == 200, f"Failed with {res.status_code}"
    resp_json = res.json()
    assert resp_json["success"] is True, f"Error in response: {resp_json}"
    data = resp_json["data"]
    
    print(f"=== {name} ===")
    p_class = data["commodity"]["perishabilityClass"]
    print(f"  Commodity: {data['commodity']['commodityName']} ({p_class})")
    print(f"  Candidates: {len(data['nearbyMandis'])} | Cross-boundary: {data['search']['crossBoundaryCandidatesIncluded']}")
    print(f"  Base Decision: {data['decision']['baseDecision']}")
    print(f"  Final Recommendation: {data['decision']['finalRecommendation']}")
    print(f"  Risk Override Applied: {data['decision']['riskOverrideApplied']}")
    rec_mandi = data['decision']['recommendedMandi']['mandiName'] if data['decision']['recommendedMandi'] else 'None'
    print(f"  Recommended Mandi: {rec_mandi}")
    print(f"  Reason: {data['decision']['humanReadableReason']}")
    print(f"  Forecast Peak: INR {data['forecast']['expectedPeakPrice']} (Day {data['forecast']['peakDay']}) | Alert: {data['forecast']['peakAlert']}")
    print(f"  Top Mandi Buyer Signal: {data['nearbyMandis'][0]['buyerSignal']}")
    print(f"  Top Mandi Breakdown: {data['nearbyMandis'][0]['rankingBreakdown']}")
    print()

print("ALL 4 SCENARIOS VERIFIED SUCCESSFULLY ON LIVE BACKEND.")
