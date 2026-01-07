import pandas as pd
import numpy as np

# -----------------------------
# 1. Load Dataset
# -----------------------------
file_path = "customer_churn.csv"   # update path
df = pd.read_csv(file_path)

print("Initial shape:", df.shape)

# -----------------------------
# 2. Standardize Column Names
# -----------------------------
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
)

print("Standardized column names.")

# -----------------------------
# 3. Remove Duplicate Rows
# -----------------------------
duplicates_before = df.duplicated().sum()
df = df.drop_duplicates()
print(f"Duplicates removed: {duplicates_before}")

# -----------------------------
# 4. Handle Missing Values
# -----------------------------
# Separate numeric and categorical columns
num_cols = df.select_dtypes(include=["int64", "float64"]).columns
cat_cols = df.select_dtypes(include=["object", "category"]).columns

# Fill numeric missing values with median
for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

# Fill categorical missing values with mode
for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

print("Missing values handled.")

# -----------------------------
# 5. Data Type Corrections
# -----------------------------
# Example: convert date columns (edit as needed)
date_columns = [col for col in df.columns if "date" in col]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

print("Date columns converted.")

# -----------------------------
# 6. Outlier Treatment (IQR Method)
# -----------------------------
def remove_outliers_iqr(data, columns):
    for col in columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        data = data[(data[col] >= lower) & (data[col] <= upper)]
    return data

df = remove_outliers_iqr(df, num_cols)
print("Outliers removed using IQR method.")

# -----------------------------
# 7. Feature Engineering (Examples)
# -----------------------------
# Example: create log-transformed feature
for col in num_cols:
    if (df[col] > 0).all():
        df[f"log_{col}"] = np.log(df[col])

print("Feature engineering completed.")

# -----------------------------
# 8. Final Dataset Check
# -----------------------------
print("Final shape:", df.shape)
print("Remaining missing values:\n", df.isnull().sum().sum())

# -----------------------------
# 9. Save Cleaned Dataset
# -----------------------------
output_path = "cleaned_data.csv"
df.to_csv(output_path, index=False)

print(f"Cleaned dataset saved to {output_path}")
