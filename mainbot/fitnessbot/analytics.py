import pandas as pd

def weight_trend(weights):
    df = pd.DataFrame(
        {"weight": weights}
    )

    return (
        df["weight"]
        .rolling(7)
        .mean()
        .tolist()
    )

def progression_score(
    workouts
):
    volume = 0

    for workout in workouts:
        volume += (
            workout["sets"] *
            workout["reps"] *
            workout["weight"]
        )

    return volume