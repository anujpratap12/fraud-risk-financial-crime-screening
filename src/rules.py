import pandas as pd


def apply_risk_rules(df):
    """
    Apply transparent rule-based controls
    to identify transactions requiring review.
    """

    df = df.copy()

    # Store reasons for each transaction
    df["risk_reasons"] = ""

    # --------------------------------
    # Rule 1: Unusually high amount
    # --------------------------------

    high_amount = df["amount"] >= 30000

    df.loc[
        high_amount,
        "risk_reasons"
    ] += "HIGH_AMOUNT;"

    # --------------------------------
    # Rule 2: Significant deviation
    # from customer history
    # --------------------------------

    high_deviation = (
        df["amount_deviation_ratio"] >= 5
    )

    df.loc[
        high_deviation,
        "risk_reasons"
    ] += "HIGH_AMOUNT_DEVIATION;"

    # --------------------------------
    # Rule 3: High transaction velocity
    # --------------------------------

    high_velocity = (
        df["high_velocity"] == 1
    )

    df.loc[
        high_velocity,
        "risk_reasons"
    ] += "HIGH_VELOCITY;"

    # --------------------------------
    # Rule 4: Rapid location change
    # --------------------------------

    rapid_location_change = (
        (df["location_change"] == 1)
        & (df["minutes_since_previous_transaction"] <= 60)
    )

    df.loc[
        rapid_location_change,
        "risk_reasons"
    ] += "RAPID_LOCATION_CHANGE;"

    # --------------------------------
    # Remove trailing semicolon
    # --------------------------------

    df["risk_reasons"] = (
        df["risk_reasons"]
        .str.rstrip(";")
    )

    # --------------------------------
    # Flag transactions
    # --------------------------------

    df["rule_flagged"] = (
        df["risk_reasons"] != ""
    ).astype(int)

    return df


if __name__ == "__main__":

    from feature_engineering import create_features

    input_path = "data/raw/transactions.csv"

    df = pd.read_csv(input_path)

    # Create behavioral features
    df = create_features(df)

    # Apply rules
    df = apply_risk_rules(df)

    flagged = df[
        df["rule_flagged"] == 1
    ]

    print("\nRULE-BASED RISK ANALYSIS")
    print("=" * 40)

    print(
        f"Total transactions: {len(df)}"
    )

    print(
        f"Flagged transactions: {len(flagged)}"
    )

    print(
        f"Flag rate: "
        f"{len(flagged) / len(df) * 100:.2f}%"
    )

    print("\nRule trigger counts:")

    for rule in [
        "HIGH_AMOUNT",
        "HIGH_AMOUNT_DEVIATION",
        "HIGH_VELOCITY",
        "RAPID_LOCATION_CHANGE"
    ]:

        count = (
            flagged["risk_reasons"]
            .str.contains(rule, regex=False)
            .sum()
        )

        print(
            f"{rule}: {count}"
        )

    print("\nSample flagged transactions:")

    print(
        flagged[
            [
                "transaction_id",
                "customer_id",
                "amount",
                "amount_deviation_ratio",
                "high_velocity",
                "location",
                "previous_location",
                "risk_reasons"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )