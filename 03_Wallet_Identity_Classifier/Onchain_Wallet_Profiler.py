#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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
st.markdown("---")

#‌ـــــــ

metrics_df = pd.read_csv(
    'https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/metrics_df.csv',
    on_bad_lines='skip')

st.subheader("📌 Summary Category")

st.markdown("""
These metrics summarize the **behavior of wallets in the selected category** based on their onchain activity.

- `Avg Tx per Month`: how frequently wallets in this category interact onchain.
- `Unique Function Count`: how many different smart contract functions they tend to call.
- `Unique Contract Count`: how many unique contracts they’ve interacted with.
- `Avg Gas Used`: an estimate of how heavy or complex their transactions are.
""")


selected_metrics = metrics_df[metrics_df['TOP_PROFILE'] == selected_category].squeeze()
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

col1.metric("📊 Avg Tx per Month", f"{selected_metrics['avg_tx_per_month']:.0f}")
col2.metric("🔣 Unique Function Count", f"{selected_metrics['unique_function_count']}")
col3.metric("📜 Unique Contract Count", f"{selected_metrics['unique_contract_count']}")
col4.metric("⛽ Avg Gas Used", f"{selected_metrics['avg_gas_used']:.0f}")

st.subheader("📊 Category Metrics Comparison")

# تعریف رنگ‌ها: فقط دسته انتخاب‌شده رنگی
def colorize(df, selected_category):
    return [
        "#636EFA" if cat == selected_category else "#DDDDDD"
        for cat in df["TOP_PROFILE"]
    ]

# ---------- Chart 1: Avg Tx per Month ----------
fig1 = px.bar(
    metrics_df,
    x="TOP_PROFILE",
    y="avg_tx_per_month",
    title="Avg Tx per Month",
    color_discrete_sequence=colorize(metrics_df, selected_category)
)
fig1.update_layout(showlegend=False)

# ---------- Chart 2: Unique Function Count ----------
fig2 = px.bar(
    metrics_df,
    x="TOP_PROFILE",
    y="unique_function_count",
    title="Unique Function Count",
    color_discrete_sequence=colorize(metrics_df, selected_category)
)
fig2.update_layout(showlegend=False)

# ---------- Chart 3: Unique Contract Count ----------
fig3 = px.bar(
    metrics_df,
    x="TOP_PROFILE",
    y="unique_contract_count",
    title="Unique Contract Count",
    color_discrete_sequence=colorize(metrics_df, selected_category)
)
fig3.update_layout(showlegend=False)

# ---------- Chart 4: Avg Gas Used ----------
fig4 = px.bar(
    metrics_df,
    x="TOP_PROFILE",
    y="avg_gas_used",
    title="Avg Gas Used",
    color_discrete_sequence=colorize(metrics_df, selected_category)
)
fig4.update_layout(showlegend=False)

# نمایش به صورت دو به دو
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    st.plotly_chart(fig4, use_container_width=True)


st.markdown("---")


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

st.markdown("---")
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
st.markdown("---")


weekday_activity = df = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/weekday_activity.csv', on_bad_lines='skip')
hourly_activity = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/hourly_activity.csv',on_bad_lines='skip')
# Clean and ensure correct order
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_activity['WEEKDAY'] = pd.Categorical(weekday_activity['WEEKDAY'], categories=weekday_order, ordered=True)

# Filter data for selected category
filtered_weekday = weekday_activity[weekday_activity['TOP_PROFILE'] == selected_category]
filtered_hourly = hourly_activity[hourly_activity['TOP_PROFILE'] == selected_category]

# Pivot for heatmaps
pivot_weekday = filtered_weekday.pivot(index='TOP_PROFILE', columns='WEEKDAY', values='UNIQUE_WALLETS')
pivot_hourly = filtered_hourly.pivot(index='TOP_PROFILE', columns='HOUR', values='UNIQUE_WALLETS')

# --------------------------------------
# Plot heatmaps
st.subheader("📅 Weekly Activity Pattern")
fig1, ax1 = plt.subplots(figsize=(10, 1.5))
sns.heatmap(pivot_weekday, annot=False, cmap="YlGnBu", cbar=True, ax=ax1)
ax1.set_ylabel("")
ax1.set_xlabel("")
st.pyplot(fig1)

st.subheader("⏰ Hourly Activity Pattern")
fig2, ax2 = plt.subplots(figsize=(10, 1.5))
sns.heatmap(pivot_hourly, annot=False, cmap="YlGnBu", cbar=True, ax=ax2)
ax2.set_ylabel("")
ax2.set_xlabel("")
st.pyplot(fig2)


# ـــ

st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


