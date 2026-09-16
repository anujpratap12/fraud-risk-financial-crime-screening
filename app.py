import streamlit as st
import pandas as pd

from src.feature_engineering import create_features
from src.rules import apply_risk_rules
from src.anomaly_detection import detect_anomalies
from src.risk_scoring import calculate_risk_score
from src.investigation import create_investigation_records


# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="Fraud Risk Investigation System",
    page_icon="🔎",
    layout="wide"
)


# --------------------------------
# Load and process data
# --------------------------------

@st.cache_data
def load_data():

    input_path = "data/raw/transactions.csv"

    df = pd.read_csv(input_path)

    # Create behavioral features
    df = create_features(df)

    # Apply rule-based controls
    df = apply_risk_rules(df)

    # Detect statistical anomalies
    df = detect_anomalies(df)

    # Calculate transparent risk score
    df = calculate_risk_score(df)

    return df


df = load_data()


# --------------------------------
# Create investigation records
# --------------------------------

investigation_df = create_investigation_records(df)


# --------------------------------
# Sidebar filters
# --------------------------------

st.sidebar.title("Investigation Filters")

risk_filter = st.sidebar.multiselect(
    "Risk Level",
    options=["HIGH", "MEDIUM", "LOW"],
    default=["HIGH", "MEDIUM"]
)

transaction_types = sorted(
    df["transaction_type"].unique()
)

transaction_filter = st.sidebar.multiselect(
    "Transaction Type",
    options=transaction_types,
    default=transaction_types
)

locations = sorted(
    df["location"].unique()
)

location_filter = st.sidebar.multiselect(
    "Location",
    options=locations,
    default=locations
)

min_score = st.sidebar.slider(
    "Minimum Risk Score",
    min_value=0,
    max_value=int(df["risk_score"].max()),
    value=0
)


# --------------------------------
# Apply filters
# --------------------------------

filtered_df = df[
    (df["risk_level"].isin(risk_filter))
    & (df["transaction_type"].isin(transaction_filter))
    & (df["location"].isin(location_filter))
    & (df["risk_score"] >= min_score)
].copy()


# --------------------------------
# Dashboard header
# --------------------------------

st.title(
    "🔎 Fraud Risk & Transaction Anomaly Investigation System"
)

st.markdown(
    """
This dashboard analyzes **synthetic banking transaction data**
using explainable risk rules and Isolation Forest anomaly detection.

Transactions are prioritized for review based on observed risk signals.
The system does not determine whether a transaction is fraudulent.
"""
)


# --------------------------------
# KPI metrics
# --------------------------------

total_transactions = len(df)

transactions_for_review = len(
    df[df["risk_level"].isin(["HIGH", "MEDIUM"])]
)

high_risk = len(
    df[df["risk_level"] == "HIGH"]
)

medium_risk = len(
    df[df["risk_level"] == "MEDIUM"]
)

anomalies = int(
    df["anomaly_flag"].sum()
)


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Transactions",
    f"{total_transactions:,}"
)

col2.metric(
    "For Review",
    f"{transactions_for_review:,}"
)

col3.metric(
    "High Risk",
    f"{high_risk:,}"
)

col4.metric(
    "Medium Risk",
    f"{medium_risk:,}"
)

col5.metric(
    "ML Anomalies",
    f"{anomalies:,}"
)


# --------------------------------
# Risk distribution
# --------------------------------

st.subheader("Risk Distribution")

risk_distribution = (
    df["risk_level"]
    .value_counts()
    .reindex(
        ["LOW", "MEDIUM", "HIGH"],
        fill_value=0
    )
)

st.bar_chart(risk_distribution)


# --------------------------------
# Rule trigger summary
# --------------------------------

st.subheader("Rule Trigger Summary")

rule_counts = {
    "High Amount": (
        df["amount"] >= 30000
    ).sum(),

    "High Amount Deviation": (
        df["amount_deviation_ratio"] >= 5
    ).sum(),

    "High Velocity": (
        df["high_velocity"] == 1
    ).sum(),

    "Rapid Location Change": (
        (df["location_change"] == 1)
        & (
            df["minutes_since_previous_transaction"] <= 60
        )
    ).sum()
}

rule_summary = pd.DataFrame(
    list(rule_counts.items()),
    columns=["Rule", "Triggered"]
)

st.dataframe(
    rule_summary,
    use_container_width=True,
    hide_index=True
)


# --------------------------------
# Investigation queue
# --------------------------------

st.subheader(
    f"Investigation Queue ({len(filtered_df)} transactions)"
)

display_columns = [
    "transaction_id",
    "customer_id",
    "timestamp",
    "amount",
    "transaction_type",
    "merchant_category",
    "location",
    "risk_score",
    "risk_level",
    "risk_reasons",
    "anomaly_flag"
]

st.dataframe(
    filtered_df[
        display_columns
    ].sort_values(
        by="risk_score",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)


# --------------------------------
# Transaction investigation details
# --------------------------------

st.subheader("Transaction Investigation")

if len(filtered_df) > 0:

    transaction_ids = (
        filtered_df["transaction_id"]
        .tolist()
    )

    selected_transaction = st.selectbox(
        "Select a transaction",
        transaction_ids
    )

    selected = df[
        df["transaction_id"] == selected_transaction
    ].iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Transaction Details")

        st.write(
            f"**Transaction ID:** "
            f"{selected['transaction_id']}"
        )

        st.write(
            f"**Customer ID:** "
            f"{selected['customer_id']}"
        )

        st.write(
            f"**Timestamp:** "
            f"{selected['timestamp']}"
        )

        st.write(
            f"**Amount:** "
            f"₹{selected['amount']:,.2f}"
        )

        st.write(
            f"**Transaction Type:** "
            f"{selected['transaction_type']}"
        )

        st.write(
            f"**Merchant Category:** "
            f"{selected['merchant_category']}"
        )

        st.write(
            f"**Location:** "
            f"{selected['location']}"
        )

    with col2:

        st.markdown("### Risk Assessment")

        st.metric(
            "Risk Score",
            selected["risk_score"]
        )

        st.write(
            f"**Risk Level:** "
            f"{selected['risk_level']}"
        )

        st.write(
            f"**Anomaly Score:** "
            f"{selected['anomaly_score']:.4f}"
        )

        st.write(
            f"**Anomaly Flag:** "
            f"{'Yes' if selected['anomaly_flag'] else 'No'}"
        )

        st.write(
            f"**Rules Triggered:** "
            f"{selected['risk_reasons'] or 'None'}"
        )

    st.markdown("### Score Breakdown")

    st.info(
        selected["score_breakdown"]
        if selected["score_breakdown"]
        else "No risk points assigned."
    )

    investigation_record = investigation_df[
        investigation_df["transaction_id"]
        == selected_transaction
    ]

    if not investigation_record.empty:

        record = investigation_record.iloc[0]

        st.markdown(
            "### Investigation Rationale"
        )

        st.write(
            record["investigation_rationale"]
        )

        st.markdown(
            "### Recommended Next Action"
        )

        st.warning(
            record["recommended_action"]
        )


# --------------------------------
# Export findings
# --------------------------------

st.subheader("Export Findings")

csv_data = investigation_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Investigation Findings CSV",
    data=csv_data,
    file_name="investigation_findings.csv",
    mime="text/csv"
)


# --------------------------------
# Footer
# --------------------------------

st.markdown("---")

st.caption(
    "Synthetic data only | Risk screening prototype | "
    "System-generated recommendations are not compliance decisions."
)