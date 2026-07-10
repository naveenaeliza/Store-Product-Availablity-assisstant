from distance_service import calculate_store_distances

stores = [
    {
        "store_name": "Lulu Mall",
        "latitude": 10.028,
        "longitude": 76.308,
        "quantity": 5
    },
    {
        "store_name": "Forum Mall",
        "latitude": 10.011,
        "longitude": 76.331,
        "quantity": 3
    }
]

result = calculate_store_distances(
    10.030,
    76.320,
    stores
)

for store in result:
    print(store)