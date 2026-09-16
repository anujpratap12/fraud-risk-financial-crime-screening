import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df):
    """
    Detect unusual transactions using Isolation Forest.
    """

    df = df.copy()

    # Features used by the anomaly detection model
    features = [
        "amount",
        "amount_deviation_ratio",
        "transactions_last_10min",
        "transactions_last_1hr",
        "minutes_since_previous_transaction",
        "account_age_days"
    ]

    # Create the Isolation Forest model
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    # Train the model and predict anomalies
    predictions = model.fit_predict(df[features])

    # Isolation Forest returns:
    #  1  = normal
    # -1  = anomaly
    df["anomaly_flag"] = (predictions == -1).astype(int)

    # Store the model's anomaly score
    df["anomaly_score"] = model.decision_function(df[features])

    return df


if __name__ == "__main__":

    from feature_engineering import create_features

    input_path = "data/raw/transactions.csv"

    df = pd.read_csv(input_path)

    # Create behavioral features
    df = create_features(df)

    # Detect unusual transactions
    df = detect_anomalies(df)

    anomalies = df[df["anomaly_flag"] == 1]

    print("\nISOLATION FOREST ANOMALY DETECTION")
    print("=" * 45)

    print(f"Total transactions: {len(df)}")
    print(f"Anomalies detected: {len(anomalies)}")
    print(f"Anomaly rate: {len(anomalies) / len(df) * 100:.2f}%")

    print("\nSample anomalies:")

    print(
        anomalies[
            [
                "transaction_id",
                "customer_id",
                "amount",
                "amount_deviation_ratio",
                "transactions_last_10min",
                "transactions_last_1hr",
                "anomaly_score"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )