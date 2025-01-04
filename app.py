import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
data_file = 'test_data.csv'
df = pd.read_csv(data_file)

# Preprocessing
df['Order Time'] = pd.to_datetime(df['Order Time'])
df['Serve Time'] = pd.to_datetime(df['Serve Time'])
df['Month'] = df['Order Time'].dt.to_period('M').astype(str)
df['Day Of Week'] = pd.Categorical(
    df['Day Of Week'],
    categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    ordered=True
)
df['Waiting Time'] = (df['Serve Time'] - df['Order Time']).dt.total_seconds()

# Header
st.title("Restaurant Dashboard")

# -------------------- Overall Section -------------------- #
st.header("Overall")
col1, col2 = st.columns(2)

# Chart 1: Line chart with area (Sum of Price by Month with Trend Line)
price_by_month = df.groupby('Month')['Price'].sum().reset_index()
fig1 = px.area(price_by_month, x='Month', y='Price', title="Sum of Price by Month", range_y=[0, 4000])
fig1.add_traces(go.Scatter(x=price_by_month['Month'], y=price_by_month['Price'], mode='lines', name='Trend Line'))
col1.plotly_chart(fig1, use_container_width=True)

# Chart 2: Line chart with area (Average Count of Menu by Day of Week)
menu_by_day = df.groupby('Day Of Week')['Menu'].count().reset_index(name='Menu Count')
fig2 = px.area(menu_by_day, x='Day Of Week', y='Menu Count', title="Avg Count of Menu by Day of Week", range_y=[0, 2000])
col2.plotly_chart(fig2, use_container_width=True)

# -------------------- Popular Menu Section -------------------- #
st.header("Popular Menu")
col3, col4 = st.columns(2)

# Chart 3: Bar chart (Top 4 Popular Food Categories)
top_food = df[df['Category'] == 'food'].groupby('Menu').size().nlargest(4).reset_index(name='Count')
fig3 = px.bar(top_food, x='Menu', y='Count', title="Top 4 Popular Food Categories", range_y=[0, 1000])
col3.plotly_chart(fig3, use_container_width=True)

# Chart 4: Bar chart (Top 4 Popular Drink Categories)
top_drink = df[df['Category'] == 'drink'].groupby('Menu').size().nlargest(4).reset_index(name='Count')
fig4 = px.bar(top_drink, x='Menu', y='Count', title="Top 4 Popular Drink Categories", range_y=[0, 700])
col4.plotly_chart(fig4, use_container_width=True)

# -------------------- Waiting Time - Food Section -------------------- #
st.header("Waiting Time - Food")
col5, col6 = st.columns(2)

# Chart 5: Line chart with area (Quantity of All Menus by Month)
menu_quantity_by_month = df.groupby('Month')['Menu'].count().reset_index(name='Menu Quantity')
fig5 = px.area(menu_quantity_by_month, x='Month', y='Menu Quantity', title="Quantity of All Menus by Month")
col5.plotly_chart(fig5, use_container_width=True)

# Chart 6: Line chart with area (Avg Waiting Time vs. Kitchen Staff)
avg_wait_time_by_staff = df.groupby('Kitchen Staff')['Waiting Time'].mean().reset_index(name='Avg Waiting Time')
fig6 = px.area(avg_wait_time_by_staff, x='Kitchen Staff', y='Avg Waiting Time', title="Avg Waiting Time vs. Kitchen Staff")
col6.plotly_chart(fig6, use_container_width=True)

# -------------------- Waiting Time - Food Continued -------------------- #
st.header("Waiting Time - Food Continued")
col7, col8 = st.columns(2)

# Chart 7: Line chart without area (Avg Waiting Time by Month)
avg_wait_time_by_month = df.groupby('Month')['Waiting Time'].mean().reset_index(name='Avg Waiting Time')
fig7 = px.line(avg_wait_time_by_month, x='Month', y='Avg Waiting Time', title="Avg Waiting Time by Month")
col7.plotly_chart(fig7, use_container_width=True)

# Chart 8: Line chart without area (Count of Menu and Kitchen Staff by Day of Week)
menu_and_staff_by_day = df.groupby('Day Of Week').agg({'Menu': 'count', 'Kitchen Staff': 'mean'}).reset_index()
fig8 = go.Figure()
fig8.add_trace(go.Scatter(x=menu_and_staff_by_day['Day Of Week'], y=menu_and_staff_by_day['Menu'], mode='lines+markers', name='Menu Count'))
fig8.add_trace(go.Scatter(x=menu_and_staff_by_day['Day Of Week'], y=menu_and_staff_by_day['Kitchen Staff'], mode='lines+markers', name='Kitchen Staff'))
fig8.update_layout(title="Menu Count and Kitchen Staff by Day of Week", xaxis_title="Day of Week")
col8.plotly_chart(fig8, use_container_width=True)

# -------------------- Waiting Time - Drink Section -------------------- #
st.header("Waiting Time - Drink")

# Chart 9: Line chart without area (Quantity of Drink Menus by Month)
drink_data = df[df['Category'] == 'drink']
drink_quantity_by_month = drink_data.groupby('Month')['Menu'].count().reset_index(name='Drink Quantity')
fig9 = px.line(drink_quantity_by_month, x='Month', y='Drink Quantity', title="Quantity of Drink Menus by Month")
st.plotly_chart(fig9, use_container_width=True)
