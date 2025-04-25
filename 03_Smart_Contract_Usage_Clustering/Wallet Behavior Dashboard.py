#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Wallet Behavior Dashboard", layout="wide")

# Load data
df = pd.read_csv("final_clustered_wallets.csv")
st.title("📊 Wallet Behavior Dashboard")

# Cluster distribution
st.header("Cluster Distribution")
cluster_counts = df["cluster"].value_counts().sort_index().reset_index()
cluster_counts.columns = ["Cluster", "Count"]
st.plotly_chart(px.bar(cluster_counts, x="Cluster", y="Count", text="Count",
                      color="Cluster", title="Number of Wallets per Cluster"))

# Most common values per cluster
st.header("Top Features per Cluster")
selected_feature = st.selectbox("Choose a feature to compare across clusters", df.columns[1:-1])
top_features = df.groupby("cluster")[selected_feature].agg(lambda x: x.value_counts().index[0]).reset_index()
st.dataframe(top_features, use_container_width=True)

# Explore a cluster in detail
st.header("Explore Cluster Details")
selected_cluster = st.selectbox("Select a cluster", sorted(df["cluster"].unique()))
st.subheader(f"Wallets in Cluster {selected_cluster}")
st.dataframe(df[df["cluster"] == selected_cluster], use_container_width=True)

# Pie charts for selected cluster
st.header("Feature Distributions in Selected Cluster")
col1, col2 = st.columns(2)
with col1:
    feature1 = st.selectbox("Feature 1", df.columns[1:-1], key="f1")
    fig1 = px.pie(df[df["cluster"] == selected_cluster], names=feature1, title=f"{feature1} Distribution")
    st.plotly_chart(fig1)
with col2:
    feature2 = st.selectbox("Feature 2", df.columns[1:-1], key="f2")
    fig2 = px.pie(df[df["cluster"] == selected_cluster], names=feature2, title=f"{feature2} Distribution")
    st.plotly_chart(fig2)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit and Plotly")

