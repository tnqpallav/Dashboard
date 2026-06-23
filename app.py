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
    
    # CEK KOLOM (Penting untuk debugging)
    # Jika aplikasi error, ini akan memunculkan daftar kolom yang benar di layar
    required_cols = ['NIP', 'Division', 'TL']
    missing_cols = [col for col in required_cols if col not in df_master.columns]
    
    if missing_cols:
        st.error(f"Kolom berikut tidak ditemukan di sheet 'Master Data': {missing_cols}")
        st.write("Kolom yang tersedia di Master Data:", df_master.columns.tolist())
        st.stop() # Menghentikan aplikasi agar tidak lanjut error

    # Menggabungkan data
    df = pd.merge(df_complaint, df_master[['NIP', 'Division', 'TL']], on='NIP', how='left')
    return df

df = load_data()

# --- SIDEBAR: FILTER ---
st.sidebar.header("FILTER DATA")
bulan_list = sorted(df["Month"].unique().tolist(), reverse=True)[:3]
bulan_pilihan = st.sidebar.multiselect("Pilih Bulan (3 Terakhir):", bulan_list, default=bulan_list[0])
div_pilihan = st.sidebar.multiselect("Pilih Division:", df["Division"].unique())
tl_pilihan = st.sidebar.multiselect("Pilih Team Leader (TL):", df["TL"].unique())

# Logika Filter
mask = df["Month"].isin(bulan_pilihan)
if div_pilihan: mask &= df["Division"].isin(div_pilihan)
if tl_pilihan: mask &= df["TL"].isin(tl_pilihan)

data_filtered = df[mask]

# --- DASHBOARD HEADER ---
st.title("Dashboard Monitoring Komplain")
col1, col2, col3 = st.columns(3)
col1.metric("Total Komplain", len(data_filtered))
col2.metric("Divisi Terdampak", data_filtered["Division"].nunique())
col3.metric("TL Terlibat", data_filtered["TL"].nunique())
st.divider()

# --- VISUALISASI ---
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Tren Komplain (3 Bulan)")
    tren = data_filtered.groupby("Month").size().reset_index(name="Jumlah")
    st.plotly_chart(px.line(tren, x="Month", y="Jumlah", markers=True), use_container_width=True)

with col_b:
    st.subheader("Komplain per TL")
    tl_counts = data_filtered["TL"].value_counts().reset_index()
    tl_counts.columns = ["TL", "Jumlah"]
    st.plotly_chart(px.bar(tl_counts, x="Jumlah", y="TL", orientation='h'), use_container_width=True)

# --- ANALISIS ISU ---
st.subheader("Tren Kasus Komplain")
isu = data_filtered["Isu Komplain"].value_counts().reset_index()
isu.columns = ["Isu Komplain", "Jumlah"]
st.plotly_chart(px.bar(isu, x="Jumlah", y="Isu Komplain", orientation='h', text="Jumlah"), use_container_width=True)

# --- TABEL DETAIL ---
with st.expander("Lihat Data Detail"):
    st.dataframe(data_filtered[["Month", "TL", "Division", "Agent", "Isu Komplain", "Status"]], use_container_width=True)
