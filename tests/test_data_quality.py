import pandas as pd

from src.validation import validate_transactions


def test_generated_dataset_has_expected_size():
    df = pd.read_csv("data/raw/transactions.csv")

    assert len(df) == 3000
    assert df["transaction_id"].nunique() == 3000


def test_generated_dataset_has_no_missing_values():
    df = pd.read_csv("data/raw/transactions.csv")

    assert df.isnull().sum().sum() == 0


def test_generated_dataset_passes_validation():
    df = pd.read_csv("data/raw/transactions.csv")

    report, findings = validate_transactions(df)

    assert report["status"] == "VALID"
    assert findings.empty