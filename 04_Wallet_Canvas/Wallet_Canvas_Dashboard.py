#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/04_Wallet_Canvas/df_final.csv',on_bad_lines='skip')

st.title("📊 Ethereum Wallet Dashboard")

#filter
wallet = st.selectbox("Select Wallet Address", df['wallet_address'])

wallet_data = df[df['wallet_address'] == wallet].iloc[0]


col1, col2 = st.columns(2)
# part1: Basic Wallet Information
with col1:
    st.subheader("🟡 Basic Wallet Information")
    st.write("**Wallet Address:**", wallet_address)
    st.write("**💰 ETH Balance:**", eth_balance)
    st.write("**📦 Total Transactions (All Time):**", f"{tx_count:,}")
    st.write("**📆 Transactions in Last 3 Months:**", f"{total_tx:,}")
    st.write("**🕒 First TX:**", first_tx)
    st.write("**🕒 Last TX:**", last_tx)
# part 2: Transaction Behavior
with col2:
    st.subheader("🟡 Transaction Behavior")
    st.write("**📈 Avg TX Value (ETH):**", round(avg_tx_value, 4))
    st.write("**💵 Avg TX Value (USD):**", f"${avg_value_usd:,.2f}")
    st.write("**🗓️ Avg TX per Day:**", round(tx_per_day))
    st.write("**📅 Avg TX per Month:**", round(tx_per_month))
    st.write("**⏳ Avg Time Gap (days):**", avg_time_gap_days)

# ـــ
st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


