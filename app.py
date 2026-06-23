import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Layout
st.set_page_config(layout="wide", page_title="Dashboard Komplain")

# Load Data
@st.cache_data
def load_data():
    return pd.read_excel("TnQ-Report-2026_Github.xlsx", sheet_name="Complaint")

df = load_data()

# --- SIDEBAR: FILTER ---
st.sidebar.header("FILTER DATA")
bulan_pilihan = st.sidebar.selectbox("Bulan:", df["Month"].unique())
# Menambahkan filter Tim (Recovery/M1)
tim_pilihan = st.sidebar.multiselect("Pilih Tim:", df["Team"].unique())
project_pilihan = st.sidebar.multiselect("Project:", df["Project"].unique())

# Logika Filter
mask = (df["Month"] == bulan_pilihan)
if tim_pilihan:
    mask &= df["Team"].isin(tim_pilihan)
if project_pilihan:
    mask &= df["Project"].isin(project_pilihan)

data_filtered = df[mask]

# --- DASHBOARD HEADER ---
st.title("Monitoring Tren Komplain")

# Metrik Utama
col1, col2 = st.columns(2)
col1.metric("Total Kasus Komplain", len(data_filtered))
col2.metric("Jumlah Agen Terdampak", data_filtered["Agent"].nunique())

# --- VISUALISASI ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Komplain per Agen (Top 10)")
    # Menghitung agen dengan komplain terbanyak
    top_agents = data_filtered["Agent"].value_counts().head(10).reset_index()
    top_agents.columns = ["Agent", "Jumlah"]
    fig_agent = px.bar(top_agents, x="Jumlah", y="Agent", orientation='h', title="Agen dengan Komplain Terbanyak")
    st.plotly_chart(fig_agent, use_container_width=True)

with col_b:
    st.subheader("Distribusi Jenis Kasus")
    kasus_counts = data_filtered["Isu Komplain"].value_counts().reset_index()
    kasus_counts.columns = ["Isu Komplain", "Jumlah"]
    fig_kasus = px.pie(kasus_counts, names="Isu Komplain", values="Jumlah", title="Jenis Kasus Komplain")
    st.plotly_chart(fig_kasus, use_container_width=True)

# --- TABEL DETAIL ---
st.subheader("Detail Data Komplain")
st.dataframe(data_filtered[["Month", "Team", "Agent", "Project", "Isu Komplain", "Status"]], use_container_width=True)
