class BankrollManager:

    def kelly(
        self,
        probability,
        odds
    ):
        if not 0 <= probability <= 1:
            raise ValueError("probability must be between 0 and 1")

        if odds <= 1:
            raise ValueError("odds must be decimal odds greater than 1")

        b = odds - 1

        q = 1 - probability

        return (
            (b * probability - q)
            / b
        )
