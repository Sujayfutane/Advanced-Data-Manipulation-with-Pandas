import pandas as pd

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv("cleaned_data.csv")

print("Dataset loaded")
print("-" * 60)

# -----------------------------
# 2. Revenue Trend by Tenure (Months)
# -----------------------------
tenure_trend = (
    df.groupby("tenure")
      .agg(
          avg_monthly_revenue=("monthlycharges", "mean"),
          avg_total_revenue=("totalcharges", "mean"),
          customer_count=("customerid", "count")
      )
      .reset_index()
)

print("Revenue Trend by Tenure:")
print(tenure_trend.head(10))
print("-" * 60)

# -----------------------------
# 3. Best Revenue-Generating Customers
# -----------------------------
top_customers = (
    df.sort_values("totalcharges", ascending=False)
      .loc[:, ["customerid", "tenure", "monthlycharges", "totalcharges"]]
      .head(10)
)

print("Top 10 Revenue-Generating Customers:")
print(top_customers)
print("-" * 60)

# -----------------------------
# 4. Monthly Charges Distribution
# -----------------------------
monthly_charge_analysis = (
    df.groupby(pd.cut(df["monthlycharges"], bins=5))
      .agg(
          total_customers=("customerid", "count"),
          avg_tenure=("tenure", "mean"),
          avg_total_revenue=("totalcharges", "mean")
      )
      .reset_index()
)

print("Monthly Charges Distribution:")
print(monthly_charge_analysis)
print("-" * 60)

# -----------------------------
# 5. Save Outputs
# -----------------------------
tenure_trend.to_csv("sales_trend_by_tenure.csv", index=False)
top_customers.to_csv("top_revenue_customers.csv", index=False)
monthly_charge_analysis.to_csv("monthly_charge_distribution.csv", index=False)

print("✅ Sales Pattern Analysis completed successfully.")
