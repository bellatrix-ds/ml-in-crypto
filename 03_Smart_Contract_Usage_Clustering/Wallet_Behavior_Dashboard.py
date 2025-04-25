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
# --------------------------------------


# Sidebar Filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df["BLOCK_TIMESTAMP"].min().date())
end_date = st.sidebar.date_input("End Date", df["BLOCK_TIMESTAMP"].max().date())
selected_personas = st.sidebar.multiselect("Select Personas", df["dominant_persona"].unique(), default=df["dominant_persona"].unique())

# Filter data
mask = (df["BLOCK_TIMESTAMP"].dt.date >= start_date) & (df["BLOCK_TIMESTAMP"].dt.date <= end_date) & (df["dominant_persona"].isin(selected_personas))
df_filtered = df[mask]

# Pie Chart: Persona Distribution
pie_data = df_filtered["dominant_persona"].value_counts().reset_index()
pie_data.columns = ["Persona", "Count"]
fig_pie = px.pie(pie_data, names="Persona", values="Count", title="Persona Market Share")

# Clustered Bar Chart: Behavior Comparison
agg_data = df_filtered.groupby("dominant_persona").agg({"VALUE":"mean", "GAS":"mean", "GAS_USED":"mean"}).reset_index()
fig_bar = px.bar(agg_data, x="dominant_persona", y=["VALUE", "GAS", "GAS_USED"], barmode="group", title="Avg VALUE / GAS / GAS_USED per Persona")

# Time Series Line Chart
df_filtered["Date"] = df_filtered["BLOCK_TIMESTAMP"].dt.date
time_series = df_filtered.groupby(["Date", "dominant_persona"]).size().reset_index(name="Tx Count")
fig_time = px.line(time_series, x="Date", y="Tx Count", color="dominant_persona", title="Daily Activity per Persona")

# Heatmap
df_filtered["Hour"] = df_filtered["BLOCK_TIMESTAMP"].dt.hour
heatmap_data = df_filtered.groupby(["dominant_persona", "Hour"]).size().reset_index(name="Count")
fig_heatmap = px.density_heatmap(heatmap_data, x="Hour", y="dominant_persona", z="Count", nbinsx=24, title="Hourly Activity Heatmap")

# Radar Chart
radar_data = df_filtered.groupby("dominant_persona").agg({"VALUE":"mean", "GAS":"mean", "GAS_USED":"mean"}).reset_index()
fig_radar = go.Figure()
for i in range(len(radar_data)):
    fig_radar.add_trace(go.Scatterpolar(
        r=[radar_data.loc[i, "VALUE"], radar_data.loc[i, "GAS"], radar_data.loc[i, "GAS_USED"]],
        theta=["VALUE", "GAS", "GAS_USED"],
        fill='toself',
        name=radar_data.loc[i, "dominant_persona"]
    ))
fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), title="Radar Comparison of Personas")

# Top Wallets
top_wallets = df_filtered.groupby("FROM_ADDRESS")["VALUE"].sum().sort_values(ascending=False).head(10).reset_index()
fig_top_wallets = px.bar(top_wallets, x="FROM_ADDRESS", y="VALUE", title="Top 10 Wallets by Total Value")

# ---------------- Layout ----------------

# Row 1
st.header("📊 Market Overview")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Persona Distribution (Pie Chart)")
    st.plotly_chart(fig_pie, use_container_width=True)
with col2:
    st.subheader("Behavior Comparison (Bar Chart)")
    st.plotly_chart(fig_bar, use_container_width=True)

# Row 2
st.header("📈 Temporal Activity")
col3, col4 = st.columns(2)
with col3:
    st.subheader("Activity Over Time (Line Chart)")
    st.plotly_chart(fig_time, use_container_width=True)
with col4:
    st.subheader("Hourly Heatmap")
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Row 3
st.header("🧠 Deep Persona Analysis")
col5, col6 = st.columns(2)
with col5:
    st.subheader("Radar Chart")
    st.plotly_chart(fig_radar, use_container_width=True)
with col6:
    st.subheader("Top 10 Wallets")
    st.plotly_chart(fig_top_wallets, use_container_width=True)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit and Plotly")


