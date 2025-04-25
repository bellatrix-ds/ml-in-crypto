#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Wallet Behavior Dashboard", layout="wide")

# Load data
url = "https://raw.githubusercontent.com/bellatrix-ds/ml-in-crypto/refs/heads/main/03_Smart_Contract_Usage_Clustering/data.csv"

df = pd.read_csv(url, on_bad_lines='skip')  
# Convert BLOCK_TIMESTAMP to datetime
df["BLOCK_TIMESTAMP"] = pd.to_datetime(df["BLOCK_TIMESTAMP"], errors="coerce")
df = df.dropna(subset=["BLOCK_TIMESTAMP"])
st.title("📊 Wallet Behavior Dashboard")



# Sidebar Filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df["BLOCK_TIMESTAMP"].min())
end_date = st.sidebar.date_input("End Date", df["BLOCK_TIMESTAMP"].max())
selected_personas = st.sidebar.multiselect("Select Personas", df["dominant_persona"].unique(), default=df["dominant_persona"].unique())

# Filter data
mask = (df["BLOCK_TIMESTAMP"].dt.date >= start_date) & (df["BLOCK_TIMESTAMP"].dt.date <= end_date) & (df["dominant_persona"].isin(selected_personas))
df_filtered = df[mask]



# --------------------------------------
# 1. Pie Chart: Persona Distribution
st.header("🍰 Persona Distribution")
pie_data = df_filtered["dominant_persona"].value_counts().reset_index()
pie_data.columns = ["Persona", "Count"]
fig_pie = px.pie(pie_data, names="Persona", values="Count", title="Persona Market Share")
st.plotly_chart(fig_pie)

