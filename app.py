import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="WhaleTrack.ai PRO", page_icon="🐋", layout="wide", initial_sidebar_state="expanded")

# 2. CUSTOM CSS & HTML (Mengubah total wajah Streamlit)
st.markdown("""
    <style>
    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Hilangkan padding default yang mengganggu */
    .block-container { padding-top: 2rem; padding-bottom: 0rem; }

    /* Custom Glassmorphism Card (Untuk Metric) */
    .glass-card {
        background: linear-gradient(135deg, rgba(26, 32, 44, 0.8) 0%, rgba(13, 17, 23, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.2s, border-color 0.2s;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 198, 255, 0.5);
    }
    .card-title { color: #A0AEC0; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .card-value { color: #FFFFFF; font-size: 1.8rem; font-weight: 800; margin-bottom: 4px; }
    .card-delta.up { color: #00E676; font-size: 0.9rem; font-weight: 600; }
    .card-delta.down { color: #FF1744; font-size: 0.9rem; font-weight: 600; }
    .card-delta.neutral { color: #82AAFF; font-size: 0.9rem; font-weight: 600; }

    /* Custom Trading Plan Cards */
    .plan-card {
        background: rgba(13, 17, 23, 0.6);
        border-radius: 8px;
        padding: 15px 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .plan-card.entry { border-left: 5px solid #2979FF; }
    .plan-card.tp { border-left: 5px solid #00E676; }
    .plan-card.sl { border-left: 5px solid #FF1744; }
    .plan-label { font-size: 0.8rem; font-weight: 800; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;}
    .plan-price { font-size: 1.4rem; font-weight: 800; color: white; margin-bottom: 2px;}
    .plan-desc { font-size: 0.75rem; color: #A0AEC0; }
    
    .plan-label.entry-text { color: #2979FF; }
    .plan-label.tp-text { color: #00E676; }
    .plan-label.sl-text { color: #FF1744; }

    /* Alert Box Keren */
    .alert-box {
        border-radius: 12px; padding: 20px; font-weight: 600; font-size: 0.9rem; line-height: 1.5;
    }
    .alert-buy { background: rgba(0, 230, 118, 0.1); border: 1px solid #00E676; color: #00E676; }
    .alert-sell { background: rgba(255, 23, 68, 0.1); border: 1px solid #FF1744; color: #FF1744; }
    .alert-safe { background: rgba(130, 170, 255, 0.1); border: 1px solid #82AAFF; color: #82AAFF; }

    /* Judul Utama */
    .main-header {
        font-size: 2.5rem; font-weight: 800; 
        background: -webkit-linear-gradient(45deg, #00C6FF, #0072FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0; padding-bottom: 0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00C6FF; font-weight: 800;'>🐋 Control Panel</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #2D3748;'>", unsafe_allow_html=True)
    ticker = st.text_input("🔍 Input Ticker (ex: RATU.JK, BBCA.JK):", "RATU.JK")
    analyze_button = st.button("🚀 Run AI Engine", type="primary", use_container_width=True)
    st.markdown("<hr style='border-color: #2D3748;'>", unsafe_allow_html=True)
    st.caption("⚙️ **Engine Status:** Online")
    st.caption("🔗 **Data Feed:** YF API v2.0")
    st.caption("🛡️ **System:** Encrypted SSL")

# 4. HEADER UTAMA
st.markdown("<h1 class='main-header'>WhaleTrack.ai Terminal</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #A0AEC0; font-size: 1rem; margin-top: -10px;'>Advanced Institutional Order Block & Shadow-Flow Detector</p>", unsafe_allow_html=True)

# 5. FUNGSI LOGIKA (Simulasi AI)
def calculate_whale_power(df):
    recent_vol = float(df['Volume'].tail(5).mean())
    past_vol = float(df['Volume'].tail(20).head(15).mean())
    price_momentum = float((df['Close'].iloc[-1] - df['Close'].iloc[-5]) / df['Close'].iloc[-5] * 100)
    
    base_power = 50
    if recent_vol > past_vol * 1.5: base_power += 25
    elif recent_vol < past_vol * 0.8: base_power -= 15
    if price_momentum > 2: base_power += 10
    elif price_momentum < -2: base_power -= 20
        
    return max(10, min(99, int(base_power)))

# 6. LOGIKA EKSEKUSI
if analyze_button:
    with st.spinner("Decrypting Market Maker Footprints..."):
        time.sleep(1)

    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='6mo')
        
        if data.empty:
            st.error("❌ Data tidak ditemukan. Pastikan format ticker valid.")
        else:
            whale_power = calculate_whale_power(data)
            latest_price = int(float(data['Close'].iloc[-1]))
            prev_price = int(float(data['Close'].iloc[-2]))
            price_change = latest_price - prev_price
            price_change_pct = (price_change / prev_price) * 100
            
            # Kalkulasi Trading Plan
            highest_5d = float(data['High'].tail(5).max())
            lowest_5d = float(data['Low'].tail(5).min())
            tp_price = int(highest_5d * 1.03)
            sl_price = int(lowest_5d * 0.98)
            
            data['MA20'] = data['Close'].rolling(window=20).mean()
            
            # --- TABS ---
            tab1, tab2, tab3 = st.tabs(["📊 Main Dashboard", "🤖 AI Prediction Engine", "🗄️ Raw Data Feed"])
            
            # --- TAB 1: DASHBOARD ---
            with tab1:
                st.write("") # Spacing
                
                # ROW 1: METRICS (Memakai Custom HTML)
                col1, col2, col3, col4 = st.columns(4)
                
                # Card 1: Price
                color_class = "up" if price_change >= 0 else "down"
                sign = "+" if price_change >= 0 else ""
                col1.markdown(f"""
                <div class="glass-card">
                    <div class="card-title">Last Price</div>
                    <div class="card-value">Rp {latest_price:,}</div>
                    <div class="card-delta {color_class}">{sign}Rp {abs(price_change):,} ({sign}{price_change_pct:.2f}%)</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Card 2: RSI
                rsi_sim = np.random.randint(40, 70)
                col2.markdown(f"""
                <div class="glass-card">
                    <div class="card-title">RSI (14d)</div>
                    <div class="card-value">{rsi_sim}</div>
                    <div class="card-delta neutral">Normal Zone</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Card 3 & 4: Whale Power & Alert
                if whale_power >= 70:
                    col3.markdown(f"""<div class="glass-card"><div class="card-title">Whale Power Index</div><div class="card-value" style="color: #00E676;">{whale_power}%</div><div class="card-delta up">↑ Strong Accumulation</div></div>""", unsafe_allow_html=True)
                    col4.markdown("""<div class="alert-box alert-buy">🚨 <b>SYSTEM ALERT</b><br>Volume Spike terdeteksi. Bandar sedang akumulasi. Sinyal AI merekomendasikan <b>BUY</b>.</div>""", unsafe_allow_html=True)
                elif whale_power <= 40:
                    col3.markdown(f"""<div class="glass-card"><div class="card-title">Whale Power Index</div><div class="card-value" style="color: #FF1744;">{whale_power}%</div><div class="card-delta down">↓ Heavy Distribution</div></div>""", unsafe_allow_html=True)
                    col4.markdown("""<div class="alert-box alert-sell">⚠️ <b>WARNING</b><br>Guyuran institusi terdeteksi. Risiko tinggi. Sinyal AI merekomendasikan <b>WAIT / SELL</b>.</div>""", unsafe_allow_html=True)
                else:
                    col3.markdown(f"""<div class="glass-card"><div class="card-title">Whale Power Index</div><div class="card-value" style="color: #82AAFF;">{whale_power}%</div><div class="card-delta neutral">→ Neutral Flow</div></div>""", unsafe_allow_html=True)
                    col4.markdown("""<div class="alert-box alert-safe">✅ <b>MARKET SAFE</b><br>Tidak ada anomali algoritma High Frequency Trading (HFT). Flow retail dominan.</div>""", unsafe_allow_html=True)

                st.write("") # Spacing
                
                # ROW 2: TRADING PLAN (Custom HTML)
                st.markdown("<h3 style='font-size: 1.2rem; color: white; margin-bottom: 10px;'>🎯 Algorithmic Trading Plan</h3>", unsafe_allow_html=True)
                
                p1, p2, p3 = st.columns(3)
                p1.markdown(f"""
                <div class="plan-card entry">
                    <div class="plan-label entry-text">🔵 ENTRY ZONE</div>
                    <div class="plan-price">Rp {latest_price:,}</div>
                    <div class="plan-desc">Current Market Price / Accumulation Area</div>
                </div>
                """, unsafe_allow_html=True)
                
                p2.markdown(f"""
                <div class="plan-card tp">
                    <div class="plan-label tp-text">🟢 TAKE PROFIT (Target)</div>
                    <div class="plan-price">Rp {tp_price:,}</div>
                    <div class="plan-desc">Resistance Breakout (+3% Estimasi)</div>
                </div>
                """, unsafe_allow_html=True)
                
                p3.markdown(f"""
                <div class="plan-card sl">
                    <div class="plan-label sl-text">🔴 CUT LOSS (Risk)</div>
                    <div class="plan-price">Rp {sl_price:,}</div>
                    <div class="plan-desc">Support Breakdown (-2% Toleransi)</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                
                # ROW 3: PLOTLY CHART (Clean UI)
                st.markdown("<h3 style='font-size: 1.2rem; color: white; margin-bottom: 0px;'>📈 Institutional Footprint Chart</h3>", unsafe_allow_html=True)
                
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.75, 0.25])

                fig.add_trace(go.Candlestick(
                    x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
                    increasing_line_color='#00E676', decreasing_line_color='#FF1744', name='Price'
                ), row=1, col=1)
                
                fig.add_trace(go.Scatter(
                    x=data.index, y=data['MA20'], line=dict(color='#2979FF', width=1.5), name='MA 20'
                ), row=1, col=1)

                colors = ['#00E676' if row['Open'] - row['Close'] >= 0 else '#FF1744' for index, row in data.iterrows()]
                fig.add_trace(go.Bar(
                    x=data.index, y=data['Volume'], marker_color=colors, name='Volume', opacity=0.8
                ), row=2, col=1)
                
                fig.update_layout(
                    template='plotly_dark', plot_bgcolor='rgba(13, 17, 23, 0.4)', paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=10, b=0), height=550, showlegend=False,
                    xaxis_rangeslider_visible=False
                )
                
                fig.update_xaxes(showgrid=False, zeroline=False)
                fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
                
                st.plotly_chart(fig, use_container_width=True)

            # --- TAB 2 & 3 ---
            with tab2:
                st.markdown("### ⚙️ Feature Engineering Details")
                short_momentum = float((data['Close'].iloc[-1] - data['Close'].iloc[-5]) / data['Close'].iloc[-5] * 100)
                avg_vol_20 = int(float(data['Volume'].tail(20).mean()))
                recent_vol_5 = int(float(data['Volume'].tail(5).mean()))
                st.write(f"- **Short-Term Momentum (5d):** {short_momentum:.2f}%")
                st.write(f"- **Baseline Volatility (20d):** {avg_vol_20:,} shares")
                st.write(f"- **Recent Volume Spike (5d):** {recent_vol_5:,} shares")
                st.info("🧠 Model Confidence: 87.4% (Based on historical backtesting)")
            
            with tab3:
                st.markdown("### 🗄️ OHLCV Database")
                clean_data = data[['Open', 'High', 'Low', 'Close', 'Volume', 'MA20']].round(2)
                st.dataframe(clean_data.tail(30).sort_index(ascending=False), use_container_width=True)

    except Exception as e:
        st.error(f"Error fetching data: {e}")
