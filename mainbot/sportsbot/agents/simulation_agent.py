import random

class SimulationAgent:

    def simulate_game(
        self,
        home_strength,
        away_strength,
        runs=10000
    ):

        home_wins = 0

        for _ in range(runs):

            home_score = (
                random.gauss(
                    home_strength,
                    10
                )
            )

            away_score = (
                random.gauss(
                    away_strength,
                    10
                )
            )

            if home_score > away_score:
                home_wins += 1

        return {
            "home_win_pct":
            home_wins / runs
        }