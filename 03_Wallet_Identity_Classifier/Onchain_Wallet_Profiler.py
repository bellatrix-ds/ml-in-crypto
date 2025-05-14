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

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Wallet_Identity_Classifier/04_df_final.csv',on_bad_lines='skip')

# Streamlit App
st.title("🧠 Onchain Wallet Profiler")

category_emojis = {
    "Dex Trader": "📈",
    "Protocol Dev": "🛠️",
    "Yield Farmer": "🌾",
    "Nft Collector": "🖼️",
    "Oracle User": "🔮",
    "Staker Validator": "🗳️",
    "Defi Farmer": "👨‍🌾",
    "Bot": "🤖",
    "Bridge User": "🌉",
    "Airdrop Hunter": "🎯"
}
selected_wallet = st.selectbox("🔍 Select a wallet address", df["FROM_ADDRESS"].unique())

selected_category = df[df["FROM_ADDRESS"] == selected_wallet]["TOP_PROFILE"].values[0]
emoji = category_emojis.get(selected_category, "❓")
st.markdown(f"### 🏷️ Category: **{emoji} {selected_category}**")
def highlight_selected(row):
    return ['background-color: lightgreen' if row['TOP_PROFILE'] == selected_category else '' for _ in row]

st.markdown("### 📋 All Categories")
df_display = df[["FROM_ADDRESS", "TOP_PROFILE"]]
st.dataframe(df_display.style.apply(highlight_selected, axis=1))


# ـــ


st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


