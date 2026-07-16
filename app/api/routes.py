import logging
from fastapi import APIRouter
from google.genai import types

from app.schemas import (
    ProductAvailabilityRequest,
    ProductAvailabilityResponse,
)
from app.mcp.client import StoreMCPClient
import os
from dotenv import load_dotenv
from google import genai

# Force loading correct GEMINI_API_KEY from root/backend .env to override any incorrect keys
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"), override=True)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()
logger = logging.getLogger(__name__)

# Declare tool schema manually for Gemini SDK
check_availability_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="check_product_availability",
            description="Checks the availability of a product in stores near the user's location.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "product_name": types.Schema(
                        type="STRING",
                        description="The name or query of the product to search."
                    ),
                    "user_latitude": types.Schema(
                        type="NUMBER",
                        description="The user's latitude coordinate."
                    ),
                    "user_longitude": types.Schema(
                        type="NUMBER",
                        description="The user's longitude coordinate."
                    ),
                },
                required=["product_name", "user_latitude", "user_longitude"]
            )
        )
    ]
)


async def _execute_availability_tool(
    product_name: str,
    user_latitude: float,
    user_longitude: float,
) -> dict:
    logger.info(
        f"Executing availability tool: product_name='{product_name}', "
        f"latitude={user_latitude}, longitude={user_longitude}"
    )
    mcp_client = StoreMCPClient()
    result = await mcp_client.check_availability(
        product_name=product_name,
        user_latitude=user_latitude,
        user_longitude=user_longitude,
    )
    return result


@router.post(
    "/availability",
    response_model=ProductAvailabilityResponse,
)
async def check_availability(
    request: ProductAvailabilityRequest,
):
    logger.info(f"Received availability request for product: '{request.query}'")

    prompt = (
        f"User query: {request.query}\n"
        f"User coordinates: Latitude {request.user_latitude}, Longitude {request.user_longitude}\n\n"
        "Please check the availability of the product using the check_product_availability tool. "
        "Make sure to pass the product name and the user's exact latitude and longitude coordinates. "
        "After getting the tool response, respond naturally and concisely to the user in a friendly, conversational tone."
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    ]

    config = types.GenerateContentConfig(
        tools=[check_availability_tool],
        system_instruction="You are a helpful Store Product Availability Assistant.",
        temperature=0.0
    )

    logger.info("Invoking Gemini initially with tool access")
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=contents,
        config=config
    )

    if response.function_calls:
        logger.info("Gemini requested function calls: %s", response.function_calls)
        contents.append(response.candidates[0].content)

        for function_call in response.function_calls:
            if function_call.name == "check_product_availability":
                args = function_call.args
                # Run the async tool
                tool_output = await _execute_availability_tool(
                    product_name=args.get("product_name"),
                    user_latitude=args.get("user_latitude"),
                    user_longitude=args.get("user_longitude")
                )
                logger.info("Tool output: %s", tool_output)

                contents.append(
                    types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=function_call.name,
                                response=tool_output
                            )
                        ]
                    )
                )

        logger.info("Invoking Gemini again with tool output")
        final_response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=contents,
            config=config
        )
        response_text = final_response.text
    else:
        logger.info("Gemini resolved the request directly without tool calls")
        response_text = response.text

    logger.info("Returning successful response to frontend")
    return ProductAvailabilityResponse(
        status="success",
        response=response_text or "No response generated.",
    )