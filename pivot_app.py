import streamlit as st
import yfinance as yf
from datetime import datetime
import time

# Page config
st.set_page_config(page_title="Pivot Point Action Plan", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS Styling
st.markdown("""
    <style>
    .big-font {
        font-size:36px !important;
        color: white;
        text-align: center;
        font-weight: 700;
    }
    .author {
        text-align: center;
        font-size: 25px !important;
        color: white;
        font-weight: bold;
    }
    .metric-label {
        font-weight: bold;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


# Title & Author
st.markdown('<div class="big-font">📊💰💸💵 Pivot Point Action Plan 📊💰💸💵</div>', unsafe_allow_html=True)
st.markdown('<div class="author">😎 Bhupendra Meghwal 😎</div>', unsafe_allow_html=True)
st.markdown("---")

# --- Pivot Point Calculation ---
def calc_levels(h, l, c):
    pp = (h + l + c) / 3
    lb = (h + l) / 2
    ub = 2 * pp - lb
    hl = h - l
    return {
        "Resistance (R3)": ("R1 + (H - L)", 2 * pp - l + hl),
        "Resistance (R2)": ("CP + (H - L)", pp + hl),
        "Resistance (R1)": ("(2 x CP) - L", 2 * pp - l),
        "Upper Boundary": ("(CP - LB) + CP", ub),
        "Central Pivot (CP)": ("(H + L + C) / 3", pp),
        "Lower Boundary": ("(H + L)/2", lb),
        "Support (S1)": ("(2 x CP) - H", 2 * pp - h),
        "Support (S2)": ("CP - (H - L)", pp - hl),
        "Support (S3)": ("S1 - (H - L)", 2 * pp - h - hl)
    }

def calc_cpr_range(pp, lb, ub):
    return (ub - pp) / pp * 100, (pp - lb) / pp * 100


# --- Input Mode ---
mode = st.radio("## 🛠️ Select Input Mode:" , ["Manual" , "Auto Fetch NIFTY 50"], horizontal=True)

h = l = c = None

if mode == "Manual":
    with st.expander("🔧 Enter High, Low, Close manually"):
        h = st.number_input("Enter High", min_value=0.0, format="%.2f")
        l = st.number_input("Enter Low", min_value=0.0, format="%.2f")
        c = st.number_input("Enter Close", min_value=0.0, format="%.2f")    

else:
    with st.spinner("🔄 Fetching latest NIFTY 50 data..."):
        time.sleep(2)  # Animation delay
        try:
            nifty = yf.Ticker("^NSEI")
            hist = nifty.history(period="1d")
            h = hist['High'].iloc[0]
            l = hist['Low'].iloc[0]
            c = hist['Close'].iloc[0]

            st.success("✅✅ Latest NIFTY 50 data fetched successfully!")

            # --- Metrics display ---
            col1, col2, col3 = st.columns(3)
            col1.metric("📈 High", f"{h:.2f}")
            col2.metric("📉 Low", f"{l:.2f}")
            col3.metric("⏳ Close", f"{c:.2f}")

            # Timestamp
            timestamp = datetime.now().strftime("%d-%b-%Y %I:%M %p")
            st.caption(f"⏱️ Last update on: {timestamp}")

        except:
            st.error("⚠⚠️️ Failed to fetch data. Please try again later.")
            st.stop()

# --- Display Pivot Table ---
if h and l and c:
    levels = calc_levels(h, l, c)
    
    with st.expander("📮🪄✨ View Pivot Point Levels", expanded=True):
        st.markdown("#### 📌 Calculated Pivot Levels:")
        styled_table = {k: {"Formula": v[0], "Value": f"{v[1]:.2f}"} for k, v in levels.items()}
        st.table(styled_table)

    # --- CPR Range ---
    pp = levels["Central Pivot (CP)"][1]
    lb = levels["Lower Boundary"][1]
    ub = levels["Upper Boundary"][1]
    p_ub, p_lb = calc_cpr_range(pp, lb, ub)

    with st.expander("📐📏 Central Pivot Range Width"):
        col1, col2 = st.columns(2)
        col1.metric("📊 CP → UB", f"{p_ub:.2f}%", delta=None)
        col2.metric("📊 CP → LB", f"{p_lb:.2f}%", delta=None)
else:
    st.info("ℹ️ Please enter valid values to see Pivot Point analysis.")

