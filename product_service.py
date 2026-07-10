from rapidfuzz import process, fuzz
from queries import get_all_products


def find_product(product_name: str):
    """
    Finds the closest matching product using RapidFuzz.
    """

    products = get_all_products()

    if not products:
        return None

    product_names = [
        product["product_name"]
        for product in products
    ]

    match = process.extractOne(
        product_name,
        product_names,
        scorer=fuzz.WRatio
    )

    if match is None:
        return None

    matched_name, score, index = match

    if score < 70:
        return None

    return products[index]