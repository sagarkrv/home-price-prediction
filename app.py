import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Sample Data (Replace this with actual data)
expanded_features_data = {
    "Home Site": [1, 2, 3, 4, 99, 100, 93, 94, 95, 16],
    "Square Footage": [2556, 2434, 2434, 2434, 3008, 3008, 3008, 3008, 3008, 3008],
    "Exceptionally Priced": [849038, 809995, 834995, 824901, 884995, 889995, 1035791, 999995, 1036648, 956398],
    "Delivery Date Encoded": [3, 3, 4, 4, 5, 6, 7, 7, 7, 2],
    "Bedrooms_4": [1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    "Predicted Price": [845000, 810000, 835000, 825000, 880000, 890000, 1030000, 998000, 1035000, 955000]
}

# Convert to DataFrame
df = pd.DataFrame(expanded_features_data)

# Create a Plotly scatter plot
fig = go.Figure()

# Add actual vs predicted points
fig.add_trace(go.Scatter(
    x=df["Exceptionally Priced"],
    y=df["Predicted Price"],
    mode='markers',
    marker=dict(color='blue', size=8, opacity=0.7),
    name="Predicted vs Actual"
))

# Add perfect fit line (where predicted = actual)
fig.add_trace(go.Scatter(
    x=[df["Exceptionally Priced"].min(), df["Exceptionally Priced"].max()],
    y=[df["Exceptionally Priced"].min(), df["Exceptionally Priced"].max()],
    mode='lines',
    line=dict(color='black', dash='dash'),
    name="Perfect Fit Line"
))

# Add interactive annotations (Home Site, Bedrooms, Sq Ft, Delivery)
for i, row in df.iterrows():
    home_site = row["Home Site"]
    bedrooms = "4BR" if row["Bedrooms_4"] == 1 else "3BR"
    sq_ft = row["Square Footage"]
    delivery_month = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"][row["Delivery Date Encoded"] - 1]
    label = f"{home_site} ({bedrooms}, {sq_ft}sqft, {delivery_month})"
    
    fig.add_annotation(
        x=row["Exceptionally Priced"],
        y=row["Predicted Price"],
        text=label,
        showarrow=True,
        arrowhead=2,
        ax=40 if i % 2 == 0 else -40,
        ay=40 if i % 3 == 0 else -40,
        font=dict(size=10, color="red")
    )

# Format axes
fig.update_layout(
    title="Interactive Predicted vs Actual Prices",
    xaxis=dict(title="Actual Prices ($)", tickformat=",", showgrid=True),
    yaxis=dict(title="Predicted Prices ($)", tickformat=",", showgrid=True),
    template="plotly_white",
    legend=dict(x=0.02, y=0.98)
)

# Streamlit UI
st.title("Interactive Home Price Prediction Chart")
st.write("Move labels by clicking on them in the interactive chart.")
st.plotly_chart(fig, use_container_width=True)
