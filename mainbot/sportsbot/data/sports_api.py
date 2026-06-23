try:
    import requests
except ImportError:
    requests = None

try:
    from config import SPORTS_API_BASE_URL, SPORTS_API_KEY
except ImportError:
    from sportsbot.config import SPORTS_API_BASE_URL, SPORTS_API_KEY

class SportsData:

    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or SPORTS_API_KEY
        self.base_url = base_url or SPORTS_API_BASE_URL

    def get_team_stats(
        self,
        team_id
    ):
        if requests is None:
            return {"error": "The requests package is not installed"}

        if not self.base_url:
            return {"error": "SPORTS_API_BASE_URL is not configured"}

        url = f"{self.base_url.rstrip('/')}/team/{team_id}"
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as exc:
            return {"error": f"Sports data request failed: {exc}"}

        return response.json()
