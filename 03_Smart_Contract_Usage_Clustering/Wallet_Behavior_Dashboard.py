#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
# --------------------------------------
# Page config
st.set_page_config(page_title="OnChain Pulse: Wallet Activity Tracker", layout="wide")
st.title("🔋 OnChain Pulse: Wallet Activity Tracker")

# Load data
url = "https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Smart_Contract_Usage_Clustering/data_all.csv"
data = pd.read_csv(url, on_bad_lines='skip')  
data["BLOCK_TIMESTAMP"] = pd.to_datetime(data["BLOCK_TIMESTAMP"], errors="coerce")
data = data.dropna(subset=["BLOCK_TIMESTAMP"])

# Calculate additional metrics
data['Gas_Efficiency'] = data['VALUE'] / data['GAS_USED'].replace(0, 1)
data['Activity_Date'] = data['BLOCK_TIMESTAMP'].dt.date

# Sidebar filters
st.sidebar.header("Filters")

# Time filter options
time_filter_option = st.sidebar.selectbox("Select time range", ("Last 1 Month", "Last 3 Months", "Last 6 Months", "Last 12 Months"))
now = datetime.now().date()

if time_filter_option == "Last 1 Month":
    start_date = now - timedelta(days=30)
elif time_filter_option == "Last 3 Months":
    start_date = now - timedelta(days=90)
elif time_filter_option == "Last 6 Months":
    start_date = now - timedelta(days=180)
elif time_filter_option == "Last 12 Months":
    start_date = now - timedelta(days=365)

selected_persona = st.sidebar.multiselect("Select Dominant Persona", options=data['dominant_persona'].unique(), default=data['dominant_persona'].unique())

# Apply global filters
mask = (data['BLOCK_TIMESTAMP'].dt.date >= start_date) & (data['BLOCK_TIMESTAMP'].dt.date <= now)
mask &= data['dominant_persona'].isin(selected_persona)
data_filtered = data[mask]

# Section 1: Trends Over Time
st.subheader("1. Persona Market Share and Value/Gas Trends Over Time")
col1, col2 = st.columns(2)

# Persona Market Share Over Time
data_grouped = data_filtered.groupby([pd.Grouper(key='BLOCK_TIMESTAMP', freq='W'), 'dominant_persona']).size().reset_index(name='count')
fig1 = px.line(data_grouped, x='BLOCK_TIMESTAMP', y='count', color='dominant_persona', title="Persona Market Share Over Time")
col1.plotly_chart(fig1, use_container_width=True)

# Average VALUE Over Time
value_gas = data_filtered.groupby([pd.Grouper(key='BLOCK_TIMESTAMP', freq='W'), 'dominant_persona']).agg({
    'VALUE': 'mean',
    'GAS_USED': 'mean'
}).reset_index()
fig2 = px.line(value_gas, x='BLOCK_TIMESTAMP', y='VALUE', color='dominant_persona', title="Average VALUE Over Time")
col2.plotly_chart(fig2, use_container_width=True)

# Section 2: Top Wallets
st.subheader("2. Top Wallets by Activity")
col3, col4 = st.columns(2)

wallet_search = st.text_input("Search Wallet Address")

top_value = data_filtered.groupby('FROM_ADDRESS').agg({'VALUE':'sum', 'dominant_persona':'first'}).sort_values(by='VALUE', ascending=False).reset_index()
if wallet_search:
    top_value = top_value[top_value['FROM_ADDRESS'].str.contains(wallet_search, case=False)]
col3.dataframe(top_value[['FROM_ADDRESS', 'dominant_persona', 'VALUE']].head(10))

top_gas = data_filtered.groupby('FROM_ADDRESS').agg({'GAS_USED':'sum', 'dominant_persona':'first'}).sort_values(by='GAS_USED', ascending=False).reset_index()
if wallet_search:
    top_gas = top_gas[top_gas['FROM_ADDRESS'].str.contains(wallet_search, case=False)]
col4.dataframe(top_gas[['FROM_ADDRESS', 'dominant_persona', 'GAS_USED']].head(10))

# Section 3: Persona-Specific Deep Dive
st.subheader("3. Persona-Specific Deep Dive")
selected_dive = st.selectbox("Select Persona for Deep Dive", options=data['dominant_persona'].unique())

persona_data = data[data['dominant_persona'] == selected_dive]
persona_summary = persona_data.groupby('FROM_ADDRESS').agg({
    'VALUE':'mean',
    'GAS_USED':'mean',
    'FROM_ADDRESS':'count'
}).rename(columns={'FROM_ADDRESS': 'tx_count'}).mean()

