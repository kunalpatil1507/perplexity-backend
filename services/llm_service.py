import google.generativeai as genai
from config import Settings

settings = Settings()

genai.configure(api_key=settings.GEMINI_API_KEY)

class LLMService:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")

    def generate_response(self, query: str, search_results: list[dict]):
        context_text = "\n\n".join(
            [f"Source {i+1} ({res['url']}):\n{res['content']}" for i, res in enumerate(search_results)]
        )
        prompt = f"""
        Context from web search:
        {context_text}

        Query: {query}

        Provide a detailed, well-cited response using only the context above. Think carefully.
        """

        try:
            response = self.model.generate_content(prompt, stream=True)
            for chunk in response:
                yield chunk.text
        except Exception as e:
            yield f"LLMService error: {e}"
