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

wallets = df["FROM_ADDRESS"].unique()
selected_wallet = st.selectbox("🔍 Select a wallet address", wallets)
selected_category = df[df["FROM_ADDRESS"] == selected_wallet]["TOP_PROFILE"].values[0]

category_table = pd.DataFrame({
    "Category": list(category_emojis.keys()),
    "Emoji": [category_emojis[cat] for cat in category_emojis.keys()]
})

def highlight_selected(row):
    if row["Category"] == selected_category:
        return ['background-color: lightgreen', 'background-color: lightgreen']
    return ['', '']

st.markdown("### 🧠 Categories")
st.dataframe(category_table.style.apply(highlight_selected, axis=1))

# ـــ


st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


