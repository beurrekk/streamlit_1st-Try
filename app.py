import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
data = pd.read_csv("test_data.csv")

# Ensure date columns are in datetime format
data['Date'] = pd.to_datetime(data['Date'])
data['Order Time'] = pd.to_datetime(data['Order Time'])
data['Serve Time'] = pd.to_datetime(data['Serve Time'])

# Extract additional information for charts
data['Month'] = data['Date'].dt.to_period('M').astype(str)  # Month-Year
data['Waiting Time'] = (data['Serve Time'] - data['Order Time']).dt.total_seconds() / 60  # In minutes

# 1. Line chart with area: Sum of price by month (Add trend line)
monthly_price = data.groupby('Month')['Price'].sum().reset_index()
fig1 = px.area(monthly_price, x='Month', y='Price', title="Sum of Price by Month",
               labels={'Price': 'Sum of Price', 'Month': 'Month'})
fig1.add_traces(
    go.Scatter(x=monthly_price['Month'], y=monthly_price['Price'], mode='lines', name='Trend Line',
               line=dict(color='black', dash='dash'))
)
fig1.update_traces(line_color="#fbc536", fillcolor="#fbc536")

# 2. Line chart with area: Average count of menu by day (Day Of Week)
day_of_week_data = data.groupby('Day Of Week')['Menu'].count().reset_index()
day_of_week_data['Menu'] = day_of_week_data['Menu'] / len(data['Month'].unique())  # Average by month
fig2 = px.area(day_of_week_data, x='Day Of Week', y='Menu', title="Average Count of Menu by Day Of Week",
               labels={'Menu': 'Count of Menu', 'Day Of Week': 'Day Of Week'})
fig2.update_traces(line_color="#fbc536", fillcolor="#fbc536")

# 3. Bar chart: Top 4 popular food items
top_food = data[data['Category'] == 'food'].groupby('Menu')['Menu'].count().nlargest(4).reset_index(name='Count')
fig3 = px.bar(top_food, x='Menu', y='Count', title="Top 4 Popular Food Items",
              labels={'Menu': 'Food Menu', 'Count': 'Count'}, color_discrete_sequence=["#636efb"])

# 4. Bar chart: Top 4 popular drink items
top_drink = data[data['Category'] == 'drink'].groupby('Menu')['Menu'].count().nlargest(4).reset_index(name='Count')
fig4 = px.bar(top_drink, x='Menu', y='Count', title="Top 4 Popular Drink Items",
              labels={'Menu': 'Drink Menu', 'Count': 'Count'}, color_discrete_sequence=["#ef553b"])

# 5. Line chart with area: Quantity of all menu by month
monthly_quantity = data.groupby('Month')['Menu'].count().reset_index()
fig5 = px.area(monthly_quantity, x='Month', y='Menu', title="Quantity of All Menu by Month",
               labels={'Menu': 'Quantity', 'Month': 'Month'})
fig5.update_traces(line_color="#fbc536", fillcolor="#fbc536")

# 6. Line chart with area: Average waiting time by kitchen staff count
staff_waiting = data.groupby('Kitchen Staff')['Waiting Time'].mean().reset_index()
fig6 = px.area(staff_waiting, x='Kitchen Staff', y='Waiting Time', title="Average Waiting Time by Kitchen Staff Count",
               labels={'Kitchen Staff': 'Kitchen Staff Count', 'Waiting Time': 'Average Waiting Time (minutes)'})
fig6.update_traces(line_color="#fbc536", fillcolor="#fbc536")

# Streamlit Dashboard
st.title("Restaurant Dashboard")
st.write("This dashboard provides insights into sales and operational performance.")

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)
st.plotly_chart(fig4, use_container_width=True)
st.plotly_chart(fig5, use_container_width=True)
st.plotly_chart(fig6, use_container_width=True)
