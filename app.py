import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Layout
st.set_page_config(layout="wide", page_title="Dashboard Monitoring Komplain")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    file_path = "TnQ-Report-2026_Github.xlsx"
    df_complaint = pd.read_excel(file_path, sheet_name="Complaint")
    df_master = pd.read_excel(file_path, sheet_name="Master Data")
    
    # Menggabungkan data (Merge) berdasarkan NIP
    # Pastikan di Master Data ada kolom NIP, Division, dan TL
    df = pd.merge(df_complaint, df_master[['NIP', 'Division', 'TL']], on='NIP', how='left')
    return df

df = load_data()

# --- SIDEBAR: FILTER ---
st.sidebar.header("FILTER DATA")
# Filter untuk 3 bulan terakhir (asumsi kolom Month berisi angka/nama bulan)
bulan_list = sorted(df["Month"].unique().tolist(), reverse=True)[:3]
bulan_pilihan = st.sidebar.multiselect("Pilih 3 Bulan Terakhir:", bulan_list, default=bulan_list[0])

div_pilihan = st.sidebar.multiselect("Pilih Division:", df["Division"].unique())
tl_pilihan = st.sidebar.multiselect("Pilih Team Leader (TL):", df["TL"].unique())

# Logika Filter
mask = df["Month"].isin(bulan_pilihan)
if div_pilihan:
    mask &= df["Division"].isin(div_pilihan)
if tl_pilihan:
    mask &= df["TL"].isin(tl_pilihan)

data_filtered = df[mask]

# --- DASHBOARD HEADER ---
st.title("Dashboard Monitoring Komplain")

# Metrik Utama
col1, col2, col3 = st.columns(3)
col1.metric("Total Komplain", len(data_filtered))
col2.metric("Divisi Terdampak", data_filtered["Division"].nunique())
col3.metric("TL Terlibat", data_filtered["TL"].nunique())

st.divider()

# --- VISUALISASI ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Tren Komplain (3 Bulan)")
    # Grouping data berdasarkan bulan
    tren_data = data_filtered.groupby("Month").size().reset_index(name="Jumlah")
    fig_line = px.line(tren_data, x="Month", y="Jumlah", markers=True, title="Tren Volume Komplain")
    st.plotly_chart(fig_line, use_container_width=True)

with col_b:
    st.subheader("Komplain per Team Leader")
    tl_counts = data_filtered["TL"].value_counts().reset_index()
    tl_counts.columns = ["TL", "Jumlah"]
    fig_tl = px.bar(tl_counts, x="Jumlah", y="TL", orientation='h', title="Distribusi Komplain per TL")
    st.plotly_chart(fig_tl, use_container_width=True)

# --- ANALISIS ISU ---
st.subheader("Tren Kasus Komplain")
isu_counts = data_filtered["Isu Komplain"].value_counts().reset_index()
isu_counts.columns = ["Isu Komplain", "Jumlah"]

fig_isu = px.bar(isu_counts, x="Jumlah", y="Isu Komplain", orientation='h', title="Frekuensi Jenis Isu", text="Jumlah")
fig_isu.update_traces(textposition='outside')
st.plotly_chart(fig_isu, use_container_width=True)

# --- TABEL DETAIL ---
with st.expander("Lihat Data Detail"):
    st.dataframe(data_filtered[["Month", "TL", "Division", "Agent", "Isu Komplain", "Status"]], use_container_width=True)
