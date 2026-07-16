import logging

from fastmcp import FastMCP
from availability_tool import availability_tool

logger = logging.getLogger(__name__)

# Create MCP Server
logger.info("Starting Store Availability MCP Server...")
mcp = FastMCP("Store Availability Server")


@mcp.tool()
def check_product_availability(
    product_name: str,
    user_latitude: float,
    user_longitude: float,
):
    logger.info(
        f"Received tool request: check_product_availability "
        f"(Product: {product_name}, "
        f"Latitude: {user_latitude}, "
        f"Longitude: {user_longitude})"
    )

    result = availability_tool(
        product_name,
        user_latitude,
        user_longitude
    )

    logger.info("Tool execution completed successfully.")

    return result


if __name__ == "__main__":
    logger.info("Launching FastMCP server...")
    mcp.run()