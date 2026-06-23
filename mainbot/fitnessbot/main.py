from coach import calculate_macros


def main() -> None:
    macros = calculate_macros(weight_lbs=205, goal="bulk")
    print("Fitness capability demo")
    print(macros)


if __name__ == "__main__":
    main()
