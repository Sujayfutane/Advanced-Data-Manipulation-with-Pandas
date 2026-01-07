import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("cleaned_data.csv")

# -----------------------------
# Clean churn column
# -----------------------------
df['churn'] = df['churn'].astype(str).str.strip().str.capitalize()  # normalize 'Yes'/'No'

# -----------------------------
# Initialize app
# -----------------------------
app = Dash(__name__)
app.title = "Telco Customer Analytics Dashboard"

# -----------------------------
# Layout
# -----------------------------
app.layout = html.Div(style={"fontFamily": "Arial, sans-serif", "padding": "20px", "backgroundColor": "#f4f4f4"}, children=[

    html.H1("📊 Telco Customer Analytics Dashboard", style={"textAlign": "center", "marginBottom": "30px"}),

    # Filters
    html.Div(style={"display": "flex", "gap": "20px", "marginBottom": "30px"}, children=[
        html.Div(style={"flex": "1"}, children=[
            html.Label("Select Contract Type"),
            dcc.Dropdown(
                options=[{"label": c, "value": c} for c in df["contract"].unique()] + [{"label":"All","value":"All"}],
                value="All",
                id="contract-filter",
                clearable=False
            )
        ]),
        html.Div(style={"flex": "2"}, children=[
            html.Label("Select Tenure Range"),
            dcc.RangeSlider(
                min=df["tenure"].min(),
                max=df["tenure"].max(),
                step=1,
                marks={0: "0", 12: "12", 24: "24", 36: "36", 48:"48", 60:"60", 72:"72"},
                value=[df["tenure"].min(), df["tenure"].max()],
                id="tenure-filter"
            )
        ])
    ]),

    # KPI cards
    html.Div(style={"display": "flex", "gap": "20px", "marginBottom": "30px"}, children=[
        html.Div(id="kpi-revenue", style={"flex": "1", "padding": "20px", "backgroundColor": "#e0f7fa", "borderRadius": "10px", "textAlign": "center", "boxShadow": "2px 2px 5px #aaa"}),
        html.Div(id="kpi-churn", style={"flex": "1", "padding": "20px", "backgroundColor": "#ffebee", "borderRadius": "10px", "textAlign": "center", "boxShadow": "2px 2px 5px #aaa"}),
        html.Div(id="kpi-customers", style={"flex": "1", "padding": "20px", "backgroundColor": "#fff3e0", "borderRadius": "10px", "textAlign": "center", "boxShadow": "2px 2px 5px #aaa"})
    ]),

    # Charts
    html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(3, 1fr)", "gap": "20px", "marginBottom": "20px"}, children=[
        dcc.Graph(id="churn-dist"),
        dcc.Graph(id="churn-contract"),
        dcc.Graph(id="revenue-tenure")
    ]),
    html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(2, 1fr)", "gap": "20px", "marginBottom": "20px"}, children=[
        dcc.Graph(id="monthly-hist"),
        dcc.Graph(id="scatter-cross")
    ]),

    # Insights
    html.Div(style={"padding": "20px", "backgroundColor": "#eceff1", "borderRadius": "10px", "boxShadow": "2px 2px 5px #aaa"}, children=[
        html.H4("Key Insights"),
        html.Ul([
            html.Li("Month-to-month contracts show higher churn"),
            html.Li("High tenure + high charges indicate cross-sell potential"),
            html.Li("Revenue generally increases with tenure")
        ])
    ])
])

# -----------------------------
# Callbacks
# -----------------------------
@app.callback(
    Output("kpi-revenue", "children"),
    Output("kpi-churn", "children"),
    Output("kpi-customers", "children"),
    Output("churn-dist", "figure"),
    Output("churn-contract", "figure"),
    Output("revenue-tenure", "figure"),
    Output("monthly-hist", "figure"),
    Output("scatter-cross", "figure"),
    Input("contract-filter", "value"),
    Input("tenure-filter", "value")
)
def update_dashboard(contract_value, tenure_range):
    # Filter dataframe
    dff = df.copy()
    if contract_value != "All":
        dff = dff[dff["contract"] == contract_value]
    dff = dff[(dff["tenure"] >= tenure_range[0]) & (dff["tenure"] <= tenure_range[1])]

    # KPIs
    total_revenue = (dff["monthlycharges"] * dff["tenure"]).sum()
    churn_rate = dff["churn"].value_counts(normalize=True).get("Yes", 0) * 100
    total_customers = len(dff)

    kpi_rev = html.Div([
        html.H5("💰 Total Revenue"),
        html.H2(f"₹{total_revenue:,.0f}")
    ])
    kpi_churn = html.Div([
        html.H5("📉 Churn Rate"),
        html.H2(f"{churn_rate:.2f}%")
    ])
    kpi_cust = html.Div([
        html.H5("👥 Total Customers"),
        html.H2(f"{total_customers}")
    ])

    # Churn distribution
    churn_counts = dff["churn"].value_counts().reset_index()
    churn_counts.columns = ["churn_status", "count"]
    fig_churn = px.bar(
        churn_counts, x="churn_status", y="count", text="count",
        color="churn_status", color_discrete_map={"Yes": "#F44336", "No": "#4CAF50"}
    )
    fig_churn.update_layout(showlegend=False, plot_bgcolor="#f4f4f4")

    # Churn by contract
    contract_churn = pd.crosstab(dff["contract"], dff["churn"]).reset_index()
    churn_categories = [col for col in contract_churn.columns if col != "contract"]
    contract_churn_long = contract_churn.melt(
        id_vars="contract", value_vars=churn_categories, var_name="churn_status", value_name="count"
    )
    fig_contract = px.bar(
        contract_churn_long, x="contract", y="count", color="churn_status", text="count",
        barmode="stack", color_discrete_map={"Yes": "#F44336", "No": "#4CAF50"}
    )
    fig_contract.update_layout(plot_bgcolor="#f4f4f4")

    # Avg monthly charges by tenure
    tenure_avg = dff.groupby("tenure")["monthlycharges"].mean().reset_index()
    fig_revenue = px.line(tenure_avg, x="tenure", y="monthlycharges",
                          labels={"tenure": "Tenure (Months)", "monthlycharges": "Avg Monthly Charges"},
                          line_shape="spline")
    fig_revenue.update_traces(line=dict(color="#2196F3"))
    fig_revenue.update_layout(plot_bgcolor="#f4f4f4")

    # Monthly charges histogram
    fig_hist = px.histogram(dff, x="monthlycharges", nbins=20,
                            labels={"monthlycharges": "Monthly Charges"},
                            color_discrete_sequence=["#9C27B0"])
    fig_hist.update_layout(plot_bgcolor="#f4f4f4")

    # Cross-selling scatter
    fig_scatter = px.scatter(dff, x="tenure", y="monthlycharges",
                             labels={"tenure": "Tenure (Months)", "monthlycharges": "Monthly Charges"},
                             opacity=0.6, color_discrete_sequence=["#FF9800"],
                             hover_data=["contract", "churn"])
    fig_scatter.update_layout(plot_bgcolor="#f4f4f4")

    return kpi_rev, kpi_churn, kpi_cust, fig_churn, fig_contract, fig_revenue, fig_hist, fig_scatter

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
