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

# Average VALUE Over Time
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
col3.dataframe(top_value[['FROM_ADDRESS', 'dominant_persona', 'VALUE']])

top_gas = data.groupby('FROM_ADDRESS').agg({'GAS_USED':'sum', 'dominant_persona':'first'}).sort_values(by='GAS_USED', ascending=False).head(10).reset_index()
col4.dataframe(top_gas[['FROM_ADDRESS', 'dominant_persona', 'GAS_USED']])

# Section 3: Persona-Specific Deep Dive
st.subheader("3. Persona-Specific Deep Dive")
selected_dive = st.selectbox("Select Persona for Deep Dive", options=data['dominant_persona'].unique())

persona_data = data[data['dominant_persona'] == selected_dive]
persona_summary = persona_data.groupby('FROM_ADDRESS').agg({
    'VALUE':'mean',
    'GAS_USED':'mean',
    'FROM_ADDRESS':'count'
}).rename(columns={'FROM_ADDRESS':'tx_count'}).mean()

# Calculate transactions per week and month
avg_tx_week = persona_summary['tx_count'] / (7/7)
avg_tx_month = persona_summary['tx_count'] / (30/7)

# Calculate Gas Usage
eth_price = 3000  # (replace this if you want to fetch live ETH price later)
avg_gas_eth = persona_summary['GAS_USED'] / 1e9
avg_gas_usd = avg_gas_eth * eth_price

# Display
col1, col2, col3 = st.columns(3)

col1.metric("Avg Transactions per Week", f"{avg_tx_week:.2f}")
col2.metric("Avg Transactions per Month", f"{avg_tx_month:.2f}")
col3.metric("Avg Gas Used", f"{avg_gas_eth:.6f} ETH (~${avg_gas_usd:,.2f})")

# Section 4: Behavioral Patterns
st.subheader("4. Behavioral Patterns")

# Heatmap of transaction hours
st.subheader("Heatmap of Transaction Hours by Persona")
data['hour'] = data['BLOCK_TIMESTAMP'].dt.hour
heatmap_data = data.groupby(['dominant_persona', 'hour']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="Blues", ax=ax)
plt.title("Transaction Activity by Hour and Persona")
st.pyplot(fig)

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
#___new
# Section 6: Advanced Analytics
st.subheader("6. Advanced Analytics")

# Prepare columns
col1, col2 = st.columns(2)

# --- Chart 1: Cumulative Wallet Growth ---
wallet_growth = data.groupby(data['BLOCK_TIMESTAMP'].dt.to_period('W'))['FROM_ADDRESS'].nunique().cumsum().reset_index()
wallet_growth['BLOCK_TIMESTAMP'] = wallet_growth['BLOCK_TIMESTAMP'].astype(str)

fig_wallet_growth = px.line(wallet_growth, 
                             x='BLOCK_TIMESTAMP', 
                             y='FROM_ADDRESS',
                             title="Cumulative Wallet Growth Over Time",
                             labels={'FROM_ADDRESS': 'Total Unique Wallets', 'BLOCK_TIMESTAMP': 'Week'})
col1.plotly_chart(fig_wallet_growth, use_container_width=True)

# --- Chart 2: Transaction Heatmap (Day vs Hour) ---
data['weekday'] = data['BLOCK_TIMESTAMP'].dt.day_name()
data['hour'] = data['BLOCK_TIMESTAMP'].dt.hour

heatmap_data = data.groupby(['weekday', 'hour']).size().unstack(fill_value=0)
# مرتب سازی روزهای هفته
heatmap_data = heatmap_data.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

fig_heatmap = px.imshow(heatmap_data,
                        labels=dict(x="Hour of Day", y="Day of Week", color="Number of TXs"),
                        title="Transaction Heatmap (Day vs Hour)")
col2.plotly_chart(fig_heatmap, use_container_width=True)

# --- New Row for next charts ---
col3, col4 = st.columns(2)

# --- Chart 3: Top 10 Biggest Transactions ---
top_transactions = data[['FROM_ADDRESS', 'TO_ADDRESS', 'VALUE', 'dominant_persona']].sort_values(by='VALUE', ascending=False).head(10)

col3.subheader("Top 10 Biggest Transactions")
col3.dataframe(top_transactions)

# --- Chart 4: Transaction Size Variability ---
fig_boxplot = px.box(data, 
                     x='dominant_persona', 
                     y='VALUE',
                     title="Transaction Size Variability by Persona",
                     points="outliers")
col4.plotly_chart(fig_boxplot, use_container_width=True)




# ـــ
st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


