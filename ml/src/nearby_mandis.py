import pandas as pd
from math import radians, sin, cos, sqrt, atan2

from route_service import get_road_route


# ============================================================
# FILE PATHS
# ============================================================

MANDI_MASTER_FILE = "data/mandi_master.csv"
MARKET_DATA_FILE = "data/processed_mandi_data.csv"


# ============================================================
# HAVERSINE DISTANCE
# ============================================================

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate straight-line distance between two mandis.

    This is used only to find nearby candidate mandis.
    Final transport calculations should use road distance.
    """

    earth_radius = 6371.0

    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return earth_radius * c


# ============================================================
# GET NEARBY MANDIS
# ============================================================

def get_nearby_mandis(
    selected_mandi,
    radius_km=100,
    max_results=4,
    commodity=None
):
    """
    Find nearby mandis that have ML prediction data.

    Workflow:
    1. Load mandi coordinates.
    2. Find mandis with data for the selected commodity.
    3. Use Haversine distance to shortlist candidates.
    4. Expand the search radius if needed.
    5. Call OSRM for the shortlisted mandis.
    6. Return real road distance and travel duration.
    """

    # --------------------------------------------------------
    # LOAD MANDI MASTER
    # --------------------------------------------------------

    df = pd.read_csv(
        MANDI_MASTER_FILE
    )

    df = df.drop_duplicates(
        subset=["mandi"]
    ).copy()

    df["state"] = (
        df["state"]
        .astype(str)
        .str.strip()
    )

    df["district"] = (
        df["district"]
        .astype(str)
        .str.strip()
    )

    df["mandi"] = (
        df["mandi"]
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------------
    # FIND SELECTED MANDI
    # --------------------------------------------------------

    selected_mandi_clean = (
        str(selected_mandi)
        .strip()
        .lower()
    )

    selected_matches = df[
        df["mandi"]
        .str.lower()
        ==
        selected_mandi_clean
    ]

    if selected_matches.empty:
        raise ValueError(
            f"Mandi '{selected_mandi}' "
            f"was not found in mandi_master.csv"
        )

    selected = selected_matches.iloc[0]


    # --------------------------------------------------------
    # LOAD ML MARKET DATA
    # --------------------------------------------------------

    market_data = pd.read_csv(
        MARKET_DATA_FILE
    )

    market_data["mandi_clean"] = (
        market_data["mandi"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    market_data["commodity_clean"] = (
        market_data["commodity"]
        .astype(str)
        .str.strip()
        .str.lower()
    )


    # --------------------------------------------------------
    # FILTER MANDIS WITH AVAILABLE ML DATA
    # --------------------------------------------------------

    if commodity is not None:

        commodity_clean = (
            str(commodity)
            .strip()
            .lower()
        )

        available_mandis = set(
            market_data[
                market_data["commodity_clean"]
                ==
                commodity_clean
            ]["mandi_clean"].unique()
        )

    else:

        available_mandis = set(
            market_data["mandi_clean"].unique()
        )


    # --------------------------------------------------------
    # CALCULATE STRAIGHT-LINE DISTANCES
    # --------------------------------------------------------

    candidates = []

    for _, mandi in df.iterrows():

        mandi_name = mandi["mandi"]

        # Skip selected mandi
        if (
            mandi_name.lower()
            ==
            selected_mandi_clean
        ):
            continue

        # Skip mandis without prediction data
        if (
            mandi_name.lower()
            not in available_mandis
        ):
            continue

        straight_distance = calculate_distance(
            selected["latitude"],
            selected["longitude"],
            mandi["latitude"],
            mandi["longitude"]
        )

        candidates.append({
            "State": mandi["state"],
            "District": mandi["district"],
            "Mandi": mandi_name,

            "Latitude": float(
                mandi["latitude"]
            ),

            "Longitude": float(
                mandi["longitude"]
            ),

            "Straight Distance (km)": round(
                straight_distance,
                2
            )
        })


    candidate_df = pd.DataFrame(
        candidates
    )

    if candidate_df.empty:

        return candidate_df


    # --------------------------------------------------------
    # SORT BY STRAIGHT-LINE DISTANCE
    # --------------------------------------------------------

    candidate_df = candidate_df.sort_values(
        "Straight Distance (km)"
    ).reset_index(
        drop=True
    )


    # --------------------------------------------------------
    # ADAPTIVE SEARCH
    # --------------------------------------------------------

    nearby_candidates = candidate_df[
        candidate_df[
            "Straight Distance (km)"
        ]
        <=
        radius_km
    ]

    # Expand only if not enough candidates
    if len(nearby_candidates) < max_results:

        for expanded_radius in [
            150,
            250,
            500,
            1000
        ]:

            nearby_candidates = candidate_df[
                candidate_df[
                    "Straight Distance (km)"
                ]
                <=
                expanded_radius
            ]

            if (
                len(nearby_candidates)
                >=
                max_results
            ):
                break


    # --------------------------------------------------------
    # FINAL CANDIDATE SHORTLIST
    # --------------------------------------------------------

    nearby_candidates = (
        nearby_candidates
        .head(max_results)
        .copy()
    )


    # --------------------------------------------------------
    # GET REAL ROAD ROUTES
    # --------------------------------------------------------

    route_results = []

    print(
        f"\nCalculating road routes for "
        f"{len(nearby_candidates)} nearby mandis..."
    )

    for _, mandi in nearby_candidates.iterrows():

        try:

            route = get_road_route(
                origin_lat=float(
                    selected["latitude"]
                ),

                origin_lon=float(
                    selected["longitude"]
                ),

                destination_lat=float(
                    mandi["Latitude"]
                ),

                destination_lon=float(
                    mandi["Longitude"]
                )
            )

            route_results.append({

                "State":
                    mandi["State"],

                "District":
                    mandi["District"],

                "Mandi":
                    mandi["Mandi"],

                "Straight Distance (km)":
                    mandi[
                        "Straight Distance (km)"
                    ],

                "Road Distance (km)":
                    route["distance_km"],

                "Travel Duration (minutes)":
                    route[
                        "duration_minutes"
                    ],

                "Travel Duration (hours)":
                    route[
                        "duration_hours"
                    ]
            })


        except Exception as error:

            print(
                f"Warning: Route lookup failed for "
                f"{mandi['Mandi']}: {error}"
            )

            # Fallback to straight-line distance
            route_results.append({

                "State":
                    mandi["State"],

                "District":
                    mandi["District"],

                "Mandi":
                    mandi["Mandi"],

                "Straight Distance (km)":
                    mandi[
                        "Straight Distance (km)"
                    ],

                "Road Distance (km)":
                    mandi[
                        "Straight Distance (km)"
                    ],

                "Travel Duration (minutes)":
                    None,

                "Travel Duration (hours)":
                    None
            })


    # --------------------------------------------------------
    # CREATE FINAL RESULT
    # --------------------------------------------------------

    result_df = pd.DataFrame(
        route_results
    )

    if result_df.empty:
        return result_df

    # Sort by actual road distance
    result_df = result_df.sort_values(
        "Road Distance (km)"
    ).reset_index(
        drop=True
    )

    return result_df


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    nearby = get_nearby_mandis(

        selected_mandi=
            "Ahmedabad APMC",

        commodity=
            "Banana",

        radius_km=120,

        max_results=4
    )


    print(
        "\n========== NEARBY MANDIS WITH ROAD ROUTES ==========\n"
    )

    if nearby.empty:

        print(
            "No nearby mandis found."
        )

    else:

        print(
            nearby.to_string(
                index=False
            )
        )