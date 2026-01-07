# Telco Customer Analytics Dashboard

An **interactive dashboard** for analyzing Telco customer data, visualizing churn trends, revenue patterns, and cross-selling opportunities.  
Built using **Python, Dash, and Plotly**, the dashboard allows real-time exploration of key metrics and insights.

---

## **Table of Contents**

- [Project Overview](#project-overview)
- [Features](#features)
- [Data Description](#data-description)
- [Installation](#installation)
- [Usage](#usage)
- [Dashboard Layout](#dashboard-layout)
- [Insights & Recommendations](#insights--recommendations)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## **Project Overview**

This project analyzes Telco customer data to:

- Identify **customer churn patterns**
- Calculate **key performance indicators (KPIs)**
- Highlight **high-value and at-risk customer segments**
- Suggest **business recommendations for retention and cross-selling**

The result is a **live, interactive dashboard** where stakeholders can explore trends dynamically.

---

## **Features**

- ✅ **Interactive Filters**: Contract type, tenure range  
- ✅ **KPIs**: Total Revenue, Churn Rate, Total Customers  
- ✅ **Charts**:
  - Churn Distribution  
  - Churn by Contract Type  
  - Average Monthly Charges by Tenure  
  - Monthly Charges Distribution  
  - Cross-Selling Scatter Plot  
- ✅ **Insights Panel**: Key business observations  
- ✅ **Responsive Layout**: Grid-based and visually appealing

---

## **Data Description**

**Dataset:** `cleaned_data.csv` (cleaned Telco dataset)  

| Column | Description |
|--------|-------------|
| customerID | Unique customer identifier |
| contract | Contract type (Month-to-month, One-year, Two-year) |
| tenure | Number of months the customer has stayed |
| monthlycharges | Monthly billing amount |
| churn | Customer churn status (Yes/No) |

---

## **Installation**

1. Clone the repository:

```bash
git clone https://github.com/your-username/telco-dashboard.git
cd telco-dashboard
****
