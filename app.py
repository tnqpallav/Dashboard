import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Layout Halaman
st.set_page_config(layout="wide", page_title="Dashboard Monitoring Komplain")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Pastikan file Excel berada di folder yang sama
    file_path = "TnQ-Report-2026_Github.xlsx"
    df_complaint = pd.read_excel(file_path, sheet_name="Complaint")
    df_master = pd.read_excel(file_path, sheet_name="Master Data")
    
    # Menggabungkan data (Merge) berdasarkan NIP
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
st.title("Dashboard Monitoring Komplain")

# Metrik Utama
col1, col2, col3 = st.columns(3)
col1.metric("Total Komplain", len(data_filtered))
col2.metric("Divisi Terdampak", data_filtered["Division"].nunique())
col3.metric("Agen Unik", data_filtered["Agent"].nunique())

st.divider()

# --- VISUALISASI ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Agen dengan Komplain Terbanyak (Top 10)")
    top_agents = data_filtered["Agent"].value_counts().head(10).reset_index()
    top_agents.columns = ["Agent", "Jumlah"]
    fig_agent = px.bar(top_agents, x="Jumlah", y="Agent", orientation='h', title="Top 10 Agen")
    st.plotly_chart(fig_agent, use_container_width=True)

with col_b:
    st.subheader("Proporsi per Divisi")
    div_counts = data_filtered["Division"].value_counts().reset_index()
    div_counts.columns = ["Division", "Jumlah"]
    fig_div = px.pie(div_counts, names="Division", values="Jumlah", title="Distribusi per Divisi")
    st.plotly_chart(fig_div, use_container_width=True)

# --- ANALISIS TREN ISU KOMPLAIN ---
st.subheader("Tren Kasus Komplain")
isu_counts = data_filtered["Isu Komplain"].value_counts().reset_index()
isu_counts.columns = ["Isu Komplain", "Jumlah"]

fig_isu = px.bar(
    isu_counts, 
    x="Jumlah", 
    y="Isu Komplain", 
    orientation='h', 
    title="Frekuensi Jenis Isu Komplain",
    text="Jumlah"
)
fig_isu.update_traces(textposition='outside')
st.plotly_chart(fig_isu, use_container_width=True)

# --- TABEL DETAIL ---
with st.expander("Lihat Data Detail Komplain"):
    st.dataframe(data_filtered[["Month", "Division", "Agent", "Project", "Isu Komplain", "Status"]], use_container_width=True)
