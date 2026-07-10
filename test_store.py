from inventory_service import check_product_availability
from store_service import get_available_store_details

result = check_product_availability(1)

if result["success"]:

    stores = get_available_store_details(result["inventory"])

    print(stores)

else:

    print(result["message"])