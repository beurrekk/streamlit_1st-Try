import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the dashboard
st.title("Restaurant Dashboard")

# Load data
data = pd.read_csv("test_data.csv")


# Chart 1: Line Chart with Area (Sum of Price by Month with Trend Line)
st.subheader("Sum of Price by Month (with Trend Line)")
price_by_month = data.groupby('month')['price'].sum().reset_index()
fig1 = px.line(price_by_month, x='month', y='price', title="Sum of Price by Month",
               markers=True, line_shape='spline', trendline='ols')
fig1.update_traces(fill='tozeroy', line_color='#636efb')
fig1.update_layout(xaxis_title='Month', yaxis_title='Total Price')
st.plotly_chart(fig1)

# Chart 2: Line Chart with Area (Average Count of Menu by Day of Week)
st.subheader("Average Count of Menu by Day of Week")
menu_by_day = data.groupby('day_of_week').size().reset_index(name='count')
menu_by_day['average'] = menu_by_day['count'] / menu_by_day['count'].sum()
order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
menu_by_day = menu_by_day.set_index('day_of_week').loc[order].reset_index()
fig2 = px.line(menu_by_day, x='day_of_week', y='average', title="Average Menu Count by Day of Week",
               markers=True, line_shape='spline')
fig2.update_traces(fill='tozeroy', line_color='#ef553b')
fig2.update_layout(xaxis_title='Day of Week', yaxis_title='Average Count')
st.plotly_chart(fig2)

# Chart 3: Bar Chart (Top 4 Most Popular Food Menus)
st.subheader("Top 4 Most Popular Food Menus")
food_data = data[data['category'] == 'food']
top_foods = food_data['menu'].value_counts().nlargest(4).reset_index()
top_foods.columns = ['menu', 'count']
fig3 = px.bar(top_foods, x='menu', y='count', title="Top 4 Most Popular Food Menus",
              text='count', color_discrete_sequence=['#636efb'])
fig3.update_layout(xaxis_title='Menu', yaxis_title='Count')
st.plotly_chart(fig3)

# Chart 4: Bar Chart (Top 4 Most Popular Drink Menus)
st.subheader("Top 4 Most Popular Drink Menus")
drink_data = data[data['category'] == 'drink']
top_drinks = drink_data['menu'].value_counts().nlargest(4).reset_index()
top_drinks.columns = ['menu', 'count']
fig4 = px.bar(top_drinks, x='menu', y='count', title="Top 4 Most Popular Drink Menus",
              text='count', color_discrete_sequence=['#ef553b'])
fig4.update_layout(xaxis_title='Menu', yaxis_title='Count')
st.plotly_chart(fig4)

# Chart 5: Line Chart with Area (Quantity of All Menus by Month)
st.subheader("Quantity of All Menus by Month")
quantity_by_month = data.groupby('month')['quantity'].sum().reset_index()
fig5 = px.line(quantity_by_month, x='month', y='quantity', title="Quantity of All Menus by Month",
               markers=True, line_shape='spline')
fig5.update_traces(fill='tozeroy', line_color='#636efb')
fig5.update_layout(xaxis_title='Month', yaxis_title='Total Quantity')
st.plotly_chart(fig5)

# Chart 6: Line Chart with Area (Average Waiting Time by Kitchen Staff)
st.subheader("Average Waiting Time by Kitchen Staff")
data['waiting_time'] = (pd.to_datetime(data['serve_time']) - pd.to_datetime(data['order_time'])).dt.total_seconds()
waiting_by_staff = data.groupby('kitchen_staff')['waiting_time'].mean().reset_index()
fig6 = px.line(waiting_by_staff, x='kitchen_staff', y='waiting_time',
               title="Average Waiting Time by Kitchen Staff",
               markers=True, line_shape='spline')
fig6.update_traces(fill='tozeroy', line_color='#ef553b')
fig6.update_layout(xaxis_title='Number of Kitchen Staff', yaxis_title='Average Waiting Time (seconds)')
st.plotly_chart(fig6)
