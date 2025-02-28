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
custom_colors = ['#F2DD83', '#9A8CB5','#CBD9EF', '#FCD5C6',  '#EB9861', '#72884B', '#567BA2']

# Header
st.title("Restaurant Dashboard")

# Overall Section
st.header("Overall")



# Chart 0: Bar and Line in One Chart with Category Filter for Bar Chart

# Filter for Category (for bar chart only)
category_filter = st.selectbox("Select Category for Bar Chart", options=["All", "food", "drink"], index=0)

# Apply filter to the bar chart data
if category_filter == "All":
    bar_data = df.groupby('Day Of Week')['Price'].sum().reset_index(name='Average Sales')
else:
    bar_data = df[df['Category'] == category_filter].groupby('Day Of Week')['Price'].sum().reset_index(name='Average Sales')

# Line Chart Data: Staff (Kitchen Staff, Drinks Staff) by Day of Week (unchanged)
line_data = df.groupby('Day Of Week').agg({'Kitchen Staff': 'mean', 'Drinks Staff': 'mean'}).reset_index()

# Create Figure
fig0 = go.Figure()

# Add Bar Chart for Average Sales (filtered by category)
fig0.add_trace(go.Bar(
    x=bar_data['Day Of Week'],
    y=bar_data['Average Sales'],
    name='Average Sales',
    marker_color='#F2DD83',
    yaxis='y1'
))

# Add Line Chart for Kitchen Staff
fig0.add_trace(go.Scatter(
    x=line_data['Day Of Week'],
    y=line_data['Kitchen Staff'],
    mode='lines',
    name='Kitchen Staff',
    line=dict(color='#ff5757'),
    yaxis='y2'
))

# Add Line Chart for Drinks Staff
fig0.add_trace(go.Scatter(
    x=line_data['Day Of Week'],
    y=line_data['Drinks Staff'],
    mode='lines',
    name='Drinks Staff',
    line=dict(color='#9A8CB5'),
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

# Display Chart
st.plotly_chart(fig0, use_container_width=True)


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
    fig2.update_yaxes(range=[2500, 5000])
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
    fig4.update_yaxes(range=[2200, 2600])
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
    fig5.update_yaxes(range=[2500, 4500])
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    # Chart 6: Line chart with area (Average Waiting Time vs. Kitchen Staff)
    avg_wait_time_by_staff = df.groupby('Kitchen Staff')['Waiting Time'].mean().reset_index(name='Avg Waiting Time')
    avg_wait_time_by_staff = avg_wait_time_by_staff[avg_wait_time_by_staff['Avg Waiting Time'] >= 1000]  # Filter to show 1,000+
    fig6 = px.area(avg_wait_time_by_staff, x='Kitchen Staff', y='Avg Waiting Time', 
                   title="Average Waiting Time vs. Kitchen Staff", 
                   markers=True, 
                   color_discrete_sequence=custom_colors)
    fig6.update_yaxes(range=[1400, 2500])
    st.plotly_chart(fig6, use_container_width=True)
# Chart 7 and Chart 8: Place in the same row
col7, col8 = st.columns(2)

with col7:
    # Chart 7: Line chart without area (Average Waiting Time by Month)
    avg_wait_time_by_month = df.groupby('Month')['Waiting Time'].mean().reset_index(name='Avg Waiting Time')
    fig7 = px.line(avg_wait_time_by_month, x='Month', y='Avg Waiting Time', 
                   title="Average Waiting Time by Month", 
                   markers=True, 
                   color_discrete_sequence=custom_colors)
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    # Chart 8: Line chart with dual y-axes (Menu Count and Kitchen Staff by Day of Week)
    menu_and_staff_by_day = df.groupby('Day Of Week').agg({'Menu': 'count', 'Kitchen Staff': 'mean'}).reset_index()
    fig8 = go.Figure()

    # Add trace for Menu Count (left y-axis)
    fig8.add_trace(go.Scatter(x=menu_and_staff_by_day['Day Of Week'], 
                              y=menu_and_staff_by_day['Menu'], 
                              mode='lines+markers', 
                              name='Menu Count', 
                              line=dict(color=custom_colors[0])))

    # Add trace for Kitchen Staff (right y-axis)
    fig8.add_trace(go.Scatter(x=menu_and_staff_by_day['Day Of Week'], 
                              y=menu_and_staff_by_day['Kitchen Staff'], 
                              mode='lines+markers', 
                              name='Kitchen Staff', 
                              line=dict(color=custom_colors[1]), 
                              yaxis="y2"))

    # Configure layout for dual y-axes
    fig8.update_layout(
        title="Menu Count and Kitchen Staff by Day of Week",
        xaxis_title="Day of Week",
        yaxis_title="Menu Count",
        yaxis2=dict(
            title="Kitchen Staff",
            overlaying="y",
            side="right"
        )
    )
    st.plotly_chart(fig8, use_container_width=True)

# Waiting Time - Drink Section
st.header("Waiting Time - Drink")

# Chart 9: Full-width chart
drink_data = df[df['Category'] == 'drink']
drink_quantity_by_month = drink_data.groupby(['Month', 'Menu']).size().reset_index(name='Drink Quantity')
fig9 = px.line(drink_quantity_by_month, x='Month', y='Drink Quantity', color='Menu', 
               title="Quantity of Drink Menus by Month (per Drink Type)", 
               markers=True, 
               color_discrete_sequence=custom_colors)
st.plotly_chart(fig9, use_container_width=True)
