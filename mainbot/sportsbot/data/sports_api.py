import requests

class SportsData:

    def get_team_stats(
        self,
        team_id
    ):

        url = f"https://api.example.com/team/{team_id}"

        response = requests.get(url)

        return response.json()