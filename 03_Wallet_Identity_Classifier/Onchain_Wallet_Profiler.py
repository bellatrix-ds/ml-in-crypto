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

selected_wallet = st.selectbox("Select a wallet address", df["FROM_ADDRESS"].unique())

category = df.loc[df["FROM_ADDRESS"] == selected_wallet, "TOP_PROFILE"].values[0]

st.markdown(f"### 🏷️ Category: `{TOP_PROFILE}`")
# ـــ


st.markdown("---")
st.caption("Contact me: bellabahramii@gmail.com")


