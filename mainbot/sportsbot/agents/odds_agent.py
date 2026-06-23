try:
    import requests
except ImportError:
    requests = None

try:
    from config import ODDS_API_KEY
except ImportError:
    from sportsbot.config import ODDS_API_KEY

class OddsAgent:

    def __init__(self, api_key=None):
        self.api_key = api_key or ODDS_API_KEY

    def get_odds(self, sport="basketball_nba", regions="us", markets="h2h"):
        if requests is None:
            return {"error": "The requests package is not installed"}

        if not self.api_key:
            return {"error": "ODDS_API_KEY is not configured"}

        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"

        try:
            response = requests.get(
                url,
                params={
                    "apiKey": self.api_key,
                    "regions": regions,
                    "markets": markets,
                },
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            return {"error": f"Odds request failed: {exc}"}

        return response.json()
