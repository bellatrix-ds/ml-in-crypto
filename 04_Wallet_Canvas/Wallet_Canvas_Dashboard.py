#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd

df = pd.read_csv("df_final.csv",on_bad_lines='skip')
st.title("📊 Ethereum Wallet Dashboard")

#filter
wallet = st.selectbox("Select Wallet Address", df['wallet_address'])
wallet_data = df[df['wallet_address'] == wallet].iloc[0]

# part1: Basic Wallet Information
st.header("🔹 Basic Wallet Information")
st.write(f"**Wallet Address:** `{wallet_data['wallet_address']}`")
st.metric("💰 ETH Balance", f"{wallet_data['eth']} ETH")
st.metric("📦 Total Transactions (All Time)", wallet_data['tx_count'])
st.metric("📆 Transactions in Last 3 Months", wallet_data['total_tx'])
st.write(f"**🕒 First Transaction:** {wallet_data['first_tx']}")
st.write(f"**🕒 Last Transaction:** {wallet_data['last_tx']}")

# part 2: Transaction Behavio
st.header("🔹 Transaction Behavior")
st.metric("📈 Avg Value per Transaction (ETH)", f"{wallet_data['avg_tx_value']:.6f}")
st.metric("💵 Avg Value per Transaction (USD)", f"${wallet_data['avg_value_usd']:.2f}")
st.metric("🗓️ Avg Transactions per Day", f"{wallet_data['tx_per_day']:.2f}")
st.metric("📅 Avg Transactions per Month", f"{wallet_data['tx_per_month']:.2f}")
st.metric("⏳ Avg Time Between Transactions (days)", f"{wallet_data['avg_time_gap_days']}")



# ـــ
st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


