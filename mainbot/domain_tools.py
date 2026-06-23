import re
from dataclasses import dataclass

from fitnessbot.coach import calculate_macros
from sportsbot.agents.simulation_agent import SimulationAgent
from sportsbot.ai.bankroll import BankrollManager


@dataclass(frozen=True)
class ToolResult:
    text: str


class DomainTools:
    """Small deterministic helpers for questions the bot can answer locally."""

    _bankroll_re = re.compile(
        r"\b(?:kelly|bankroll)\b.*?(?P<probability>\d+(?:\.\d+)?)\s*%?.*?"
        r"(?:odds|price|decimal)\s*(?P<odds>\d+(?:\.\d+)?)",
        re.IGNORECASE,
    )
    _macro_re = re.compile(
        r"\b(?:macro|macros|calorie|calories)\b.*?(?P<weight>\d+(?:\.\d+)?)\s*"
        r"(?:lb|lbs|pounds)?\b.*?\b(?P<goal>cut|bulk|maintain|maintenance)\b",
        re.IGNORECASE,
    )
    _simulation_re = re.compile(
        r"\b(?:simulate|simulation)\b.*?(?:home|team\s*a)?\s*(?P<home>\d+(?:\.\d+)?)"
        r".*?(?:away|team\s*b)?\s*(?P<away>\d+(?:\.\d+)?)",
        re.IGNORECASE,
    )

    def __init__(self) -> None:
        self._bankroll = BankrollManager()
        self._simulation = SimulationAgent()

    def try_answer(self, message: str) -> ToolResult | None:
        return (
            self._answer_bankroll(message)
            or self._answer_macros(message)
            or self._answer_simulation(message)
        )

    def _answer_bankroll(self, message: str) -> ToolResult | None:
        match = self._bankroll_re.search(message)
        if not match:
            return None

        probability = float(match.group("probability"))
        odds = float(match.group("odds"))
        if probability > 1:
            probability = probability / 100

        try:
            fraction = self._bankroll.kelly(probability, odds)
        except ValueError as exc:
            return ToolResult(text=f"I could not calculate Kelly sizing: {exc}.")
        suggested = max(0.0, fraction)

        return ToolResult(
            text=(
                f"Using full Kelly with probability {probability:.1%} and decimal odds "
                f"{odds:.2f}, the stake fraction is {fraction:.1%} of bankroll.\n\n"
                f"Practical read: {suggested:.1%} if you are using full Kelly, often less "
                "for risk control. This is math, not financial advice."
            )
        )

    def _answer_macros(self, message: str) -> ToolResult | None:
        match = self._macro_re.search(message)
        if not match:
            return None

        weight = float(match.group("weight"))
        goal = match.group("goal").lower()
        if goal == "maintenance":
            goal = "maintain"

        macros = calculate_macros(weight, goal)

        return ToolResult(
            text=(
                f"For {weight:g} lb and a {goal} goal, a simple starting target is:\n"
                f"- Calories: {macros['calories']} kcal\n"
                f"- Protein: {macros['protein']} g\n"
                f"- Carbs: {macros['carbs']} g\n"
                f"- Fats: {macros['fats']} g\n\n"
                "Adjust from weekly weight trend, training performance, hunger, and recovery."
            )
        )

    def _answer_simulation(self, message: str) -> ToolResult | None:
        match = self._simulation_re.search(message)
        if not match:
            return None

        home_strength = float(match.group("home"))
        away_strength = float(match.group("away"))
        result = self._simulation.simulate_game(home_strength, away_strength)

        return ToolResult(
            text=(
                f"Simulated home strength {home_strength:g} vs away strength {away_strength:g}.\n"
                f"Estimated home win probability: {result['home_win_pct']:.1%}.\n\n"
                "This is a toy normal-distribution simulation until we connect real team, injury, "
                "market, and historical data."
            )
        )
