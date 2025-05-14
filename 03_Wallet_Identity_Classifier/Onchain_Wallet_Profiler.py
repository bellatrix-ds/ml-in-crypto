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
df2 = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/line_chart.csv',
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



# Line chart
df2['MONTH'] = df2['BLOCK_TIMESTAMP'].dt.to_period('M').dt.to_timestamp()

# Filter by selected wallet
wallet_df = df2[df2["FROM_ADDRESS"] == selected_wallet]

# Group by MONTH and count transactions
tx_per_month = wallet_df.groupby("MONTH").size().reset_index(name="Transaction Count")

# Optional: also count category-wise if df2 includes TOP_PROFILE column
# If not, merge category info from df to df2
if 'TOP_PROFILE' not in df2.columns:
    df2 = df2.merge(df[['FROM_ADDRESS', 'TOP_PROFILE']].drop_duplicates(), on='FROM_ADDRESS', how='left')
    wallet_df = df2[df2["FROM_ADDRESS"] == selected_wallet]

# Group by MONTH and CATEGORY
category_per_month = wallet_df.groupby(['MONTH', 'TOP_PROFILE']).size().reset_index(name='Count')

# Draw line chart: total transaction count per month
st.markdown("### 📊 Monthly Transaction Count for Selected Wallet")
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(tx_per_month['MONTH'], tx_per_month['Transaction Count'], marker='o')
ax2.set_xlabel("Month")
ax2.set_ylabel("Number of Transactions")
ax2.set_title(f"Monthly Transactions for Wallet {selected_wallet[:6]}...")
ax2.grid(True)
st.pyplot(fig2)

# Draw line chart: category breakdown
st.markdown("### 📈 Category-wise Transaction Count per Month")
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


