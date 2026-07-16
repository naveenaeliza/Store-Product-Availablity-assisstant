from inventory_service import check_product_availability
from store_service import get_available_store_details
from distance_service import calculate_store_distances
from nearest_store import find_nearest_store
from product_service import find_product


def availability_tool(
    product_name,
    user_latitude,
    user_longitude
):
    """
    Finds the nearest store where the requested product
    is available.
    """

    # Step 1: Find the closest matching product
    product = find_product(product_name)

    if product is None:
        return {
            "success": False,
            "message": "The requested query is outside the scope of this assistant. Please try a different search.."
        }

    product_id = product["product_id"]

    # Step 2: Check inventory
    result = check_product_availability(product_id)

    if not result["success"]:
        return result

    # Step 3: Get complete store details
    stores = get_available_store_details(result["inventory"])

    # Step 4: Calculate distance
    stores = calculate_store_distances(
        user_latitude,
        user_longitude,
        stores
    )

    # Step 5: Find nearest store
    nearest = find_nearest_store(stores)

    # Step 6: Return response
    return {
        "success": True,
        "product": product["product_name"],
        "store_name": nearest["store_name"],
        "address": nearest["address"],
        "city": nearest["city"],
        "distance_km": nearest["distance_km"],
        "available_stock": nearest["quantity"]
    }