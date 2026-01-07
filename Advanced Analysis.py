import pandas as pd

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv("cleaned_data.csv")

print("Dataset loaded")
print("-" * 70)

# -----------------------------
# 2. Retention Rate Calculation
# -----------------------------
# Retained customers = Churn == "No"
total_customers = df["customerid"].nunique()
retained_customers = df[df["churn"] == "No"]["customerid"].nunique()

retention_rate = (retained_customers / total_customers) * 100

print(f"Customer Retention Rate: {retention_rate:.2f}%")
print("-" * 70)

# -----------------------------
# 3. Pivot Table: Contract vs Churn
# -----------------------------
contract_churn_pivot = pd.pivot_table(
    df,
    values="customerid",
    index="contract",
    columns="churn",
    aggfunc="count",
    fill_value=0
)

contract_churn_pivot["churn_rate_%"] = (
    contract_churn_pivot.get("Yes", 0) /
    contract_churn_pivot.sum(axis=1)
) * 100

print("Contract vs Churn Pivot Table:")
print(contract_churn_pivot)
print("-" * 70)

# -----------------------------
# 4. Pivot Table: Payment Method vs Revenue
# -----------------------------
payment_revenue_pivot = pd.pivot_table(
    df,
    values="totalcharges",
    index="paymentmethod",
    aggfunc=["mean", "sum"]
)

print("Payment Method vs Revenue:")
print(payment_revenue_pivot)
print("-" * 70)

# -----------------------------
# 5. Cross-Selling Opportunity Identification
# -----------------------------
# High tenure & high monthly charges → best cross-sell candidates
cross_sell_customers = df[
    (df["tenure"] > df["tenure"].median()) &
    (df["monthlycharges"] > df["monthlycharges"].median()) &
    (df["churn"] == "No")
][[
    "customerid",
    "tenure",
    "monthlycharges",
    "totalcharges",
    "contract",
    "paymentmethod"
]]

print("Top Cross-Selling Candidates:")
print(cross_sell_customers.head(10))
print("-" * 70)

# -----------------------------
# 6. Save Outputs
# -----------------------------
contract_churn_pivot.to_csv("contract_churn_pivot.csv")
payment_revenue_pivot.to_csv("payment_revenue_pivot.csv")
cross_sell_customers.to_csv("cross_sell_customers.csv", index=False)

print("✅ Advanced analysis completed successfully.")
