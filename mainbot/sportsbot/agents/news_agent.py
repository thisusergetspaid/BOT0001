try:
    import requests
except ImportError:
    requests = None

try:
    from config import NEWS_API_KEY
except ImportError:
    from sportsbot.config import NEWS_API_KEY

class NewsAgent:

    def __init__(self, api_key=None):
        self.api_key = api_key or NEWS_API_KEY

    def get_news(self, query="NBA"):
        if requests is None:
            return {"error": "The requests package is not installed"}

        if not self.api_key:
            return {"error": "NEWS_API_KEY is not configured"}

        url = "https://newsapi.org/v2/everything"

        try:
            response = requests.get(
                url,
                params={"q": query, "apiKey": self.api_key},
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            return {"error": f"News request failed: {exc}"}

        return response.json()
