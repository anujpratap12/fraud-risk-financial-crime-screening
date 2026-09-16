# Fraud Risk & Transaction Anomaly Investigation System

A Python-based project that analyzes synthetic banking transactions to identify unusual patterns and prioritize transactions for review.

The system combines data validation, rule-based checks, Isolation Forest anomaly detection, risk scoring, and an investigation workflow with a Streamlit dashboard.

## Key Features

- Synthetic banking transaction data generation
- Data quality and validation checks
- Transaction behaviour feature engineering
- Rule-based risk detection
- Isolation Forest anomaly detection
- Explainable risk scoring
- Investigation queue for medium and high-risk transactions
- Streamlit dashboard for reviewing flagged transactions
- Automated testing with pytest

## How It Works

The project processes the transactions in a few stages:

**Transaction Data → Validation → Feature Engineering → Risk Rules → Isolation Forest → Risk Score → Investigation Queue**

First, the generated transaction data is checked for missing values, duplicates, invalid amounts, timestamps, and invalid categories.

Next, transaction behaviour features are created, such as transaction frequency, time since the previous transaction, amount deviation, and location changes.

The system then applies rule-based checks and Isolation Forest to identify unusual transactions. These results are combined into a risk score.

Medium and high-risk transactions are added to the investigation queue along with the reasons they were flagged and a suggested next action.

## Risk Detection

The system uses two approaches to identify unusual transactions.

### Rule-based checks

The following conditions are checked:

- Transaction amount is ₹30,000 or higher
- Transaction amount is at least 5x the customer's average
- 3 or more transactions occur within 10 minutes
- Transaction location changes within 60 minutes

### Anomaly Detection

Isolation Forest is used to identify transactions that look unusual based on transaction amount, transaction frequency, time between transactions, account age, and other transaction behaviour features.

The model is used as an additional signal rather than treating an anomaly as proof of fraud.

### Risk Score

The rule-based signals and the Isolation Forest result are combined into a score from 0 to 100.

| Signal | Points |
|---|---:|
| High amount | +25 |
| High amount deviation | +20 |
| High velocity | +20 |
| Rapid location change | +15 |
| ML anomaly | +20 |

Risk levels:

- **LOW:** 0–29
- **MEDIUM:** 30–59
- **HIGH:** 60–100

## Investigation Output

Transactions with a MEDIUM or HIGH risk level are added to the investigation queue.

For each transaction, the system stores:

- Transaction details
- Risk signals that were triggered
- Isolation Forest anomaly score
- Final risk score
- Risk level
- Explanation for the risk
- Suggested review action

The system currently produces:

- 3,000 transactions processed
- 150 transactions identified as anomalies by Isolation Forest
- 123 transactions requiring review
- 103 MEDIUM-risk transactions
- 20 HIGH-risk transactions

The investigation findings are saved to:

`reports/investigation_findings.csv`

## Testing

The project includes automated tests using pytest.

The tests cover:

- Dataset size and integrity
- Missing values and validation
- Invalid transaction values
- Risk detection rules
- Risk scoring
- Normal transactions without risk signals

Current test result:

```text
14 tests passed
0 tests failed