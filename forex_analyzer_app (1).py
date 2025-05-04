
import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt

# --- Streamlit UI ---
st.set_page_config(page_title="Forex Analyzer", layout="wide")
st.title("📊 Dorgam9675.Smart.Sniper.FX")

symbol = st.selectbox("اختر زوج العملات أو الذهب:", ["EURUSD=X", "GBPUSD=X", "JPY=X", "XAUUSD=X"])
period = st.selectbox("الفترة الزمنية:", ["1mo", "3mo", "6mo", "1y"])
interval = st.selectbox("الفاصل الزمني:", ["1h", "4h", "1d"])

# --- Load Data ---
@st.cache_data
def load_data(symbol, period, interval):
    df = yf.download(symbol, period=period, interval=interval)
    df.dropna(inplace=True)
    return df

data = load_data(symbol, period, interval)

# --- Technical Indicators ---
data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
data['MACD'] = ta.trend.MACD(data['Close']).macd()
bb = ta.volatility.BollingerBands(data['Close'])
data['Upper_BB'] = bb.bollinger_hband()
data['Lower_BB'] = bb.bollinger_lband()

ema = ta.trend.EMAIndicator(data['Close'], window=200)
data['EMA200'] = ema.ema_indicator()

# --- Charts ---
st.subheader("الرسم البياني للسعر + EMA200")
st.line_chart(data[['Close', 'EMA200']])

# --- Indicators Visualization ---
with st.expander("📈 المؤشرات الفنية"):
    fig, ax = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
    ax[0].plot(data['Close'], label='السعر')
    ax[0].plot(data['Upper_BB'], label='BB Upper', linestyle='--')
    ax[0].plot(data['Lower_BB'], label='BB Lower', linestyle='--')
    ax[0].legend()
    ax[0].set_title("Bollinger Bands")

    ax[1].plot(data['RSI'], color='orange')
    ax[1].axhline(70, color='red', linestyle='--')
    ax[1].axhline(30, color='green', linestyle='--')
    ax[1].set_title("RSI")

    ax[2].plot(data['MACD'], color='blue')
    ax[2].set_title("MACD")
    st.pyplot(fig)

# --- Signal Logic ---
st.subheader("📌 التوصية الآلية:")
rsi = data['RSI'].iloc[-1]
macd = data['MACD'].iloc[-1]
ema_cond = data['Close'].iloc[-1] > data['EMA200'].iloc[-1]

if rsi < 30 and macd > 0 and ema_cond:
    st.success("🟢 إشارة شراء قوية متاحة")
elif rsi > 70 and macd < 0 and not ema_cond:
    st.error("🔴 إشارة بيع قوية متاحة")
else:
    st.info("⚪ لا توجد فرصة واضحة حالياً")
