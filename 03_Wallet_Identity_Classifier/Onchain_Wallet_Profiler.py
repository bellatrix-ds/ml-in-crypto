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
# Load main data
df = pd.read_csv(
    'https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/04_df_final.csv',
    on_bad_lines='skip')

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

# Load df2 (your trace dataset)
df2 = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/04_df_row.csv',
                  on_bad_lines='skip')
df2['BLOCK_TIMESTAMP'] = pd.to_datetime(df2['BLOCK_TIMESTAMP'], errors='coerce')
df2.dropna(subset=['BLOCK_TIMESTAMP'], inplace=True)

# Streamlit App
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

# Category and emoji
selected_category = df[df["FROM_ADDRESS"] == selected_wallet]["TOP_PROFILE"].values[0]
emoji = category_emojis.get(selected_category, "❓")
st.markdown(f"### 🏷️ Category: **{emoji} {selected_category}**")

# Pie chart: category distribution
fig1, ax1 = plt.subplots(figsize=(6, 6))
ax1.pie(category_distribution.values(), labels=category_distribution.keys(), autopct='%1.1f%%',
        startangle=90, textprops={'fontsize': 6})
ax1.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
st.pyplot(fig1)




# انتخاب کیف پول و کتگوری
selected_wallet = st.selectbox("🔍 Select a wallet address", df["FROM_ADDRESS"].unique())
selected_category = df[df["FROM_ADDRESS"] == selected_wallet]["TOP_PROFILE"].values[0]

# تراکنش‌های این کیف پول
wallet_monthly = (
    df2[df2["FROM_ADDRESS"] == selected_wallet]
    .groupby("month")["TX_HASH"]
    .count()
    .rename("Selected Wallet")
)

# تراکنش‌های همه کیف پول‌های این کتگوری
category_wallets = df[df["TOP_PROFILE"] == selected_category]["FROM_ADDRESS"].unique()

category_monthly = (
    df2[df2["FROM_ADDRESS"].isin(category_wallets)]
    .groupby("month")["TX_HASH"]
    .count()
    .rename(f"All {selected_category}s")
)

# ترکیب
df_monthly = pd.concat([wallet_monthly, category_monthly], axis=1).fillna(0)

# 📊 رسم لاین چارت دقیق
st.markdown("### 📆 Monthly Transaction Activity")
st.line_chart(df_monthly)
# ـــ


st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


