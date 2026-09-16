import pandas as pd


def calculate_risk_score(df):
    """
    Combine rule-based signals and Isolation Forest anomaly
    detection into a transparent transaction risk score.
    """

    df = df.copy()

    # Start every transaction with zero risk points
    df["risk_score"] = 0

    # Store exactly why points were added
    df["score_breakdown"] = ""

    # --------------------------------
    # 1. High transaction amount
    # --------------------------------

    high_amount = df["amount"] >= 30000

    df.loc[high_amount, "risk_score"] += 25

    df.loc[
        high_amount,
        "score_breakdown"
    ] += "HIGH_AMOUNT (+25); "

    # --------------------------------
    # 2. Amount significantly above
    # customer's typical transaction
    # --------------------------------

    high_deviation = (
        df["amount_deviation_ratio"] >= 5
    )

    df.loc[high_deviation, "risk_score"] += 20

    df.loc[
        high_deviation,
        "score_breakdown"
    ] += "HIGH_AMOUNT_DEVIATION (+20); "

    # --------------------------------
    # 3. High transaction velocity
    # --------------------------------

    high_velocity = (
        df["high_velocity"] == 1
    )

    df.loc[high_velocity, "risk_score"] += 20

    df.loc[
        high_velocity,
        "score_breakdown"
    ] += "HIGH_VELOCITY (+20); "

    # --------------------------------
    # 4. Rapid location change
    # --------------------------------

    rapid_location = (
        (df["location_change"] == 1)
        & (df["minutes_since_previous_transaction"] <= 60)
    )

    df.loc[rapid_location, "risk_score"] += 15

    df.loc[
        rapid_location,
        "score_breakdown"
    ] += "RAPID_LOCATION_CHANGE (+15); "

    # --------------------------------
    # 5. Isolation Forest anomaly
    # --------------------------------

    anomaly = (
        df["anomaly_flag"] == 1
    )

    df.loc[anomaly, "risk_score"] += 20

    df.loc[
        anomaly,
        "score_breakdown"
    ] += "ISOLATION_FOREST_ANOMALY (+20); "

    # Remove the final semicolon and space
    df["score_breakdown"] = (
        df["score_breakdown"]
        .str.rstrip("; ")
    )

    # --------------------------------
    # Risk classification
    # --------------------------------

    def classify_risk(score):

        if score >= 60:
            return "HIGH"

        elif score >= 30:
            return "MEDIUM"

        else:
            return "LOW"

    df["risk_level"] = (
        df["risk_score"]
        .apply(classify_risk)
    )

    return df


# --------------------------------
# Test the complete risk scoring
# pipeline
# --------------------------------

if __name__ == "__main__":

    from feature_engineering import create_features
    from rules import apply_risk_rules
    from anomaly_detection import detect_anomalies

    input_path = "data/raw/transactions.csv"

    # Load synthetic transaction data
    df = pd.read_csv(input_path)

    # Step 1: Create behavioral features
    df = create_features(df)

    # Step 2: Apply explainable risk rules
    df = apply_risk_rules(df)

    # Step 3: Detect statistical anomalies
    df = detect_anomalies(df)

    # Step 4: Calculate transparent risk score
    df = calculate_risk_score(df)

    # --------------------------------
    # Display results
    # --------------------------------

    print("\nTRANSACTION RISK SCORING")
    print("=" * 40)

    print(f"Total transactions: {len(df)}")

    print("\nRisk distribution:")

    print(
        df["risk_level"]
        .value_counts()
        .sort_index()
    )

    print("\nScore distribution:")

    print(
        df["risk_score"]
        .describe()
    )

    print("\nHigh-risk transactions:")

    high_risk = df[
        df["risk_level"] == "HIGH"
    ]

    print(
        high_risk[
            [
                "transaction_id",
                "customer_id",
                "amount",
                "risk_score",
                "risk_level",
                "risk_reasons",
                "score_breakdown",
                "anomaly_flag"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )