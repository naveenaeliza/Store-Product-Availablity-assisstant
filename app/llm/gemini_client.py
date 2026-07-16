import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiClient:
    """
    Wrapper class for the Google Gemini client.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")

        self.client = genai.Client(api_key=api_key)

    def generate_response(
        self,
        prompt: str,
        model: str = "gemini-2.5-pro",
    ) -> str:
        """
        Generate a response from Gemini.
        """

        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
        )

        return response.text

    def get_client(self):
        return self.client


# Singleton instance
gemini_client = GeminiClient()

# For simple response generation
generate_response = gemini_client.generate_response

# Optional: export raw client if needed elsewhere
client = gemini_client.get_client()