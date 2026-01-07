import pandas as pd

# -----------------------------
# 1. Load Dataset
# -----------------------------
# Replace with your file path
file_path = "customer_churn.csv"   # e.g., "data/cancer_data.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("-" * 50)

# -----------------------------
# 2. Basic Exploration
# -----------------------------
print("First 5 rows:")
print(df.head())
print("-" * 50)

print("Last 5 rows:")
print(df.tail())
print("-" * 50)

print("Dataset shape (rows, columns):")
print(df.shape)
print("-" * 50)

# -----------------------------
# 3. Dataset Structure
# -----------------------------
print("Dataset info:")
df.info()
print("-" * 50)

print("Column names:")
print(df.columns.tolist())
print("-" * 50)

# -----------------------------
# 4. Statistical Summary
# -----------------------------
print("Statistical summary (numerical columns):")
print(df.describe())
print("-" * 50)

# -----------------------------
# 5. Missing Values Analysis
# -----------------------------
missing_values = df.isnull().sum()
missing_percent = (missing_values / len(df)) * 100

missing_df = pd.DataFrame({
    "Missing Values": missing_values,
    "Percentage (%)": missing_percent.round(2)
})

print("Missing values summary:")
print(missing_df[missing_df["Missing Values"] > 0])
print("-" * 50)

# -----------------------------
# 6. Duplicate Check
# -----------------------------
duplicate_rows = df.duplicated().sum()
print(f"Number of duplicate rows: {duplicate_rows}")
print("-" * 50)
