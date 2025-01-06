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
st.set_page_config(layout="wide")  # Set wide layout for Streamlit
st.title("Restaurant Dashboard")

# Chart 0: Bar and Line in One Chart
st.header("Overall Sales and Staff Analysis")
bar_data = df.groupby('Day Of Week')['Price'].sum().reset_index(name='Average Sales')
line_data = df.groupby('Day Of Week').agg({'Kitchen Staff': 'mean', 'Drinks Staff': 'mean'}).reset_index()

fig0 = go.Figure()
fig0.add_trace(go.Bar(
    x=bar_data['Day Of Week'],
    y=bar_data['Average Sales'],
    name='Average Sales',
    marker_color='#F2DD83',
    yaxis='y1'
))
fig0.add_trace(go.Scatter(
    x=line_data['Day Of Week'],
    y=line_data['Kitchen Staff'],
    mode='lines',
    name='Kitchen Staff',
    line=dict(color='#CBD9EF'),
    yaxis='y2'
))
fig0.add_trace(go.Scatter(
    x=line_data['Day Of Week'],
    y=line_data['Drinks Staff'],
    mode='lines',
    name='Drinks Staff',
    line=dict(color='#FCD5C6'),
    yaxis='y2'
))

# Set layout for dual y-axis
fig0.update_layout(
    title="Average Sales and Staff by Day of Week",
    xaxis_title="Day of Week",
    yaxis=dict(
        title="Average Sales",
        titlefont=dict(color="#F2DD83"),
        tickfont=dict(color="#F2DD83"),
    ),
    yaxis2=dict(
        title="Staff Count",
        titlefont=dict(color="#CBD9EF"),
        tickfont=dict(color="#CBD9EF"),
        overlaying="y",
        side="right"
    ),
    legend=dict(orientation="h"),
    barmode='group'
)
st.plotly_chart(fig0, use_container_width=True)

# Rest of the charts go here (Charts 1–9), following similar adjustments
# Ensure to match column names as per the dataset and apply color changes


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
