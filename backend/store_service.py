from queries import get_store


def get_available_store_details(inventory_list):
    """
    Retrieves complete details for all stores
    that currently have the requested product.
    """

    stores = []

    for item in inventory_list:

        store = get_store(item["store_id"])

        if store:

            stores.append({
                "store_id": store["store_id"],
                "store_name": store["store_name"],
                "address": store["address"],
                "city": store["city"],
                "latitude": store["latitude"],
                "longitude": store["longitude"],
                "quantity": item["quantity"]
            })

    return stores