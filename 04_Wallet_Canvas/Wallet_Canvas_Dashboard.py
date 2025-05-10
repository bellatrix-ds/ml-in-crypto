#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
from datetime import datetime

df = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/04_Wallet_Canvas/df_final.csv',on_bad_lines='skip')

st.title("📊 ETH Wallet Insights & Patterns")

# Wallet selector
wallet = st.selectbox("🔎 Select a Wallet Address", df['wallet_address'])
wallet_data = df[df['wallet_address'] == wallet].iloc[0]


# 🧾 Basic Wallet Information
st.header("📘 Basic Wallet Information")
st.write(f"**🔐 Wallet Address:** `{wallet_data['wallet_address']}`")
st.write("💰 **ETH Balance:**", f"{wallet_data['eth']} ETH")
st.write("📦 **Total Transactions (All Time):**", wallet_data['tx_count'])
st.write("📆 **Transactions in Last 3 Months:**", wallet_data['total_tx'])
st.write(f"🕒 **First Transaction:** {wallet_data['first_tx']}")
st.write(f"🕓 **Last Transaction:** {wallet_data['last_tx']}")

# 🔁 Transaction Behavior
st.header("📊 Transaction Behavior")
st.write("📈 **Avg TX Value (ETH):**", f"{wallet_data['avg_tx_value']:.6f}")
st.write("💵 **Avg TX Value (USD):**", f"${wallet_data['avg_value_usd']:.2f}")
st.write("🗓️ **Avg TX per Day:**", f"{wallet_data['tx_per_day']:.2f}")
st.write("📅 **Avg TX per Month:**", f"{wallet_data['tx_per_month']:.2f}")
st.write("⏳ **Avg Time Gap (days):**", f"{wallet_data['avg_time_gap_days']}")

# New Metric: TX activity rate
tx_activity_rate = round(wallet_data['total_tx'] / wallet_data['tx_count'] * 100, 2)
st.write("📊 **Recent Activity Rate (Last 3mo vs All):**", f"{tx_activity_rate}%")


# part 3
import altair as alt

filtered_df3 = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/04_Wallet_Canvas/part3_data.csv')
st.header("📈 Wallet Activity Overview")

# تبدیل ماه به نوع datetime برای نمودار دقیق‌تر
filtered_df3['month'] = pd.to_datetime(filtered_df3['month'])
df_wallet = filtered_df3[filtered_df3['wallet_address'] == wallet]


col1, col2 = st.columns(2)

with col1:
    st.subheader("🔁 Monthly Transaction Count")
    tx_chart = alt.Chart(filtered_df3).mark_line(point=True).encode(
        x=alt.X('month:T', title='Month'),
        y=alt.Y('tx_count:Q', title='Transactions'),
        tooltip=['month:T', 'tx_count']
    ).properties(width=350, height=300)
    st.altair_chart(tx_chart, use_container_width=True)

with col2:
    st.subheader("💰 ETH Balance Over Time")
    balance_chart = alt.Chart(filtered_df3).mark_line(point=True).encode(
        x=alt.X('month:T', title='Month'),
        y=alt.Y('eth_balance:Q', title='ETH Balance'),
        tooltip=['month:T', 'eth_balance']
    ).properties(width=350, height=300)
    st.altair_chart(balance_chart, use_container_width=True)

# ـــ
st.markdown("---")
st.caption("📧 Contact me: bellabahramii@gmail.com")


