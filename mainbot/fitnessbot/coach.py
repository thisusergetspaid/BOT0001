def calculate_macros(
    weight_lbs,
    goal
):
    protein = weight_lbs * 1.0

    if goal == "cut":
        calories = weight_lbs * 12

    elif goal == "bulk":
        calories = weight_lbs * 18

    else:
        calories = weight_lbs * 15

    fats = calories * 0.25 / 9

    carbs = (
        calories -
        (protein * 4) -
        (fats * 9)
    ) / 4

    return {
        "calories": round(calories),
        "protein": round(protein),
        "carbs": round(carbs),
        "fats": round(fats)
    }