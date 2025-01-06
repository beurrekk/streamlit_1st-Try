import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Load the dataset
data_file = 'test_data.csv'
df = pd.read_csv(data_file)

# Preprocessing
df['Order Time'] = pd.to_datetime(df['Order Time'])
df['Serve Time'] = pd.to_datetime(df['Serve Time'])
df['Month'] = df['Order Time'].dt.strftime('%B')  # Month names
df['Month'] = pd.Categorical(df['Month'], categories=[
    'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)
df['Day Of Week'] = pd.Categorical(df['Day Of Week'], 
                                   categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
                                   ordered=True)
df['Waiting Time'] = (df['Serve Time'] - df['Order Time']).dt.total_seconds()

# Define custom colors
custom_colors = ['#F2DD83', '#CBD9EF', '#FCD5C6', '#9A8CB5', '#EB9861', '#72884B', '#567BA2']

# Header
st.title("Restaurant Dashboard")

# ===================== CHART 0 =====================
st.header("Chart 0: Sales and Staff Quantity per Day of Week")

# Data preparation
avg_sales_day = df.groupby('Day Of Week')['Price'].mean().reset_index(name='Average Sales')
staff_data = df.groupby(['Day Of Week']).agg({'Kitchen Staff': 'mean', 'Drink Staff': 'mean'}).reset_index()

# Create the chart
fig0 = go.Figure()

fig0.add_trace(go.Bar(
    x=avg_sales_day['Day Of Week'], 
    y=avg_sales_day['Average Sales'], 
    name='Average Sales (Bar)',
    marker=dict(color=custom_colors[0]),
    yaxis="y"  # Left y-axis
))

fig0.add_trace(go.Scatter(
    x=staff_data['Day Of Week'], 
    y=staff_data['Kitchen Staff'], 
    mode='lines', 
    name='Kitchen Staff (Line)',
    line=dict(width=2, color=custom_colors[3]),
    yaxis="y2"  # Right y-axis
))

fig0.add_trace(go.Scatter(
    x=staff_data['Day Of Week'], 
    y=staff_data['Drink Staff'], 
    mode='lines', 
    name='Drink Staff (Line)',
    line=dict(width=2, color=custom_colors[4]),
    yaxis="y2"  # Right y-axis
))

fig0.update_layout(
    title="Sales and Staff Quantity per Day of Week (Bar & Line)",
    xaxis_title="Day of Week",
    yaxis=dict(
        title="Average Sales (Bar)",
        titlefont=dict(color=custom_colors[0]),
        tickfont=dict(color=custom_colors[0]),
        side="left"
    ),
    yaxis2=dict(
        title="Staff Quantity (Line)",
        titlefont=dict(color=custom_colors[3]),
        tickfont=dict(color=custom_colors[3]),
        overlaying="y",
        side="right"
    ),
    barmode='group',
    template='plotly_white',
    legend=dict(title="Legend")
)

st.plotly_chart(fig0, use_container_width=True)

# ===================== CHART 1 =====================
st.header("Chart 1: Sum of Price by Month")

price_by_month = df.groupby('Month')['Price'].sum().reset_index()
fig1 = px.area(price_by_month, x='Month', y='Price', 
               title="Sum of Price by Month", 
               markers=True, 
               color_discrete_sequence=[custom_colors[1]])
fig1.update_yaxes(range=[8000, 14000])  # Set y-axis range
st.plotly_chart(fig1, use_container_width=True)

# ===================== CHART 2 =====================
st.header("Chart 2: Average Count of Menu by Day of Week")

menu_by_day = df.groupby('Day Of Week')['Menu'].count().reset_index(name='Menu Count')
fig2 = px.area(menu_by_day, x='Day Of Week', y='Menu Count', 
               title="Average Count of Menu by Day of Week", 
               markers=True, 
               color_discrete_sequence=[custom_colors[2]])
fig2.update_yaxes(range=[2000, 5000])  # Set y-axis range
st.plotly_chart(fig2, use_container_width=True)

# ===================== CHART 3 =====================
st.header("Chart 3: Top 4 Popular Food Categories")

top_food = df[df['Category'] == 'food'].groupby('Menu').size().nlargest(4).reset_index(name='Count')
fig3 = px.bar(top_food, x='Menu', y='Count', 
              title="Top 4 Popular Food Categories", 
              color_discrete_sequence=[custom_colors[4]])
fig3.update_yaxes(range=[2000, 2600])  # Set y-axis range
st.plotly_chart(fig3, use_container_width=True)

# ===================== CHART 4 =====================
st.header("Chart 4: Top 4 Popular Drink Categories")

top_drink = df[df['Category'] == 'drink'].groupby('Menu').size().nlargest(4).reset_index(name='Count')
fig4 = px.bar(top_drink, x='Menu', y='Count', 
              title="Top 4 Popular Drink Categories", 
              color_discrete_sequence=[custom_colors[5]])
fig4.update_yaxes(range=[2000, 2600])  # Set y-axis range
st.plotly_chart(fig4, use_container_width=True)

# ===================== CHART 5 =====================
st.header("Chart 5: Quantity of All Menus by Month")

menu_quantity_by_month = df.groupby('Month')['Menu'].count().reset_index(name='Menu Quantity')
fig5 = px.area(menu_quantity_by_month, x='Month', y='Menu Quantity', 
               title="Quantity of All Menus by Month", 
               markers=True, 
               color_discrete_sequence=[custom_colors[6]])
fig5.update_yaxes(range=[2000, 4500])  # Set y-axis range
st.plotly_chart(fig5, use_container_width=True)

# ===================== CHART 6 =====================
st.header("Chart 6: Average Waiting Time vs. Kitchen Staff")

avg_wait_time_by_staff = df.groupby('Kitchen Staff')['Waiting Time'].mean().reset_index(name='Avg Waiting Time')
fig6 = px.area(avg_wait_time_by_staff, x='Kitchen Staff', y='Avg Waiting Time', 
               title="Average Waiting Time vs. Kitchen Staff", 
               markers=True, 
               color_discrete_sequence=[custom_colors[0]])
fig6.update_yaxes(range=[1000, 2500])  # Set y-axis range
st.plotly_chart(fig6, use_container_width=True)

# ===================== CHART 7 =====================
st.header("Chart 7: Average Waiting Time by Month")

avg_wait_time_by_month = df.groupby('Month')['Waiting Time'].mean().reset_index(name='Avg Waiting Time')
fig7 = px.line(avg_wait_time_by_month, x='Month', y='Avg Waiting Time', 
               title="Average Waiting Time by Month", 
               markers=True, 
               color_discrete_sequence=[custom_colors[1]])
st.plotly_chart(fig7, use_container_width=True)

# ===================== CHART 8 =====================
st.header("Chart 8: Menu Count and Kitchen Staff by Day of Week")

menu_and_staff_by_day = df.groupby('Day Of Week').agg({'Menu': 'count', 'Kitchen Staff': 'mean'}).reset_index()
fig8 = go.Figure()
fig8.add_trace(go.Scatter(x=menu_and_staff_by_day['Day Of Week'], y=menu_and_staff_by_day['Menu'], 
                          mode='lines', name='Menu Count', line=dict(color=custom_colors[3])))
fig8.add_trace(go.Scatter(x=menu_and_staff_by_day['Day Of Week'], y=menu_and_staff_by_day['Kitchen Staff'], 
                          mode='lines', name='Kitchen Staff', line=dict(color=custom_colors[4])))
fig8.update_layout(title="Menu Count and Kitchen Staff by Day of Week", 
                   xaxis_title="Day of Week", yaxis_title="Menu Count")
st.plotly_chart(fig8, use_container_width=True)

# ===================== CHART 9 =====================
st.header("Chart 9: Quantity of Drink Menus by Month")

drink_data = df[df['Category'] == 'drink']
drink_quantity_by_month = drink_data.groupby(['Month', 'Menu']).size().reset_index(name='Drink Quantity')
fig9 = px.line(drink_quantity_by_month, x='Month', y='Drink Quantity', color='Menu', 
               title="Quantity of Drink Menus by Month (per Drink Type)", 
               markers=True, 
               color_discrete_sequence=custom_colors[:3])
st.plotly_chart(fig9, use_container_width=True)
