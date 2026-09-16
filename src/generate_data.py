import numpy as np
import pandas as pd
from pathlib import Path


# Reproducibility: the same seed produces the same dataset
np.random.seed(42)


# -----------------------------
# Configuration
# -----------------------------

NUM_TRANSACTIONS = 3000
NUM_CUSTOMERS = 500

TRANSACTION_TYPES = [
    "UPI",
    "CARD",
    "BANK_TRANSFER",
    "ATM"
]

MERCHANT_CATEGORIES = [
    "Grocery",
    "Restaurant",
    "Pharmacy",
    "Electronics",
    "Travel",
    "Utilities",
    "Online Shopping"
]

LOCATIONS = [
    "Delhi",
    "Mumbai",
    "Bengaluru",
    "Hyderabad",
    "Pune",
    "Jaipur",
    "Chandigarh",
    "Dehradun"
]


# -----------------------------
# Generate customers
# -----------------------------

customer_ids = [
    f"C{i:04d}"
    for i in range(1, NUM_CUSTOMERS + 1)
]

customer_account_age = {
    customer_id: np.random.randint(30, 3650)
    for customer_id in customer_ids
}


# -----------------------------
# Generate normal transactions
# -----------------------------

transaction_ids = [
    f"TX{i:05d}"
    for i in range(1, NUM_TRANSACTIONS + 1)
]

transaction_customer_ids = np.random.choice(
    customer_ids,
    size=NUM_TRANSACTIONS
)

timestamps = pd.to_datetime(
    np.random.choice(
        pd.date_range(
            start="2026-01-01",
            end="2026-06-30",
            freq="min"
        ),
        size=NUM_TRANSACTIONS,
        replace=False
    )
)

amounts = np.round(
    np.random.lognormal(
        mean=7.0,
        sigma=0.8,
        size=NUM_TRANSACTIONS
    ),
    2
)

transaction_types = np.random.choice(
    TRANSACTION_TYPES,
    size=NUM_TRANSACTIONS
)

merchant_categories = np.random.choice(
    MERCHANT_CATEGORIES,
    size=NUM_TRANSACTIONS
)

locations = np.random.choice(
    LOCATIONS,
    size=NUM_TRANSACTIONS
)

account_age_days = [
    customer_account_age[customer_id]
    for customer_id in transaction_customer_ids
]


transactions = pd.DataFrame({
    "transaction_id": transaction_ids,
    "customer_id": transaction_customer_ids,
    "timestamp": timestamps,
    "amount": amounts,
    "transaction_type": transaction_types,
    "merchant_category": merchant_categories,
    "location": locations,
    "account_age_days": account_age_days
})


# Sort chronologically
transactions = transactions.sort_values(
    by="timestamp"
).reset_index(drop=True)


# -----------------------------
# Insert synthetic suspicious scenarios
# -----------------------------

# Scenario 1:
# Unusually large transactions
high_amount_indices = np.random.choice(
    transactions.index,
    size=30,
    replace=False
)

transactions.loc[
    high_amount_indices,
    "amount"
] = np.round(
    np.random.uniform(30000, 100000, size=30),
    2
)


# Scenario 2:
# High transaction velocity
velocity_indices = np.random.choice(
    transactions.index,
    size=40,
    replace=False
)

for index in velocity_indices:
    customer_id = transactions.loc[index, "customer_id"]

    customer_rows = transactions[
        transactions["customer_id"] == customer_id
    ].index

    if len(customer_rows) >= 3:
        selected_rows = np.random.choice(
            customer_rows,
            size=min(3, len(customer_rows)),
            replace=False
        )

        base_time = transactions.loc[index, "timestamp"]

        for offset, row in enumerate(selected_rows):
            transactions.loc[
                row, "timestamp"
            ] = base_time + pd.Timedelta(
                minutes=offset * 3
            )


# Scenario 3:
# Location changes
location_change_indices = np.random.choice(
    transactions.index,
    size=30,
    replace=False
)

for index in location_change_indices:
    customer_id = transactions.loc[index, "customer_id"]

    customer_rows = transactions[
        transactions["customer_id"] == customer_id
    ].index

    if len(customer_rows) >= 2:
        previous_row = customer_rows[
            max(0, list(customer_rows).index(index) - 1)
        ]

        current_location = transactions.loc[
            previous_row, "location"
        ]

        different_locations = [
            location
            for location in LOCATIONS
            if location != current_location
        ]

        transactions.loc[
            index, "location"
        ] = np.random.choice(different_locations)


# -----------------------------
# Add historical behavior fields
# -----------------------------

customer_avg_amount = (
    transactions
    .groupby("customer_id")["amount"]
    .transform("mean")
)

customer_transaction_count = (
    transactions
    .groupby("customer_id")["transaction_id"]
    .transform("count")
)

transactions["customer_avg_amount"] = np.round(
    customer_avg_amount,
    2
)

transactions["customer_transaction_count"] = (
    customer_transaction_count
)


# -----------------------------
# Save dataset
# -----------------------------

output_path = Path(
    "data/raw/transactions.csv"
)

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

transactions.to_csv(
    output_path,
    index=False
)


# -----------------------------
# Display summary
# -----------------------------

print("Synthetic transaction dataset created successfully.")
print(f"Total transactions: {len(transactions)}")
print(f"Total customers: {transactions['customer_id'].nunique()}")
print(f"Saved to: {output_path}")

print("\nDataset columns:")
print(list(transactions.columns))

print("\nFirst 5 records:")
print(transactions.head())