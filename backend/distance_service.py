from distance_calculator import calculate_distance


def calculate_store_distances(user_lat, user_lon, stores):
    """
    Calculates the distance from the user's location
    to every available store.

    Parameters:
        user_lat (float)
        user_lon (float)
        stores (list)

    Returns:
        List of stores with distance added.
    """

    stores_with_distance = []

    for store in stores:

        distance = calculate_distance(
            user_lat,
            user_lon,
            store["latitude"],
            store["longitude"]
        )

        store["distance_km"] = distance

        stores_with_distance.append(store)

    return stores_with_distance