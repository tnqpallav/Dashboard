import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Layout
st.set_page_config(layout="wide", page_title="Dashboard Komplain")

# Load Data
@st.cache_data
def load_data():
    # Load data komplain
    df_complaint = pd.read_excel("TnQ-Report-2026_Github.xlsx", sheet_name="Complaint")
    # Load data dari sheet "Master Data"
    df_master = pd.read_excel("TnQ-Report-2026_Github.xlsx", sheet_name="Master Data")
    
    # MENGGABUNGKAN DATA (Merge)
    # Pastikan kedua sheet memiliki kolom 'NIP'
    df = pd.merge(df_complaint, df_master[['NIP', 'Division']], on='NIP', how='left')
    return df

df = load_data()

# --- SIDEBAR: FILTER ---
st.sidebar.header("FILTER DATA")
bulan_pilihan = st.sidebar.selectbox("Bulan:", df["Month"].unique())
div_pilihan = st.sidebar.multiselect("Pilih Division:", df["Division"].unique())
project_pilihan = st.sidebar.multiselect("Project:", df["Project"].unique())

# Logika Filter
mask = (df["Month"] == bulan_pilihan)
if div_pilihan:
    mask &= df["Division"].isin(div_pilihan)
if project_pilihan:
    mask &= df["Project"].isin(project_pilihan)

data_filtered = df[mask]

# --- DASHBOARD HEADER ---
st.title("Monitoring Tren Komplain per Divisi")

# Metrik Utama
col1, col2 = st.columns(2)
col1.metric("Total Kasus Komplain", len(data_filtered))
col2.metric("Total Divisi Terdampak", data_filtered["Division"].nunique())

# --- VISUALISASI ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Komplain per Agen (Top 10)")
    top_agents = data_filtered["Agent"].value_counts().head(10).reset_index()
    top_agents.columns = ["Agent", "Jumlah"]
    fig_agent = px.bar(top_agents, x="Jumlah", y="Agent", orientation='h', title="Agen dengan Komplain Terbanyak")
    st.plotly_chart(fig_agent, use_container_width=True)

with col_b:
    st.subheader("Distribusi Komplain per Divisi")
    div_counts = data_filtered["Division"].value_counts().reset_index()
    div_counts.columns = ["Division", "Jumlah"]
    fig_div = px.pie(div_counts, names="Division", values="Jumlah", title="Proporsi per Divisi")
    st.plotly_chart(fig_div, use_container_width=True)

# --- TABEL DETAIL ---
st.subheader("Detail Data Komplain")
st.dataframe(data_filtered[["Month", "Division", "Agent", "Project", "Isu Komplain", "Status"]], use_container_width=True)
