import pandas as pd


def create_features(df):
    """
    Create behavioral features for transaction risk analysis.
    """

    # Make a copy so the original DataFrame is not modified
    df = df.copy()

    # Convert timestamp into datetime format
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    # Sort transactions chronologically for each customer
    df = df.sort_values(
        by=["customer_id", "timestamp"]
    ).reset_index(drop=True)

    # --------------------------------
    # 1. Customer historical average
    # --------------------------------

    df["customer_avg_amount"] = (
        df.groupby("customer_id")["amount"]
        .transform("mean")
    )

    # --------------------------------
    # 2. Amount deviation ratio
    # --------------------------------

    df["amount_deviation_ratio"] = (
        df["amount"] / df["customer_avg_amount"]
    )

    # --------------------------------
    # 3. Previous transaction amount
    # --------------------------------

    df["previous_transaction_amount"] = (
        df.groupby("customer_id")["amount"]
        .shift(1)
    )

    # --------------------------------
    # 4. Time since previous transaction
    # --------------------------------

    df["minutes_since_previous_transaction"] = (
        df.groupby("customer_id")["timestamp"]
        .diff()
        .dt.total_seconds()
        / 60
    )

    # --------------------------------
    # 5. Transactions in last 10 minutes
    # --------------------------------

    def calculate_10_minute_velocity(group):

        timestamps = group["timestamp"]
        counts = []

        for current_time in timestamps:

            window_start = current_time - pd.Timedelta(minutes=10)

            count = (
                (timestamps >= window_start)
                & (timestamps <= current_time)
            ).sum()

            counts.append(count)

        return pd.Series(
            counts,
            index=group.index
        )

    df["transactions_last_10min"] = (
        df.groupby("customer_id", group_keys=False)
        .apply(
            calculate_10_minute_velocity,
            include_groups=False
        )
        .reset_index(level=0, drop=True)
    )

    # --------------------------------
    # 6. Transactions in last 1 hour
    # --------------------------------

    def calculate_1_hour_velocity(group):

        timestamps = group["timestamp"]
        counts = []

        for current_time in timestamps:

            window_start = current_time - pd.Timedelta(hours=1)

            count = (
                (timestamps >= window_start)
                & (timestamps <= current_time)
            ).sum()

            counts.append(count)

        return pd.Series(
            counts,
            index=group.index
        )

    df["transactions_last_1hr"] = (
        df.groupby("customer_id", group_keys=False)
        .apply(
            calculate_1_hour_velocity,
            include_groups=False
        )
        .reset_index(level=0, drop=True)
    )

    # A customer is considered high velocity
    # when 3 or more transactions occur
    # within 10 minutes.
    df["high_velocity"] = (
        df["transactions_last_10min"] >= 3
    ).astype(int)

    # --------------------------------
    # 7. Previous location
    # --------------------------------

    df["previous_location"] = (
        df.groupby("customer_id")["location"]
        .shift(1)
    )

    # --------------------------------
    # 8. Location change
    # --------------------------------

    df["location_change"] = (
        (df["location"] != df["previous_location"])
        & df["previous_location"].notna()
    ).astype(int)

    # --------------------------------
    # 9. Customer transaction count
    # --------------------------------

    df["customer_transaction_count"] = (
        df.groupby("customer_id")["transaction_id"]
        .transform("count")
    )

    return df


# --------------------------------
# Test the feature engineering
# --------------------------------

if __name__ == "__main__":

    input_path = "data/raw/transactions.csv"

    df = pd.read_csv(input_path)

    df = create_features(df)

    print("\nFEATURE ENGINEERING COMPLETE")
    print("=" * 40)

    print(f"Total records: {len(df)}")

    print("\nNew behavioral features:")

    print([
        "customer_avg_amount",
        "amount_deviation_ratio",
        "previous_transaction_amount",
        "minutes_since_previous_transaction",
        "transactions_last_10min",
        "transactions_last_1hr",
        "high_velocity",
        "previous_location",
        "location_change"
    ])

    print("\nSample:")

    print(
        df[
            [
                "transaction_id",
                "customer_id",
                "amount",
                "customer_avg_amount",
                "amount_deviation_ratio",
                "minutes_since_previous_transaction",
                "transactions_last_10min",
                "transactions_last_1hr",
                "high_velocity",
                "location",
                "previous_location",
                "location_change"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )