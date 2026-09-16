import pandas as pd

from src.rules import apply_risk_rules


def test_high_amount_rule():
    df = pd.DataFrame({
        "amount": [50000],
        "amount_deviation_ratio": [1],
        "high_velocity": [0],
        "location_change": [0],
        "minutes_since_previous_transaction": [120]
    })

    result = apply_risk_rules(df)

    assert result.loc[0, "rule_flagged"] == 1
    assert "HIGH_AMOUNT" in result.loc[0, "risk_reasons"]


def test_high_velocity_rule():
    df = pd.DataFrame({
        "amount": [1000],
        "amount_deviation_ratio": [1],
        "high_velocity": [1],
        "location_change": [0],
        "minutes_since_previous_transaction": [120]
    })

    result = apply_risk_rules(df)

    assert result.loc[0, "rule_flagged"] == 1
    assert "HIGH_VELOCITY" in result.loc[0, "risk_reasons"]


def test_rapid_location_change_rule():
    df = pd.DataFrame({
        "amount": [1000],
        "amount_deviation_ratio": [1],
        "high_velocity": [0],
        "location_change": [1],
        "minutes_since_previous_transaction": [10]
    })

    result = apply_risk_rules(df)

    assert result.loc[0, "rule_flagged"] == 1
    assert "RAPID_LOCATION_CHANGE" in result.loc[0, "risk_reasons"]


def test_normal_transaction_not_flagged():
    df = pd.DataFrame({
        "amount": [1000],
        "amount_deviation_ratio": [1],
        "high_velocity": [0],
        "location_change": [0],
        "minutes_since_previous_transaction": [120]
    })

    result = apply_risk_rules(df)

    assert result.loc[0, "rule_flagged"] == 0
    assert result.loc[0, "risk_reasons"] == ""