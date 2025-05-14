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

# Simulated category distribution for pie chart (replace with actual counts if available)
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
fig1, ax1 = plt.subplots()
ax1.pie(category_distribution.values(), labels=category_distribution.keys(), autopct='%1.1f%%',
        startangle=90, textprops={'fontsize': 8})
ax1.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
st.pyplot(fig1)

# Line chart: daily activity
wallet_df = df2[df2['FROM_ADDRESS'] == selected_wallet].copy()
wallet_df['DATE'] = wallet_df['BLOCK_TIMESTAMP'].dt.date
wallet_counts = wallet_df.groupby('DATE')['TX_HASH'].count().reset_index(name='wallet_tx_count')

same_cat_wallets = df[df['TOP_PROFILE'] == selected_category]['FROM_ADDRESS'].unique()
same_cat_df = df2[df2['FROM_ADDRESS'].isin(same_cat_wallets)].copy()
same_cat_df['DATE'] = same_cat_df['BLOCK_TIMESTAMP'].dt.date
cat_counts = same_cat_df.groupby('DATE')['TX_HASH'].count().reset_index(name='category_tx_count')

# Merge for chart
tx_compare = pd.merge(wallet_counts, cat_counts, on='DATE', how='outer').fillna(0)

# Plot
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=tx_compare, x='DATE', y='wallet_tx_count', label='Selected Wallet', ax=ax2)
sns.lineplot(data=tx_compare, x='DATE', y='category_tx_count', label=f'All {selected_category} Wallets', ax=ax2)
ax2.set_title("⏰ Daily Transaction Count")
ax2.set_ylabel("Transactions")
ax2.set_xlabel("Date")
ax2.tick_params(axis='x', rotation=45)
ax2.legend()
st.pyplot(fig2)


# ـــ


st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


