from database import get_supabase_client

db = get_supabase_client()


def get_product(product_id: int):
    """
    Retrieve a product using its product ID.
    """

    response = (
        db.table("products")
        .select("*")
        .eq("product_id", product_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


def get_available_inventory(product_id: int):
    """
    Retrieve inventory records where quantity > 0
    """

    response = (
        db.table("inventory")
        .select("*")
        .eq("product_id", product_id)
        .gt("quantity", 0)
        .execute()
    )

    return response.data


def get_store(store_id: int):
    """
    Retrieve store details using store ID.
    """

    response = (
        db.table("stores")
        .select("*")
        .eq("store_id", store_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None
def get_all_products():
    """
    Retrieve all products from the database.
    """

    response = (
        db.table("products")
        .select("product_id, product_name")
        .execute()
    )

    return response.data