import requests


OSRM_BASE_URL = "https://router.project-osrm.org"


def get_road_route(
    origin_lat,
    origin_lon,
    destination_lat,
    destination_lon
):
    """
    Get real road distance and estimated driving duration
    using the OSRM routing API.

    Coordinates are passed to OSRM as:
    longitude,latitude
    """

    url = (
        f"{OSRM_BASE_URL}"
        f"/route/v1/driving/"
        f"{origin_lon},{origin_lat};"
        f"{destination_lon},{destination_lat}"
    )

    params = {
        "overview": "false"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != "Ok":

            raise ValueError(
                f"Routing failed: "
                f"{data.get('message', data.get('code'))}"
            )

        route = data["routes"][0]

        distance_meters = route["distance"]
        duration_seconds = route["duration"]

        distance_km = (
            distance_meters / 1000
        )

        duration_minutes = (
            duration_seconds / 60
        )

        return {
            "distance_km": round(
                distance_km,
                2
            ),

            "duration_minutes": round(
                duration_minutes,
                2
            ),

            "duration_hours": round(
                duration_minutes / 60,
                2
            )
        }

    except requests.exceptions.RequestException as e:

        raise RuntimeError(
            f"Could not retrieve route: {str(e)}"
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    # Ahmedabad APMC
    origin_lat = 23.0218
    origin_lon = 72.5922

    # Vadodara APMC
    destination_lat = 22.3072
    destination_lon = 73.1812

    route = get_road_route(
        origin_lat,
        origin_lon,
        destination_lat,
        destination_lon
    )

    print(
        "\n========== ROAD ROUTE ==========\n"
    )

    print(
        f"Road Distance: "
        f"{route['distance_km']} km"
    )

    print(
        f"Estimated Duration: "
        f"{route['duration_minutes']} minutes"
    )

    print(
        f"Estimated Duration: "
        f"{route['duration_hours']} hours"
    )