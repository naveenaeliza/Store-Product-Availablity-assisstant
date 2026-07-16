import os
import logging
import json
from typing import AsyncGenerator, Dict, Any
from contextlib import asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from app.config import settings

logger = logging.getLogger("mcp_client")


class StoreMCPClient:
    """
    MCP Client wrapper for interacting with the Store Availability Server.
    Supports both STDIO and SSE transports.
    """

    def __init__(self):
        self.transport_type = settings.MCP_TRANSPORT.lower()
        self.sse_url = settings.MCP_SSE_URL
        self.stdio_command = settings.MCP_STDIO_COMMAND
        self.stdio_args = settings.MCP_STDIO_ARGS

        logger.info(f"MCP Client initialized with transport: {self.transport_type}")

    @asynccontextmanager
    async def _get_session(self) -> AsyncGenerator[ClientSession, None]:
        """
        Creates and initializes a ClientSession based on configured transport.
        """
        if self.transport_type == "sse":
            logger.info(f"Connecting to MCP server via SSE at {self.sse_url}")
            async with sse_client(self.sse_url) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    logger.info("Initializing MCP session...")
                    await session.initialize()
                    logger.info("MCP session initialized successfully.")
                    yield session
                    logger.info("Closing MCP session.")

        elif self.transport_type == "stdio":
            logger.info(
                f"Connecting to MCP server via STDIO: {self.stdio_command} {self.stdio_args}"
            )

            # Ensure environment variables are passed so Supabase database can connect
            env = os.environ.copy()

            if settings.SUPABASE_URL:
                env["SUPABASE_URL"] = settings.SUPABASE_URL

            if settings.SUPABASE_KEY:
                env["SUPABASE_KEY"] = settings.SUPABASE_KEY

            server_params = StdioServerParameters(
                command=self.stdio_command,
                args=self.stdio_args,
                env=env,
            )

            async with stdio_client(server_params) as (read_stream, write_stream):
                logger.info("STDIO connection established.")

                async with ClientSession(read_stream, write_stream) as session:
                    logger.info("Initializing MCP session...")
                    await session.initialize()
                    logger.info("MCP session initialized successfully.")

                    yield session

                    logger.info("Closing MCP session.")

        else:
            logger.error(f"Unsupported MCP transport type: {self.transport_type}")
            raise ValueError(f"Unsupported MCP transport type: {self.transport_type}")

    async def check_availability(
        self,
        product_name: str,
        user_latitude: float,
        user_longitude: float,
    ) -> Dict[str, Any]:
        """
        Calls the 'check_product_availability' tool on the MCP server.
        """

        logger.info(f"Preparing availability check for product: {product_name}")

        tool_name = "check_product_availability"

        arguments = {
            "product_name": product_name,
            "user_latitude": user_latitude,
            "user_longitude": user_longitude,
        }

        try:

            async with self._get_session() as session:

                logger.info(
                    f"Calling tool '{tool_name}' with arguments: {arguments}"
                )

                result = await session.call_tool(tool_name, arguments)

                logger.info(f"Tool '{tool_name}' executed successfully.")

                if not result.content:
                    logger.warning("No content returned from MCP tool.")
                    return {
                        "success": False,
                        "message": "No response content from MCP tool.",
                    }

                text_content = ""

                for content_item in result.content:
                    if hasattr(content_item, "text"):
                        text_content += content_item.text
                    elif isinstance(content_item, dict) and "text" in content_item:
                        text_content += content_item["text"]

                if getattr(result, "isError", False):
                    logger.error(f"MCP tool returned an error: {text_content}")
                    return {
                        "success": False,
                        "message": f"MCP tool error: {text_content}",
                    }

                try:
                    parsed = json.loads(text_content)

                    if isinstance(parsed, dict):
                        logger.info("Successfully parsed MCP tool response.")
                        return parsed

                    else:
                        logger.warning("Unexpected response format received from MCP tool.")
                        return {
                            "success": False,
                            "message": f"Unexpected tool response format: {text_content}",
                        }

                except json.JSONDecodeError:
                    logger.error("Failed to parse MCP response as JSON.")
                    return {
                        "success": False,
                        "message": text_content or "No text content returned.",
                    }

        except Exception as e:
            logger.error(
                f"Failed to check product availability via MCP: {str(e)}",
                exc_info=True,
            )

            return {
                "success": False,
                "message": f"MCP client error: {str(e)}",
            }