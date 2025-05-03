#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/04_Wallet_Canvas/df_final.csv',on_bad_lines='skip')

st.title("📊 Ethereum Wallet Dashboard")


wallet = st.selectbox("Select Wallet Address", df['wallet_address'])
wallet_data = df[df['wallet_address'] == wallet].iloc[0]


col1, col2 = st.columns(2)
with col1:
    st.subheader("🟡 Basic Wallet Information")
    st.write(f"**Wallet Address:** `{wallet_data['wallet_address']}`")
    st.write("💰 ETH Balance", f"{wallet_data['eth']} ETH")
    st.write("📦 Total Transactions (All Time)", wallet_data['tx_count'])
    st.write("📆 Transactions in Last 3 Months", wallet_data['total_tx'])
    st.write(f"**🕒 First Transaction:** {wallet_data['first_tx']}")
    st.write(f"**🕒 Last Transaction:** {wallet_data['last_tx']}")
with col2:
    st.subheader("🟡 Transaction Behavior")
    st.write("**📈 Avg TX Value (ETH):**", f"{round(wallet_data['avg_tx_value']):.6f}")
    st.write("**💵 Avg TX Value (USD):**", f"${round(wallet_data['avg_value_usd']):.2f}")
    st.write("**🗓️ Avg TX per Day:**", f"{round(wallet_data['tx_per_day']):.2f}")
    st.write("**📅 Avg TX per Month:**", f"{round(wallet_data['tx_per_month']):.2f}")
    st.write("**⏳ Avg Time Gap (days):**", f"{wallet_data['avg_time_gap_days']}")

# ـــ
st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


