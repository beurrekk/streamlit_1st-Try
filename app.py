import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
data = pd.read_csv("test_data.csv")

# Ensure date format and extract month
data['Date'] = pd.to_datetime(data['Date'])
data['Month'] = data['Date'].dt.to_period('M').astype(str)  # Format YYYY-MM

# Chart 1: Sum of Price by Month with Trend Line
monthly_price = data.groupby('Month')['Price'].sum().reset_index()
fig1 = px.area(monthly_price, x='Month', y='Price', title="Sum of Price by Month",
               labels={'Price': 'Sum of Price', 'Month': 'Month'})
fig1.add_traces(
    go.Scatter(x=monthly_price['Month'], y=monthly_price['Price'], mode='lines', name='Trend Line',
               line=dict(color='black', dash='dash'))
)
fig1.update_traces(line_color="#fbc536", fillcolor="#fbc536")

# Chart 2: Average Count of Menu by Day Of Week
day_of_week_data = data.groupby('Day Of Week')['Menu'].count().reset_index()
day_of_week_data['Menu'] = day_of_week_data['Menu'] / len(data['Month'].unique())  # Average by month
fig2 = px.area(day_of_week_data, x='Day Of Week', y='Menu', title="Average Count of Menu by Day Of Week",
               labels={'Menu': 'Count of Menu', 'Day Of Week': 'Day Of Week'})
fig2.update_traces(line_color="#fbc536", fillcolor="#fbc536")

# Streamlit Dashboard
st.title("Dashboard: Restaurant Insights")
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
