from rapidfuzz import process, fuzz
from queries import get_all_products
from query_parser import extract_product


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
    clean_query = extract_product(product_name)
    match = process.extractOne(
        clean_query,
        product_names,
        scorer=fuzz.WRatio
    )

    if match is None:
        return None

    matched_name, score, index = match

    if score < 70:
        return None

    return products[index]