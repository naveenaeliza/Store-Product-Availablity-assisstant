from haversine import haversine, Unit


def calculate_distance(user_lat, user_lon, store_lat, store_lon):
    """
    Calculates the distance between the user's location
    and a store using the Haversine Formula.

    Returns:
        Distance in kilometers
    """

    user_location = (user_lat, user_lon)
    store_location = (store_lat, store_lon)

    distance = haversine(
        user_location,
        store_location,
        unit=Unit.KILOMETERS
    )

    return round(distance, 2)