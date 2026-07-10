from nearest_store import find_nearest_store

stores = [
    {
        "store_name": "Lulu Mall",
        "distance_km": 1.35,
        "quantity": 5
    },
    {
        "store_name": "Forum Mall",
        "distance_km": 2.80,
        "quantity": 4
    },
    {
        "store_name": "Oberon Mall",
        "distance_km": 3.00,
        "quantity": 3
    }
]

nearest = find_nearest_store(stores)

print(nearest)