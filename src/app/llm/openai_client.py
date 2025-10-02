import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

from src.app.interfaces import LLMClientInterface

load_dotenv()

class OpenAIClient(LLMClientInterface):
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
        )

    async def analyze(self, text: str) -> dict:
        try:
            response = await self.client.chat.completions.create(
                model="x-ai/grok-4-fast:free",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": """
                            You are a text analysis expert. Analyze the following text and return a JSON object with the following fields:
                            - summary: A concise summary of the text.
                            - title: A short, catchy title for the text.
                            - topics: A list of 3 relevant topics.
                            - sentiment: The overall sentiment of the text (positive, neutral, or negative).
                        """
                    },
                    {"role": "user", "content": text}
                ]
            )
            print(response)
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(e)
            fallback = {
                "summary": "This is a mock summary due to an API error.",
                "title": "Mock Title",
                "topics": ["mock", "fallback", "error"],
                "sentiment": "neutral"
            }

            return fallback
