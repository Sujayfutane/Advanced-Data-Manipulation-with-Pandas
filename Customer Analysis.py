import pandas as pd

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv("cleaned_data.csv")

print("Dataset loaded successfully")
print("-" * 60)

# -----------------------------
# 2. Top Customers (by Total Charges)
# -----------------------------
top_customers = (
    df.groupby("customerid")["totalcharges"]
      .sum()
      .sort_values(ascending=False)
      .reset_index()
)

top_customers.columns = ["customer_id", "total_revenue"]

print("Top 10 Customers by Total Revenue:")
print(top_customers.head(10))
print("-" * 60)

# -----------------------------
# 3. Customer Lifetime Value (CLV)
# -----------------------------
# In Telco data, CLV ≈ Total Charges
customer_clv = df[[
    "customerid",
    "tenure",
    "monthlycharges",
    "totalcharges"
]].copy()

customer_clv["clv"] = customer_clv["totalcharges"]

print("Top 10 Customers by CLV:")
print(
    customer_clv
    .sort_values("clv", ascending=False)
    .head(10)
)
print("-" * 60)

# -----------------------------
# 4. Customer Distribution Analysis
# -----------------------------
# By Contract Type
contract_distribution = (
    df.groupby("contract")
      .agg(
          total_customers=("customerid", "nunique"),
          avg_clv=("totalcharges", "mean"),
          churn_rate=("churn", lambda x: (x == "Yes").mean() * 100)
      )
      .reset_index()
)

print("Customer Distribution by Contract Type:")
print(contract_distribution)
print("-" * 60)

# By Payment Method
payment_distribution = (
    df.groupby("paymentmethod")
      .agg(
          total_customers=("customerid", "nunique"),
          avg_clv=("totalcharges", "mean")
      )
      .reset_index()
)

print("Customer Distribution by Payment Method:")
print(payment_distribution)
print("-" * 60)

# -----------------------------
# 5. Save Results
# -----------------------------
top_customers.to_csv("top_customers.csv", index=False)
customer_clv.to_csv("customer_lifetime_value.csv", index=False)
contract_distribution.to_csv("contract_analysis.csv", index=False)
payment_distribution.to_csv("payment_method_analysis.csv", index=False)

print("✅ Customer Analysis completed successfully.")
