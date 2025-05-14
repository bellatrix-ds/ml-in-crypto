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
    "Protocol Dev": "🖠️",
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
    name="Wallet Transactions",
    line=dict(color="blue", width=2)
))

fig.add_trace(go.Scatter(
    x=merged["MONTH_LABEL"],
    y=merged["category_tx_count"],
    mode="lines+markers",
    name=f"{selected_category} Transactions",
    line=dict(color="orange", width=2, dash="dash")
))

fig.update_layout(
    title="📊 Monthly Transactions",
    xaxis_title="Month",
    yaxis_title="Transaction Count",
    legend_title="Legend",
    hovermode="x unified",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ـــ


st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


