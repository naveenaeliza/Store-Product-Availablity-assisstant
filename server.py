from fastmcp import FastMCP
from availability_tool import availability_tool

# Create MCP Server
mcp = FastMCP("Store Availability Server")


@mcp.tool()
def check_product_availability(
    product_name: str,
    user_latitude: float,
    user_longitude: float,
):
    return availability_tool(
        product_name,
        user_latitude,
        user_longitude
    )

if __name__ == "__main__":
    mcp.run()