from availability_tool import availability_tool

# Get input from user
product_name = input("Enter Product Name: ")

user_latitude = float(input("Enter Your Latitude: "))
user_longitude = float(input("Enter Your Longitude: "))

# Call the tool
result = availability_tool(
    product_name,
    user_latitude,
    user_longitude
)

# Print the response
print("\nResult:")
print(result)