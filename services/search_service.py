from tavily import TavilyClient
import trafilatura
from config import Settings

settings = Settings()
tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

class SearchService:
    def web_search(self, query: str):
        results = []
        response = tavily_client.search(query, max_results=10)
        for result in response.get("results", []):
            downloaded = trafilatura.fetch_url(result["url"])
            if downloaded:
                content = trafilatura.extract(downloaded, include_comments=False)
            else:
                content = ""
            results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": content
            })
        return results
