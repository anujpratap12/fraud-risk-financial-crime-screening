# Fraud Risk & Transaction Anomaly Investigation System

A Python-based transaction risk screening project that analyzes synthetic banking transactions, identifies unusual patterns, and prioritizes transactions for review.

The system combines data validation, transaction behaviour analysis, rule-based risk detection, Isolation Forest anomaly detection, explainable risk scoring, and an investigation workflow with a Streamlit dashboard.

> **Note:** This project uses synthetic transaction data and is intended as a risk-screening prototype. It does not represent a production fraud detection or compliance system.

---

## Key Features

- Synthetic banking transaction data generation
- Data quality and validation checks
- Transaction behaviour feature engineering
- Rule-based risk detection
- Isolation Forest anomaly detection
- Explainable risk scoring
- Investigation queue for medium and high-risk transactions
- Investigation rationale and recommended review actions
- Streamlit dashboard for transaction review
- Automated testing with pytest

---

## Project Workflow

The system processes transactions through the following pipeline:

**Transaction Data → Validation → Feature Engineering → Risk Rules → Isolation Forest → Risk Score → Investigation Queue**

### 1. Data Generation

The project generates a synthetic banking transaction dataset containing:

- Transaction IDs
- Customer IDs
- Transaction timestamps
- Transaction amounts
- Transaction types
- Merchant categories
- Locations
- Account age

The dataset contains **3,000 transactions across 500 synthetic customers**.

Suspicious transaction scenarios are also injected into the synthetic dataset to demonstrate the screening workflow.

### 2. Data Validation

The generated transaction data is checked for:

- Missing values
- Duplicate transaction IDs
- Invalid transaction amounts
- Invalid timestamps
- Invalid transaction types
- Invalid merchant categories
- Invalid locations

### 3. Feature Engineering

The system creates transaction behaviour features including:

- Customer average transaction amount
- Amount deviation from customer average
- Time since previous transaction
- Transactions within the last 10 minutes
- Transactions within the last hour
- Transaction velocity
- Location changes
- Customer transaction count

### 4. Risk Detection

The system combines rule-based checks with machine-learning anomaly detection to identify unusual transactions.

### 5. Risk Scoring

The detected signals are combined into an explainable risk score.

### 6. Investigation Queue

Medium and high-risk transactions are added to an investigation queue with:

- Triggered risk signals
- Risk score
- Risk level
- Investigation rationale
- Recommended review action

---

## Risk Detection

The system uses two complementary approaches:

1. Rule-based risk detection
2. Machine-learning anomaly detection

### Rule-Based Checks

The following transaction patterns are used as risk signals:

| Risk Signal | Condition | Points |
|---|---|---:|
| High Amount | Transaction amount ≥ ₹30,000 | +25 |
| High Amount Deviation | Amount ≥ 5× customer average | +20 |
| High Velocity | 3+ transactions within 10 minutes | +20 |
| Rapid Location Change | Location changes within 60 minutes | +15 |
| ML Anomaly | Isolation Forest anomaly | +20 |

These thresholds and weights are project-defined assumptions for demonstrating transaction risk screening.

### Anomaly Detection

The project uses **Isolation Forest** to identify transactions that appear unusual based on transaction behaviour.

The model considers features such as:

- Transaction amount
- Amount deviation
- Recent transaction frequency
- Time between transactions
- Account age
- Recent transaction activity

The Isolation Forest result is used as an additional risk signal rather than proof that a transaction is fraudulent.

The model is configured with a **5% contamination parameter** for this prototype.

> The anomaly rate should not be interpreted as a real-world fraud rate.

---

## Risk Scoring

The system combines rule-based signals and the Isolation Forest result into an explainable score.

| Signal | Points |
|---|---:|
| High Amount | +25 |
| High Amount Deviation | +20 |
| High Velocity | +20 |
| Rapid Location Change | +15 |
| ML Anomaly | +20 |

### Risk Levels

| Risk Level | Score |
|---|---:|
| LOW | 0–29 |
| MEDIUM | 30–59 |
| HIGH | 60–100 |

The score is a project-defined prioritization mechanism and should not be interpreted as a probability of fraud.

---

## Investigation Workflow

Transactions classified as **MEDIUM** or **HIGH** risk are added to the investigation queue.

For each transaction, the system records:

- Transaction ID
- Customer ID
- Timestamp
- Transaction amount
- Transaction type
- Merchant category
- Location
- Previous location
- Customer average amount
- Amount deviation
- Recent transaction activity
- Risk signals
- Isolation Forest anomaly score
- Final risk score
- Risk level
- Score breakdown
- Investigation rationale
- Recommended action

### Example Review Actions

- **HIGH:** Escalate for detailed review
- **MEDIUM:** Request additional verification
- **LOW:** Close / no further action

These are prototype recommendations and are not compliance decisions.

---

## Results

The current implementation produces the following results:

| Metric | Result |
|---|---:|
| Synthetic transactions processed | 3,000 |
| Synthetic customers | 500 |
| Isolation Forest anomalies | 150 |
| Transactions requiring review | 123 |
| MEDIUM-risk transactions | 103 |
| HIGH-risk transactions | 20 |
| Automated tests | 14/14 passed |

The investigation findings are saved to:

```text
reports/investigation_findings.csv
