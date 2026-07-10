from distance_calculator import calculate_distance

# User Location
user_lat = 10.0300
user_lon = 76.3200

# Store Location (Lulu Mall)
store_lat = 10.0280
store_lon = 76.3080

distance = calculate_distance(
    user_lat,
    user_lon,
    store_lat,
    store_lon
)

print(f"Distance : {distance} km")