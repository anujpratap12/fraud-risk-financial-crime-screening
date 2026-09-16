import pandas as pd


VALID_TRANSACTION_TYPES = {
    "UPI",
    "CARD",
    "BANK_TRANSFER",
    "ATM"
}

VALID_MERCHANT_CATEGORIES = {
    "Grocery",
    "Restaurant",
    "Pharmacy",
    "Electronics",
    "Travel",
    "Utilities",
    "Online Shopping"
}

VALID_LOCATIONS = {
    "Delhi",
    "Mumbai",
    "Bengaluru",
    "Hyderabad",
    "Pune",
    "Jaipur",
    "Chandigarh",
    "Dehradun"
}


def validate_transactions(df):
    """
    Validate transaction data and return:
    1. Summary of data-quality issues
    2. Detailed validation findings
    """

    findings = []

    # --------------------------------
    # Missing values
    # --------------------------------

    for column in df.columns:

        missing_rows = df[df[column].isnull()]

        for index in missing_rows.index:

            findings.append({
                "transaction_id": df.loc[
                    index, "transaction_id"
                ],
                "issue_type": "MISSING_VALUE",
                "issue": f"Missing value in {column}"
            })

    # --------------------------------
    # Duplicate transaction IDs
    # --------------------------------

    duplicate_rows = df[
        df["transaction_id"].duplicated(
            keep=False
        )
    ]

    for index in duplicate_rows.index:

        findings.append({
            "transaction_id": df.loc[
                index, "transaction_id"
            ],
            "issue_type": "DUPLICATE_TRANSACTION_ID",
            "issue": "Transaction ID appears more than once"
        })

    # --------------------------------
    # Invalid amounts
    # --------------------------------

    invalid_amount_rows = df[
        df["amount"].notna()
        & (df["amount"] <= 0)
    ]

    for index in invalid_amount_rows.index:

        findings.append({
            "transaction_id": df.loc[
                index, "transaction_id"
            ],
            "issue_type": "INVALID_AMOUNT",
            "issue": "Transaction amount must be greater than zero"
        })

    # --------------------------------
    # Invalid timestamps
    # --------------------------------

    parsed_timestamps = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    invalid_timestamp_rows = df[
        parsed_timestamps.isnull()
    ]

    for index in invalid_timestamp_rows.index:

        findings.append({
            "transaction_id": df.loc[
                index, "transaction_id"
            ],
            "issue_type": "INVALID_TIMESTAMP",
            "issue": "Timestamp could not be parsed"
        })

    # --------------------------------
    # Invalid transaction types
    # --------------------------------

    invalid_type_rows = df[
        ~df["transaction_type"].isin(
            VALID_TRANSACTION_TYPES
        )
    ]

    for index in invalid_type_rows.index:

        findings.append({
            "transaction_id": df.loc[
                index, "transaction_id"
            ],
            "issue_type": "INVALID_TRANSACTION_TYPE",
            "issue": (
                f"Invalid transaction type: "
                f"{df.loc[index, 'transaction_type']}"
            )
        })

    # --------------------------------
    # Invalid merchant categories
    # --------------------------------

    invalid_category_rows = df[
        ~df["merchant_category"].isin(
            VALID_MERCHANT_CATEGORIES
        )
    ]

    for index in invalid_category_rows.index:

        findings.append({
            "transaction_id": df.loc[
                index, "transaction_id"
            ],
            "issue_type": "INVALID_MERCHANT_CATEGORY",
            "issue": (
                f"Invalid merchant category: "
                f"{df.loc[index, 'merchant_category']}"
            )
        })

    # --------------------------------
    # Invalid locations
    # --------------------------------

    invalid_location_rows = df[
        ~df["location"].isin(
            VALID_LOCATIONS
        )
    ]

    for index in invalid_location_rows.index:

        findings.append({
            "transaction_id": df.loc[
                index, "transaction_id"
            ],
            "issue_type": "INVALID_LOCATION",
            "issue": (
                f"Invalid location: "
                f"{df.loc[index, 'location']}"
            )
        })

    # --------------------------------
    # Create findings DataFrame
    # --------------------------------

    findings_df = pd.DataFrame(findings)

    # --------------------------------
    # Create summary
    # --------------------------------

    summary = {
        "total_records": len(df),
        "missing_values": int(
            (findings_df["issue_type"] == "MISSING_VALUE").sum()
        ) if not findings_df.empty else 0,

        "duplicate_transaction_ids": int(
            (
                findings_df["issue_type"]
                == "DUPLICATE_TRANSACTION_ID"
            ).sum()
        ) if not findings_df.empty else 0,

        "invalid_amounts": int(
            (
                findings_df["issue_type"]
                == "INVALID_AMOUNT"
            ).sum()
        ) if not findings_df.empty else 0,

        "invalid_timestamps": int(
            (
                findings_df["issue_type"]
                == "INVALID_TIMESTAMP"
            ).sum()
        ) if not findings_df.empty else 0,

        "invalid_transaction_types": int(
            (
                findings_df["issue_type"]
                == "INVALID_TRANSACTION_TYPE"
            ).sum()
        ) if not findings_df.empty else 0,

        "invalid_merchant_categories": int(
            (
                findings_df["issue_type"]
                == "INVALID_MERCHANT_CATEGORY"
            ).sum()
        ) if not findings_df.empty else 0,

        "invalid_locations": int(
            (
                findings_df["issue_type"]
                == "INVALID_LOCATION"
            ).sum()
        ) if not findings_df.empty else 0
    }

    summary["status"] = (
        "VALID"
        if findings_df.empty
        else "INVALID"
    )

    return summary, findings_df


if __name__ == "__main__":

    data_path = "data/raw/transactions.csv"

    df = pd.read_csv(data_path)

    summary, findings = validate_transactions(df)

    print("\nDATA QUALITY REPORT")
    print("=" * 40)

    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\nVALIDATION FINDINGS")
    print("=" * 40)

    if findings.empty:
        print("No data-quality issues found.")
    else:
        print(findings.to_string(index=False))