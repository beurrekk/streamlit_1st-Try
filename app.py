import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page layout to wide mode
st.set_page_config(layout="wide")

# Load data
data_path = "Edit_Review.csv"  # Ensure this file is in your GitHub repo

data = pd.read_csv(data_path, encoding='ISO-8859-1', delimiter=',', skipinitialspace=True)

# Preprocess data
data['Review Date'] = pd.to_datetime(data['Review Date'], errors='coerce')
data['Month'] = data['Review Date'].dt.to_period('M')
data['Review Group'] = data['Rating'].apply(lambda x: 'Good Review' if x >= 4.0 else 'Bad Review')

# Dashboard Header
st.title("Hotel Review Dashboard")

# Filter for chart 2
hotels = ['All Hotels'] + data['Hotel'].dropna().unique().tolist()
selected_hotel = st.sidebar.selectbox("Select a hotel for the line chart:", hotels)

# Chart 1: Stacked Bar Chart
st.markdown("### Overall")
bar_data = data.groupby(['Hotel', 'Review Group']).size().reset_index(name='Count')
fig1 = px.bar(bar_data, 
              x='Hotel', 
              y='Count', 
              color='Review Group', 
              barmode='stack', 
              color_discrete_sequence=['#f2dd83', '#ff5757'],
              title="Stacked Bar Chart of Reviews by Hotel")
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Line Chart with Area
st.markdown("### Average Rating Over Time")
if selected_hotel != 'All Hotels':
    line_data = data[data['Hotel'] == selected_hotel]
else:
    line_data = data
line_data = line_data.groupby('Month')['Rating'].mean().reset_index()
fig2 = px.area(line_data, 
               x='Month', 
               y='Rating', 
               title=f"Average Rating Over Time ({selected_hotel})",
               color_discrete_sequence=['#72884B'])
st.plotly_chart(fig2, use_container_width=True)

# Add columns for layout customization
col1, col2 = st.columns(2)

# Display text
col1.markdown("#### Overall")
col1.markdown("""This dashboard provides an overview of hotel reviews. Use the filters to customize the view.""")
