#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------
# Load main dataset
df = pd.read_csv(
    'https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/04_df_final.csv',
    on_bad_lines='skip'
)

# Load trace dataset (df2) - already aggregated monthly
df2 = pd.read_csv(
    'https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/line_chart.csv',
    on_bad_lines='skip'
)
df2['MONTH'] = pd.to_datetime(df2['MONTH'], errors='coerce')  # ensure it's datetime

# Merge TOP_PROFILE info if not already present
if 'TOP_PROFILE' not in df2.columns:
    df2 = df2.merge(df[['FROM_ADDRESS', 'TOP_PROFILE']].drop_duplicates(), on='FROM_ADDRESS', how='left')

# --------------------------------------
# Streamlit App
st.title("🧠 Onchain Wallet Profiler")

# Emoji mapping for wallet categories
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

# Simulated category distribution for pie chart
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

# Wallet selector
selected_wallet = st.selectbox("🔍 Select a wallet address", df["FROM_ADDRESS"].unique())

# Display selected wallet category
selected_category = df[df["FROM_ADDRESS"] == selected_wallet]["TOP_PROFILE"].values[0]
emoji = category_emojis.get(selected_category, "❓")
st.markdown(f"### 🏷️ Category: **{emoji} {selected_category}**")

# Pie chart: category distribution
fig1, ax1 = plt.subplots(figsize=(6, 6))
ax1.pie(category_distribution.values(), labels=category_distribution.keys(), autopct='%1.1f%%',
        startangle=90, textprops={'fontsize': 6})
ax1.axis('equal')
st.pyplot(fig1)

# --------------------------------------
# Line Chart: Monthly transaction count for selected wallet
wallet_df = df2[df2["FROM_ADDRESS"] == selected_wallet]
tx_per_month = wallet_df.groupby("MONTH").size().reset_index(name="Transaction Count")

st.markdown("### 📊 Monthly Transaction Count for Selected Wallet")
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(tx_per_month["MONTH"], tx_per_month["Transaction Count"], marker='o')
ax2.set_xlabel("Month")
ax2.set_ylabel("Transactions")
ax2.set_title("Monthly Transactions")
ax2.grid(True)
st.pyplot(fig2)

# Line Chart: Category-wise monthly activity
category_per_month = wallet_df.groupby(['MONTH', 'TOP_PROFILE']).size().reset_index(name='Count')

st.markdown("### 📈 Category-wise Monthly Transactions")
fig3, ax3 = plt.subplots(figsize=(10, 5))
for category in category_per_month['TOP_PROFILE'].unique():
    cat_data = category_per_month[category_per_month['TOP_PROFILE'] == category]
    ax3.plot(cat_data['MONTH'], cat_data['Count'], marker='o', label=category)
ax3.set_xlabel("Month")
ax3.set_ylabel("Transactions")
ax3.set_title("Category-wise Monthly Transactions")
ax3.legend(fontsize=6)
ax3.grid(True)
st.pyplot(fig3)

# ـــ


st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


