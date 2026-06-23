from agents.news_agent import NewsAgent
from agents.odds_agent import OddsAgent

from agents.simulation_agent import (
    SimulationAgent
)

def main():

    news = NewsAgent()

    odds = OddsAgent()

    sim = SimulationAgent()

    latest_news = news.get_news()

    sportsbook_odds = odds.get_odds()

    result = sim.simulate_game(
        110,
        102
    )

    print(result)

if __name__ == "__main__":
    main()