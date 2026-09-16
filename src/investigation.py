import pandas as pd


def generate_investigation_rationale(row):
    """
    Generate a human-readable explanation
    for why a transaction was flagged.
    """

    reasons = []

    if row["amount"] >= 30000:
        reasons.append(
            f"Transaction amount of ₹{row['amount']:,.2f} "
            "is unusually high."
        )

    if row["amount_deviation_ratio"] >= 5:
        reasons.append(
            f"Transaction amount is "
            f"{row['amount_deviation_ratio']:.1f}x "
            "the customer's average transaction amount."
        )

    if row["high_velocity"] == 1:
        reasons.append(
            f"{int(row['transactions_last_10min'])} transactions "
            "occurred within a 10-minute window."
        )

    if (
        row["location_change"] == 1
        and row["minutes_since_previous_transaction"] <= 60
    ):
        minutes = row["minutes_since_previous_transaction"]

        if minutes == 0:
            location_message = (
                f"Location changed from "
                f"{row['previous_location']} to "
                f"{row['location']} at the same transaction timestamp."
            )
        else:
            location_message = (
                f"Location changed from "
                f"{row['previous_location']} to "
                f"{row['location']} within "
                f"{minutes:.0f} minutes."
            )

        reasons.append(location_message)

    if row["anomaly_flag"] == 1:
        reasons.append(
            "Isolation Forest identified the transaction "
            "as statistically unusual."
        )

    if not reasons:
        return "No significant risk signals identified."

    return " ".join(reasons)


def recommend_action(risk_level):
    """
    Provide a suggested review action based on
    the calculated risk level.
    """

    if risk_level == "HIGH":
        return "Escalate for detailed review"

    elif risk_level == "MEDIUM":
        return "Request additional verification"

    else:
        return "Close / no further action"


def create_investigation_records(df):
    """
    Create investigation-ready records for
    transactions requiring review.
    """

    df = df.copy()

    # Generate human-readable rationale
    df["investigation_rationale"] = df.apply(
        generate_investigation_rationale,
        axis=1
    )

    # Generate recommended next action
    df["recommended_action"] = df["risk_level"].apply(
        recommend_action
    )

    # Keep transactions that require review
    review_df = df[
        df["risk_level"].isin(["MEDIUM", "HIGH"])
    ].copy()

    # Select investigation-relevant columns
    investigation_columns = [
        "transaction_id",
        "customer_id",
        "timestamp",
        "amount",
        "transaction_type",
        "merchant_category",
        "location",
        "previous_location",
        "customer_avg_amount",
        "amount_deviation_ratio",
        "transactions_last_10min",
        "transactions_last_1hr",
        "risk_reasons",
        "anomaly_score",
        "risk_score",
        "risk_level",
        "score_breakdown",
        "investigation_rationale",
        "recommended_action"
    ]

    return review_df[investigation_columns]


if __name__ == "__main__":

    from feature_engineering import create_features
    from rules import apply_risk_rules
    from anomaly_detection import detect_anomalies
    from risk_scoring import calculate_risk_score

    input_path = "data/raw/transactions.csv"
    output_path = "reports/investigation_findings.csv"

    # Load synthetic transaction data
    df = pd.read_csv(input_path)

    # Feature engineering
    df = create_features(df)

    # Rule-based detection
    df = apply_risk_rules(df)

    # ML anomaly detection
    df = detect_anomalies(df)

    # Risk scoring
    df = calculate_risk_score(df)

    # Create investigation records
    investigation_df = create_investigation_records(df)

    # Save investigation findings
    investigation_df.to_csv(
        output_path,
        index=False
    )

    print("\nINVESTIGATION WORKFLOW")
    print("=" * 40)

    print(
        f"Transactions requiring review: "
        f"{len(investigation_df)}"
    )

    print(
        f"Saved findings to: {output_path}"
    )

    print("\nRisk levels:")

    print(
        investigation_df["risk_level"]
        .value_counts()
    )

    print("\nSample investigation findings:")

    print(
        investigation_df[
            [
                "transaction_id",
                "customer_id",
                "amount",
                "risk_score",
                "risk_level",
                "investigation_rationale",
                "recommended_action"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )