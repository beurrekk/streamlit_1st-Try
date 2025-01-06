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
custom_colors = [ '#FCD5C6', '#F2DD83', '#9A8CB5', '#EB9861', '#72884B', '#567BA2', '#CBD9EF']

# Header
st.title("Restaurant Dashboard")

# Overall Section
st.header("Overall")

# Chart 1 and Chart 2: Place in the same row
col1, col2 = st.columns(2)

with col1:
    # Chart 1: Line chart with area (Sum of Price by Month with Trend Line)
    price_by_month = df.groupby('Month')['Price'].sum().reset_index()
    price_by_month = price_by_month[price_by_month['Price'] >= 8000]  # Filter to show 8,000+
    fig1 = px.area(price_by_month, x='Month', y='Price', 
                   title="Sum of Price by Month", 
                   markers=True, 
                   color_discrete_sequence=custom_colors)
    fig1.update_yaxes(range=[8000, 14000])
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Chart 2: Line chart with area (Average Count of Menu by Day of Week)
    menu_by_day = df.groupby('Day Of Week')['Menu'].count().reset_index(name='Menu Count')
    menu_by_day = menu_by_day[menu_by_day['Menu Count'] >= 2500]  # Filter to show 2,500+
    fig2 = px.area(menu_by_day, x='Day Of Week', y='Menu Count', 
                   title="Average Count of Menu by Day of Week", 
                   markers=True, 
                   color_discrete_sequence=custom_colors)
    fig2.update_yaxes(range=[2000, 5000])
    st.plotly_chart(fig2, use_container_width=True)

# Popular Menu Section
st.header("Popular Menu")

# Chart 3 and Chart 4: Place in the same row
col3, col4 = st.columns(2)

with col3:
    # Chart 3: Bar chart (Top 4 Popular Food Categories)
    top_food = df[df['Category'] == 'food'].groupby('Menu').size().nlargest(4).reset_index(name='Count')
    top_food = top_food[top_food['Count'] >= 2000]  # Filter to show 2,000+
    fig3 = px.bar(top_food, x='Menu', y='Count', 
                  title="Top 4 Popular Food Categories", 
                  color='Menu', 
                  color_discrete_sequence=custom_colors)
    fig3.update_yaxes(range=[2000, 2600])
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    # Chart 4: Bar chart (Top 4 Popular Drink Categories)
    top_drink = df[df['Category'] == 'drink'].groupby('Menu').size().nlargest(4).reset_index(name='Count')
    top_drink = top_drink[top_drink['Count'] >= 2000]  # Filter to show 2,000+
    fig4 = px.bar(top_drink, x='Menu', y='Count', 
                  title="Top 4 Popular Drink Categories", 
                  color='Menu', 
                  color_discrete_sequence=custom_colors)
    fig4.update_yaxes(range=[2000, 2600])
    st.plotly_chart(fig4, use_container_width=True)

# Waiting Time - Food Section
st.header("Waiting Time - Food")

# Chart 5 and Chart 6: Place in the same row
col5, col6 = st.columns(2)

with col5:
    # Chart 5: Line chart with area (Quantity of All Menus by Month)
    menu_quantity_by_month = df.groupby('Month')['Menu'].count().reset_index(name='Menu Quantity')
    menu_quantity_by_month = menu_quantity_by_month[menu_quantity_by_month['Menu Quantity'] >= 2000]  # Filter to show 2,000+
    fig5 = px.area(menu_quantity_by_month, x='Month', y='Menu Quantity', 
                   title="Quantity of All Menus by Month", 
                   markers=True, 
                   color_discrete_sequence=custom_colors)
    fig5.update_yaxes(range=[2000, 4500])
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    # Chart 6: Line chart with area (Average Waiting Time vs. Kitchen Staff)
    avg_wait_time_by_staff = df.groupby('Kitchen Staff')['Waiting Time'].mean().reset_index(name='Avg Waiting Time')
    avg_wait_time_by_staff = avg_wait_time_by_staff[avg_wait_time_by_staff['Avg Waiting Time'] >= 1000]  # Filter to show 1,000+
    fig6 = px.area(avg_wait_time_by_staff, x='Kitchen Staff', y='Avg Waiting Time', 
                   title="Average Waiting Time vs. Kitchen Staff", 
                   markers=True, 
                   color_discrete_sequence=custom_colors)
    fig6.update_yaxes(range=[1000, 2500])
    st.plotly_chart(fig6, use_container_width=True)
