import pandas as pd

from src.risk_scoring import calculate_risk_score


def test_high_amount_increases_risk_score():
    df = pd.DataFrame({
        "amount": [50000],
        "amount_deviation_ratio": [1],
        "high_velocity": [0],
        "location_change": [0],
        "minutes_since_previous_transaction": [120],
        "anomaly_flag": [0]
    })

    result = calculate_risk_score(df)

    assert result.loc[0, "risk_score"] == 25
    assert result.loc[0, "risk_level"] == "LOW"


def test_multiple_risk_signals_create_high_risk():
    df = pd.DataFrame({
        "amount": [50000],
        "amount_deviation_ratio": [6],
        "high_velocity": [1],
        "location_change": [0],
        "minutes_since_previous_transaction": [120],
        "anomaly_flag": [0]
    })

    result = calculate_risk_score(df)

    assert result.loc[0, "risk_score"] == 65
    assert result.loc[0, "risk_level"] == "HIGH"


def test_anomaly_contributes_to_score():
    df = pd.DataFrame({
        "amount": [1000],
        "amount_deviation_ratio": [1],
        "high_velocity": [0],
        "location_change": [0],
        "minutes_since_previous_transaction": [120],
        "anomaly_flag": [1]
    })

    result = calculate_risk_score(df)

    assert result.loc[0, "risk_score"] == 20
    assert result.loc[0, "risk_level"] == "LOW"


def test_normal_transaction_has_zero_score():
    df = pd.DataFrame({
        "amount": [1000],
        "amount_deviation_ratio": [1],
        "high_velocity": [0],
        "location_change": [0],
        "minutes_since_previous_transaction": [120],
        "anomaly_flag": [0]
    })

    result = calculate_risk_score(df)

    assert result.loc[0, "risk_score"] == 0
    assert result.loc[0, "risk_level"] == "LOW"