import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
data = pd.read_csv("test_data.csv")

# Ensure 'date' column is in datetime format
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data = data.dropna(subset=['date'])

# Add necessary columns
data['month'] = data['date'].dt.to_period('M').astype(str)
data['day_of_week'] = data['date'].dt.day_name()

# Sum of Price by Month with Trend Line
st.header("Sum of Price by Month with Trend Line")
monthly_price = data.groupby('month')['price'].sum().reset_index()
fig1 = px.area(monthly_price, x='month', y='price', title="Sum of Price by Month", labels={'price': 'Sum of Price', 'month': 'Month'})
fig1.add_traces(
    go.Scatter(x=monthly_price['month'], y=monthly_price['price'], mode='lines', name='Trend Line', line=dict(color='black', dash='dash'))
)
fig1.update_traces(line_color="#fbc536", fillcolor="#fbc536")
st.plotly_chart(fig1)

# Average Count of Menu by Day of Week
st.header("Average Count of Menu by Day of Week")
day_of_week_data = data.groupby('day_of_week')['menu'].count().reset_index()
day_of_week_data['menu'] /= len(data['date'].dt.date.unique())  # Average count per day
fig2 = px.area(day_of_week_data, x='day_of_week', y='menu', title="Average Count of Menu by Day of Week",
               labels={'menu': 'Count of Menu', 'day_of_week': 'Day Of Week'})
fig2.update_traces(line_color="#fbc536", fillcolor="#fbc536")
st.plotly_chart(fig2)
