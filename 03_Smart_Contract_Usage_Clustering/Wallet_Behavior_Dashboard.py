#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# --------------------------------------
# Page config
st.set_page_config(page_title="OnChain Pulse: Wallet Activity Tracker", layout="wide")
st.title("🔋 OnChain Pulse: Wallet Activity Tracker")

# Load data
url = "https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Smart_Contract_Usage_Clustering/data.csv"
data = pd.read_csv(url, on_bad_lines='skip')  
data["BLOCK_TIMESTAMP"] = pd.to_datetime(data["BLOCK_TIMESTAMP"], errors="coerce")
data = data.dropna(subset=["BLOCK_TIMESTAMP"])


# Calculate additional metrics
data['Gas_Efficiency'] = data['VALUE'] / data['GAS_USED'].replace(0, 1)
data['Activity_Date'] = data['BLOCK_TIMESTAMP'].dt.date

# Sidebar filters
st.sidebar.header("Filters")
selected_dates = st.sidebar.date_input("Select date range", [data['BLOCK_TIMESTAMP'].min(), data['BLOCK_TIMESTAMP'].max()])
selected_persona = st.sidebar.multiselect("Select Dominant Persona", options=data['dominant_persona'].unique(), default=data['dominant_persona'].unique())

# Apply filters
mask = (data['BLOCK_TIMESTAMP'].dt.date >= selected_dates[0]) & (data['BLOCK_TIMESTAMP'].dt.date <= selected_dates[1])
mask &= data['dominant_persona'].isin(selected_persona)
data = data[mask]

# Section 1: Trends Over Time
st.subheader("1. Persona Market Share and Value/Gas Trends Over Time")
col1, col2 = st.columns(2)

# Persona Market Share Over Time
data_grouped = data.groupby([pd.Grouper(key='BLOCK_TIMESTAMP', freq='W'), 'dominant_persona']).size().reset_index(name='count')
fig1 = px.line(data_grouped, x='BLOCK_TIMESTAMP', y='count', color='dominant_persona', title="Persona Market Share Over Time")
col1.plotly_chart(fig1, use_container_width=True)

# Average VALUE/GAS Over Time
value_gas = data.groupby([pd.Grouper(key='BLOCK_TIMESTAMP', freq='W'), 'dominant_persona']).agg({
    'VALUE': 'mean',
    'GAS_USED': 'mean'
}).reset_index()
fig2 = px.line(value_gas, x='BLOCK_TIMESTAMP', y='VALUE', color='dominant_persona', title="Average VALUE Over Time")
col2.plotly_chart(fig2, use_container_width=True)

# Section 2: Top Wallets
st.subheader("2. Top Wallets by Activity")
col3, col4 = st.columns(2)

top_value = data.groupby('FROM_ADDRESS').agg({'VALUE':'sum', 'dominant_persona':'first'}).sort_values(by='VALUE', ascending=False).head(10).reset_index()
fig3 = px.bar(top_value, x='FROM_ADDRESS', y='VALUE', color='dominant_persona', title="Top 10 Wallets by Total VALUE")
col3.plotly_chart(fig3, use_container_width=True)

top_gas = data.groupby('FROM_ADDRESS').agg({'GAS_USED':'sum', 'dominant_persona':'first'}).sort_values(by='GAS_USED', ascending=False).head(10).reset_index()
fig4 = px.bar(top_gas, x='FROM_ADDRESS', y='GAS_USED', color='dominant_persona', title="Top 10 Wallets by Total GAS Used")
col4.plotly_chart(fig4, use_container_width=True)

# Section 3: Persona-Specific Deep Dive
st.subheader("3. Persona-Specific Deep Dive")
selected_dive = st.selectbox("Select Persona for Deep Dive", options=data['dominant_persona'].unique())

persona_data = data[data['dominant_persona'] == selected_dive]
persona_summary = persona_data.groupby('FROM_ADDRESS').agg({
    'VALUE':'mean',
    'GAS_USED':'mean',
    'FROM_ADDRESS':'count'
}).rename(columns={'FROM_ADDRESS':'tx_count'}).mean()

st.metric("Avg Transaction Size", round(persona_summary['VALUE'], 4))
st.metric("Avg Gas Used", round(persona_summary['GAS_USED'], 4))
st.metric("Avg Transactions per Wallet", round(persona_summary['tx_count'], 2))

# Section 4: Behavioral Ratios
st.subheader("4. Behavioral Ratios")
col5, col6 = st.columns(2)

behavioral_ratios = data.groupby('dominant_persona').agg({
    'Gas_Efficiency': 'mean',
    'VALUE': 'mean',
    'GAS_USED': 'mean'
}).reset_index()
behavioral_ratios['Value_per_TX'] = behavioral_ratios['VALUE'] / (behavioral_ratios['GAS_USED'].replace(0, 1))

fig5 = px.bar(behavioral_ratios, x='dominant_persona', y='Gas_Efficiency', title="Gas Efficiency by Persona")
col5.plotly_chart(fig5, use_container_width=True)

fig6 = px.bar(behavioral_ratios, x='dominant_persona', y='Value_per_TX', title="Value per Transaction by Persona")
col6.plotly_chart(fig6, use_container_width=True)

# Section 5: Anomalies
st.subheader("5. Highlight Recent Anomalies")
col7, col8 = st.columns(2)

recent = data[data['BLOCK_TIMESTAMP'] > data['BLOCK_TIMESTAMP'].max() - pd.Timedelta(weeks=2)]
previous = data[data['BLOCK_TIMESTAMP'] <= data['BLOCK_TIMESTAMP'].max() - pd.Timedelta(weeks=2)]

recent_counts = recent['dominant_persona'].value_counts()
previous_counts = previous['dominant_persona'].value_counts()

compare = pd.DataFrame({
    'recent': recent_counts,
    'previous': previous_counts
}).fillna(0)
compare['change_%'] = (compare['recent'] - compare['previous']) / compare['previous'].replace(0, 1) * 100

biggest_increase = compare['change_%'].idxmax()
biggest_drop = compare['change_%'].idxmin()

col7.metric("Biggest Increase", f"{biggest_increase} ({compare['change_%'].max():.2f}%)")
col8.metric("Biggest Drop", f"{biggest_drop} ({compare['change_%'].min():.2f}%)")


# ـــ
st.markdown("---")
st.caption("Built with ❤️ using Streamlit and Plotly")


