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
    # Load data master NIP
    df_master = pd.read_excel("TnQ-Report-2026_Github.xlsx", sheet_name="Master_NIP")
    
    # MENGGABUNGKAN DATA (Merge)
    # Kita gabungkan berdasarkan kolom NIP
    df = pd.merge(df_complaint, df_master[['NIP', 'Division']], on='NIP', how='left')
    return df

df = load_data()

# --- SIDEBAR: FILTER ---
st.sidebar.header("FILTER DATA")
bulan_pilihan = st.sidebar.selectbox("Bulan:", df["Month"].unique())
# Sekarang bisa filter berdasarkan Division yang baru saja di-merge
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
st.subheader("Tren Komplain per Divisi")
div_counts = data_filtered["Division"].value_counts().reset_index()
div_counts.columns = ["Division", "Jumlah"]
fig_div = px.bar(div_counts, x="Division", y="Jumlah", title="Jumlah Komplain per Divisi")
st.plotly_chart(fig_div, use_container_width=True)

# --- TABEL DETAIL ---
st.subheader("Detail Data Komplain")
st.dataframe(data_filtered[["Month", "Division", "Agent", "Project", "Isu Komplain", "Status"]], use_container_width=True)
