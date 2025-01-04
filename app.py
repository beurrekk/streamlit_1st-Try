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
df['Day Of Week'] = pd.Categorical(df['Day Of Week'], 
                                   categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
                                   ordered=True)
df['Waiting Time'] = (df['Serve Time'] - df['Order Time']).dt.total_seconds()

# Header
st.title("Restaurant Dashboard")

# Overall Section
st.header("Overall")

# Row 1: Chart 1 and Chart 2
col1, col2 = st.columns(2)

# Chart 1: Line chart with area (Sum of Price by Month with Trend Line)
with col1:
    price_by_month = df.groupby('Month')['Price'].sum().reset_index()
    fig1 = px.area(price_by_month, x='Month', y='Price', title="Sum of Price by Month", markers=True)
    fig1.add_traces(go.Scatter(x=price_by_month['Month'], y=price_by_month['Price'], mode='lines', name='Trend Line'))
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Line chart with area (Average Count of Menu by Day of Week)
with col2:
    menu_by_day = df.groupby('Day Of Week')['Menu'].count().reset_index(name='Menu Count')
    fig2 = px.area(menu_by_day, x='Day Of Week', y='Menu Count', title="Average Count of Menu by Day of Week", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

# Popular Menu Section
st.header("Popular Menu")

# Row 2: Chart 3 and Chart 4
col3, col4 = st.columns(2)

# Chart 3: Bar chart (Top 4 Popular Food Categories)
with col3:
    top_food = df[df['Category'] == 'food'].groupby('Menu').size().nlargest(4).reset_index(name='Count')
    fig3 = px.bar(top_food, x='Menu', y='Count', title="Top 4 Popular Food Categories")
    st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Bar chart (Top 4 Popular Drink Categories)
with col4:
    top_drink = df[df['Category'] == 'drink'].groupby('Menu').size().nlargest(4).reset_index(name='Count')
    fig4 = px.bar(top_drink, x='Menu', y='Count', title="Top 4 Popular Drink Categories")
    st.plotly_chart(fig4, use_container_width=True)

# Waiting Time - Food Section
st.header("Waiting Time - Food")

# Row 3: Chart 5 and Chart 6
col5, col6 = st.columns(2)

# Chart 5: Line chart with area (Quantity of All Menus by Month)
with col5:
    menu_quantity_by_month = df.groupby('Month')['Menu'].count().reset_index(name='Menu Quantity')
    fig5 = px.area(menu_quantity_by_month, x='Month', y='Menu Quantity', title="Quantity of All Menus by Month", markers=True)
    st.plotly_chart(fig5, use_container_width=True)

# Chart 6: Line chart with area (Average Waiting Time vs. Kitchen Staff)
with col6:
    avg_wait_time_by_staff = df.groupby('Kitchen Staff')['Waiting Time'].mean().reset_index(name='Avg Waiting Time')
    fig6 = px.area(avg_wait_time_by_staff, x='Kitchen Staff', y='Avg Waiting Time', title="Average Waiting Time vs. Kitchen Staff", markers=True)
    st.plotly_chart(fig6, use_container_width=True)

# Row 4: Chart 7 and Chart 8
col7, col8 = st.columns(2)

# Chart 7: Line chart without area (Average Waiting Time by Month)
with col7:
    avg_wait_time_by_month = df.groupby('Month')['Waiting Time'].mean().reset_index(name='Avg Waiting Time')
    fig7 = px.line(avg_wait_time_by_month, x='Month', y='Avg Waiting Time', title="Average Waiting Time by Month", markers=True)
    st.plotly_chart(fig7, use_container_width=True)

# Chart 8: Line chart without area (Count of Menu and Kitchen Staff by Day of Week)
with col8:
    menu_and_staff_by_day = df.groupby('Day Of Week').agg({'Menu': 'count', 'Kitchen Staff': 'mean'}).reset_index()
    fig8 = go.Figure()
    fig8.add_trace(go.Scatter(x=menu_and_staff_by_day['Day Of Week'], y=menu_and_staff_by_day['Menu'], mode='lines+markers', name='Menu Count'))
    fig8.add_trace(go.Scatter(x=menu_and_staff_by_day['Day Of Week'], y=menu_and_staff_by_day['Kitchen Staff'], mode='lines+markers', name='Kitchen Staff'))
    fig8.update_layout(title="Menu Count and Kitchen Staff by Day of Week", xaxis_title="Day of Week")
    st.plotly_chart(fig8, use_container_width=True)

# Waiting Time - Drink Section
st.header("Waiting Time - Drink")

# Row 5: Chart 9
col9, _ = st.columns([2, 1])  # Use 2 columns, but only use the left one for the chart

# Chart 9: Line chart without area (Quantity of Drink Menus by Month)
with col9:
    drink_data = df[df['Category'] == 'drink']
    drink_quantity_by_month = drink_data.groupby(['Month', 'Menu']).size().reset_index(name='Drink Quantity')
    fig9 = px.line(drink_quantity_by_month, x='Month', y='Drink Quantity', color='Menu', 
                   title="Quantity of Drink Menus by Month (per Drink Type)", markers=True)
    st.plotly_chart(fig9, use_container_width=True)
