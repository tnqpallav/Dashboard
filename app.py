import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Layout Halaman
st.set_page_config(layout="wide", page_title="Dashboard Operasional")

# Load Data
@st.cache_data
def load_data():
    # Pastikan file TnQ-Report-2026_Github.xlsx ada di folder yang sama
    return pd.read_excel("TnQ-Report-2026_Github.xlsx", sheet_name="Complaint")

df = load_data()

# --- SIDEBAR: FILTER ---
st.sidebar.header("FILTER DATA")
bulan_pilihan = st.sidebar.selectbox("Bulan:", df["Month"].unique())
project_pilihan = st.sidebar.multiselect("Project:", df["Project"].unique())
status_pilihan = st.sidebar.multiselect("Status:", df["Status"].unique())

# Logika Filter Data
mask = (df["Month"] == bulan_pilihan)
if project_pilihan:
    mask &= df["Project"].isin(project_pilihan)
if status_pilihan:
    mask &= df["Status"].isin(status_pilihan)

data_filtered = df[mask]

# --- DASHBOARD HEADER ---
st.title("Monitoring Komplain & Pinalti")

# Metrik Utama
col1, col2, col3 = st.columns(3)
col1.metric("Total Komplain", len(data_filtered))
col2.metric("Total Pinalti (IDR)", f"{data_filtered['Pinalti'].sum():,.0f}")
col3.metric("Avg. Pinalti per Kejadian", f"{data_filtered['Pinalti'].mean():,.0f}")

# --- VISUALISASI ---
st.subheader("Tren Komplain per Project")

# Grafik Bar dengan pewarnaan berdasarkan intensitas pinalti
fig = px.bar(
    data_filtered, 
    x="Project", 
    y="Pinalti", 
    color="Pinalti", 
    color_continuous_scale="RdYlGn_r", # Merah (Tinggi/Bahaya) ke Hijau (Rendah)
    title="Distribusi Pinalti per Project"
)
st.plotly_chart(fig, use_container_width=True)

# Tabel Data dengan Conditional Formatting
st.subheader("Data Detail Komplain")

def color_penalty(val):
    # Mengembalikan warna merah jika pinalti > 2.000.000, hijau jika sebaliknya
    color = 'red' if val > 2000000 else 'green'
    return f'color: {color}'

st.dataframe(
    data_filtered[["Agent", "Project", "Isu Komplain", "Pinalti", "Status"]]
    .style.applymap(color_penalty, subset=['Pinalti']),
    use_container_width=True
)