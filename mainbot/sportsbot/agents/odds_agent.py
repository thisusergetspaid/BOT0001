import requests

class OddsAgent:

    def get_odds(self):

        url = (
            "https://api.the-odds-api.com/v4/sports/"
        )

        response = requests.get(url)

        return response.json()