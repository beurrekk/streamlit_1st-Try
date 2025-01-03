import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
file_path = r'C:\Users\user\OneDrive\Desktop\.SPNK\Project\data\test_data.csv'
data = pd.read_csv(file_path)

# Data Preparation
chart_data = (
    data.groupby(['Drinks Staff', 'Category'])
    .size()
    .reset_index(name='Total Orders')
)

# Streamlit App
st.title("Total Orders by Drinks Staff and Category")

# Create the Bar Chart using Plotly
fig = px.bar(
    chart_data,
    x="Drinks Staff",
    y="Total Orders",
    color="Category",
    barmode="group",
    labels={"Drinks Staff": "Number of Drinks Staff", "Total Orders": "Total Orders", "Category": "Category"},
    title="Total Orders by Drinks Staff and Category",
    color_discrete_map={"drink": "#636efb", "food": "#ef553b"}  # Custom colors
)

# Update layout for y-axis range
fig.update_layout(
    yaxis=dict(
        tickvals=[2000, 4000, 6000],  # Custom tick range
        range=[0, 7000]  # Ensure the full range is visible
    )
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)
