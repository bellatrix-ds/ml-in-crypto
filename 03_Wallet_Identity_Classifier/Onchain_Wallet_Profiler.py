#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --------------------------------------
# Load main dataset
df = pd.read_csv(
    'https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/04_df_final.csv',
    on_bad_lines='skip'
)

# Load trace dataset (df2) - already monthly
df2 = pd.read_csv(
    'https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/line_chart.csv',
    on_bad_lines='skip'
)
df2['MONTH'] = pd.to_datetime(df2['MONTH'], errors='coerce')

# Merge TOP_PROFILE into df2
if 'TOP_PROFILE' not in df2.columns:
    df2 = df2.merge(df[['FROM_ADDRESS', 'TOP_PROFILE']].drop_duplicates(), on='FROM_ADDRESS', how='left')

# --------------------------------------
# Streamlit UI
st.title("🧠 Onchain Wallet Profiler")

category_emojis = {
    "Dex Trader": "📈",
    "Protocol Dev": "🛠️",
    "Yield Farmer": "🌾",
    "Nft Collector": "🔼️",
    "Oracle User": "🔮",
    "Staker Validator": "🗳️",
    "Defi Farmer": "👨‍🌾",
    "Bot": "🤖",
    "Bridge User": "🌉",
    "Airdrop Hunter": "🎯"
}

# Wallet selector
selected_wallet = st.selectbox("🔍 Select a wallet address", df["FROM_ADDRESS"].unique())

# Category for selected wallet
selected_category = df[df["FROM_ADDRESS"] == selected_wallet]["TOP_PROFILE"].values[0]
emoji = category_emojis.get(selected_category, "❓")
st.markdown(f"### 🏷️ Category: **{emoji} {selected_category}**")

# --------------------------------------
# Simulated market share
category_distribution = {
    "Dex Trader": 30,
    "Protocol Dev": 2,
    "Yield Farmer": 10,
    "Nft Collector": 15,
    "Oracle User": 5,
    "Staker Validator": 9,
    "Defi Farmer": 10,
    "Bot": 2,
    "Bridge User": 12,
    "Airdrop Hunter": 10
}
market_share = category_distribution.get(selected_category, 0)
st.markdown(f"### 📊 Market Share: **{market_share}%**")

# --------------------------------------
# Line chart data preparation

# Data for selected wallet
wallet_df = df2[df2["FROM_ADDRESS"] == selected_wallet]
wallet_counts = wallet_df.groupby("MONTH").size().reset_index(name="wallet_tx_count")

# Data for category
category_df = df2[df2["TOP_PROFILE"] == selected_category]
category_counts = category_df.groupby("MONTH").size().reset_index(name="category_tx_count")

# Merge both time series
merged = pd.merge(wallet_counts, category_counts, on="MONTH", how="outer").fillna(0)
merged = merged.sort_values("MONTH")
merged["MONTH_LABEL"] = merged["MONTH"].dt.strftime('%b-%Y')  # e.g., Jan-2023

# --------------------------------------
# Plotly line chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=merged["MONTH_LABEL"],
    y=merged["wallet_tx_count"],
    mode="lines+markers",
    name="Select Wallet Transactions",
    line=dict(color="blue", width=2)
))

fig.add_trace(go.Scatter(
    x=merged["MONTH_LABEL"],
    y=merged["category_tx_count"],
    mode="lines+markers",
    name=f"{selected_category} Category",
    line=dict(color="orange", width=2, dash="dash")
))

fig.update_layout(
    title="👛 Wallet Tx Count",
    xaxis_title="Month",
    yaxis_title="Transaction Count",
    legend_title="Legend",
    hovermode="x unified",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ____________

weekday_activity = df = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/weekday_activity.csv', on_bad_lines='skip')
hourly_activity = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/hourly_activity.csv',on_bad_lines='skip')

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_activity['WEEKDAY'] = pd.Categorical(weekday_activity['WEEKDAY'], categories=weekday_order, ordered=True)

all_profiles = sorted(weekday_activity['TOP_PROFILE'].unique())
selected_profile = st.selectbox("Select a wallet category (TOP_PROFILE):", all_profiles)
filtered_weekday = weekday_activity[weekday_activity['TOP_PROFILE'] == selected_profile]
filtered_hourly = hourly_activity[hourly_activity['TOP_PROFILE'] == selected_profile]
pivot_weekday = filtered_weekday.pivot(index='TOP_PROFILE', columns='WEEKDAY', values='UNIQUE_WALLETS')
pivot_hourly = filtered_hourly.pivot(index='TOP_PROFILE', columns='HOUR', values='UNIQUE_WALLETS')

col1, col2 = st.columns(2)

with col1:
    st.subheader("Activity by Weekday")
    fig1, ax1 = plt.subplots(figsize=(10, 2))
    sns.heatmap(pivot_weekday, annot=True, fmt="d", cmap="YlGnBu", ax=ax1)
    st.pyplot(fig1)

with col2:
    st.subheader("Activity by Hour of Day")
    fig2, ax2 = plt.subplots(figsize=(10, 2))
    sns.heatmap(pivot_hourly, annot=True, fmt="d", cmap="YlGnBu", ax=ax2)
    st.pyplot(fig2)


st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


