def find_nearest_store(stores):
    """
    Finds the nearest store from a list of stores.

    Parameters:
        stores (list): List of stores with distance_km

    Returns:
        dict: Nearest store
    """

    if not stores:
        return None

    nearest = min(
        stores,
        key=lambda store: store["distance_km"]
    )

    return nearest