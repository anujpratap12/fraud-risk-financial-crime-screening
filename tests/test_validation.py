import pandas as pd

from src.validation import validate_transactions


def test_clean_dataset_is_valid():
    df = pd.read_csv(
        "data/raw/transactions.csv"
    )

    report, findings = validate_transactions(df)

    assert report["status"] == "VALID"
    assert findings.empty


def test_invalid_amount_is_detected():
    df = pd.read_csv(
        "data/raw/transactions.csv"
    )

    df.loc[0, "amount"] = -500

    report, findings = validate_transactions(df)

    assert report["invalid_amounts"] == 1
    assert report["status"] == "INVALID"


def test_invalid_transaction_type_is_detected():
    df = pd.read_csv(
        "data/raw/transactions.csv"
    )

    df.loc[0, "transaction_type"] = "CRYPTO"

    report, findings = validate_transactions(df)

    assert report["invalid_transaction_types"] == 1
    assert report["status"] == "INVALID"