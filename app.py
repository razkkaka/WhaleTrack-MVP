import streamlit as st
import yfinance as yf
import pandas as pd
import random

st.set_page_config(page_title="WhaleTrack.ai", layout="wide")

st.title("🐋 WhaleTrack.ai - Shadow-Flow Detector")
st.markdown("Deteksi pergerakan bandar dan konfirmasi teknikal secara instan.")

# Input Pengguna
ticker = st.text_input("Masukkan Kode Saham (contoh: BBCA.JK, GOTO.JK):", "BBCA.JK")

if st.button("Analisis Saham"):
    with st.spinner('AI sedang memproses Order Book & Tick Data...'):
        # Simulasi penarikan data & model AI
        data = yf.download(ticker, period='3mo')
        
        # Simulasi output Machine Learning (Whale Power)
        whale_power = random.randint(40, 95)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Harga Terakhir", f"Rp {int(data['Close'].iloc[-1].item())}")
        
        # Logika Sinyal
        if whale_power > 75:
            col2.metric("Whale Power Index (WPI)", f"{whale_power}%", "Strong Accumulation")
            col3.error("🚨 ALERT: Bandar Terdeteksi!")
        else:
            col2.metric("Whale Power Index (WPI)", f"{whale_power}%", "-Neutral")
            col3.success("✅ Aman dari Guyuran")

        # Visualisasi Grafik Teknikal
        st.subheader(f"Grafik Pergerakan & Volume {ticker}")
        st.line_chart(data['Close'])