# Calculate transactions per week and month
avg_tx_week = persona_summary['tx_count'] / (7/7)
avg_tx_month = persona_summary['tx_count'] / (30/7)

# Calculate Gas Usage
eth_price = 3000
avg_gas_eth = persona_summary['GAS_USED'] / 1e9
avg_gas_usd = avg_gas_eth * eth_price

# Display
col5, col6, col7 = st.columns(3)

col5.metric("Avg Transactions per Week", f"{avg_tx_week:.2f}")
col6.metric("Avg Transactions per Month", f"{avg_tx_month:.2f}")
col7.metric("Avg Gas Used", f"{avg_gas_eth:.6f} ETH (~${avg_gas_usd:,.2f})")

# Section 4: Behavioral Patterns
st.subheader("4. Behavioral Patterns")

# Heatmap of transaction hours
data_filtered['hour'] = data_filtered['BLOCK_TIMESTAMP'].dt.hour
heatmap_data = data_filtered.groupby(['dominant_persona', 'hour']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="Blues", ax=ax)
plt.title("Transaction Activity by Hour and Persona")
st.pyplot(fig)

# Section 5: Highlight Recent Anomalies
st.subheader("5. Highlight Recent Anomalies")
col8, col9 = st.columns(2)

recent = data_filtered[data_filtered['BLOCK_TIMESTAMP'] > data_filtered['BLOCK_TIMESTAMP'].max() - pd.Timedelta(weeks=2)]
previous = data_filtered[data_filtered['BLOCK_TIMESTAMP'] <= data_filtered['BLOCK_TIMESTAMP'].max() - pd.Timedelta(weeks=2)]

recent_counts = recent['dominant_persona'].value_counts()
previous_counts = previous['dominant_persona'].value_counts()

compare = pd.DataFrame({
    'recent': recent_counts,
    'previous': previous_counts
}).fillna(0)
compare['change_%'] = (compare['recent'] - compare['previous']) / compare['previous'].replace(0, 1) * 100

biggest_increase = compare['change_%'].idxmax()
biggest_drop = compare['change_%'].idxmin()

inc_value = compare['change_%'].max()
dec_value = compare['change_%'].min()

inc_delta = "↑" if inc_value > 0 else "↓"
dec_delta = "↓" if dec_value < 0 else "↑"

col8.metric("Biggest Increase", f"{biggest_increase} ({inc_value:.2f}%)", delta_color="normal")
col9.metric("Biggest Drop", f"{biggest_drop} ({dec_value:.2f}%)", delta_color="inverse")

# Section 6: Advanced Analytics
st.subheader("6. Advanced Analytics")

col10, col11 = st.columns(2)

# Cumulative Wallet Growth
growth = data_filtered.groupby(data_filtered['BLOCK_TIMESTAMP'].dt.to_period('W'))['FROM_ADDRESS'].nunique().cumsum().reset_index()
growth['BLOCK_TIMESTAMP'] = growth['BLOCK_TIMESTAMP'].astype(str)
fig_growth = px.line(growth, x='BLOCK_TIMESTAMP', y='FROM_ADDRESS', title="Cumulative Wallet Growth Over Time")
col10.plotly_chart(fig_growth, use_container_width=True)

# Transaction Heatmap Day vs Hour
data_filtered['weekday'] = data_filtered['BLOCK_TIMESTAMP'].dt.day_name()
heatmap_day_hour = data_filtered.groupby(['weekday', 'hour']).size().unstack(fill_value=0)
heatmap_day_hour = heatmap_day_hour.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
fig_heatmap_day_hour = px.imshow(heatmap_day_hour, labels=dict(x="Hour", y="Day", color="Number of TXs"), title="Transaction Heatmap Day vs Hour")
col11.plotly_chart(fig_heatmap_day_hour, use_container_width=True)

col12, col13 = st.columns(2)

# Top 10 Biggest Transactions
top_tx = data_filtered[['FROM_ADDRESS', 'TO_ADDRESS', 'VALUE', 'dominant_persona']].sort_values(by='VALUE', ascending=False).head(10)
col12.subheader("Top 10 Biggest Transactions")
col12.dataframe(top_tx)

# Transaction Size Variability
fig_box = px.box(data_filtered, x='dominant_persona', y='VALUE', points="outliers", title="Transaction Size Variability by Persona")
col13.plotly_chart(fig_box, use_container_width=True)

# ـــ
st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


