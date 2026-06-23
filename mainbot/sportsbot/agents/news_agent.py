import requests

class NewsAgent:

    def get_news(self):

        url = (
            "https://newsapi.org/v2/everything?"
            "q=NBA&apiKey=YOUR_KEY"
        )

        response = requests.get(url)

        return response.json()