Store Product Availability Assistant
-----------------------------------

1. server.py
- Creates and starts the FastMCP Server.
- Registers the check_product_availability() tool.
- Receives requests from the MCP client and forwards them to the backend logic.

------------------------------------------------------------

2. availability_tool.py
- Acts as the main controller of the application.
- Uses RapidFuzz to identify the requested product, retrieves inventory, calculates store distances, and selects the nearest store.
- Returns the final JSON response containing product availability, nearest store, stock, and distance.

------------------------------------------------------------

3. database.py
- Establishes the connection between Python and the Supabase database.
- Loads the Supabase URL and API key from the .env file.
- Provides a reusable database client for the application.

------------------------------------------------------------

4. queries.py
- Contains all database operations.
- Retrieves products, inventory, and store information from Supabase.
- Separates database access from business logic.

------------------------------------------------------------

5. product_service.py
- Matches the user's product name with the closest product in the database.
- Uses RapidFuzz for fuzzy string matching.
- Returns the matched product and its product ID.

------------------------------------------------------------

6. inventory_service.py
- Checks whether the requested product is available.
- Retrieves inventory records where stock quantity is greater than zero.
- Returns all stores currently stocking the product.

------------------------------------------------------------

7. store_service.py
- Retrieves complete details of stores that have the product.
- Fetches store name, address, latitude, longitude, and available quantity.
- Prepares store information for distance calculation.

------------------------------------------------------------

8. distance_utils.py
- Implements the Haversine Formula.
- Calculates the distance between the user's location and each store.
- Returns the distance in kilometers.

------------------------------------------------------------

9. distance_service.py
- Calls the Haversine calculation for every available store.
- Computes the distance from the user to each store.
- Appends the calculated distance to each store record.

------------------------------------------------------------

10. nearest_store.py
- Compares the distances of all available stores.
- Selects the store with the minimum distance.
- Returns the nearest store to the user.

------------------------------------------------------------

11. schema.sql
- Defines the PostgreSQL/Supabase database schema.
- Creates the Products, Stores, and Inventory tables.
- Establishes relationships and indexes for efficient querying.

------------------------------------------------------------

12. .env
- Stores configuration values securely.
- Contains the Supabase Project URL and API Key.
- Prevents sensitive credentials from being hardcoded.

------------------------------------------------------------

13. requirements.txt
- Lists all Python dependencies required for the project.
- Allows easy installation of libraries using pip.
- Ensures a consistent development environment across systems.
