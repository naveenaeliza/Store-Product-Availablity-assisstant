from queries import get_product, get_available_inventory


def check_product_availability(product_id: int):
    """
    Checks whether the product exists and whether it
    is available in any store.
    """

    # Step 1 : Check if product exists
    product = get_product(product_id)

    if product is None:
        return {
            "success": False,
            "message": "Product not found"
        }

    # Step 2 : Get available inventory
    inventory = get_available_inventory(product_id)

    if len(inventory) == 0:
        return {
            "success": False,
            "message": "Product is currently out of stock"
        }

    # Step 3 : Return inventory
    return {
        "success": True,
        "product": product,
        "inventory": inventory
    }