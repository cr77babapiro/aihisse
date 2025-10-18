from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from ..config import settings
from ..data.providers.yf import fetch_ohlcv
from ..strategy.sma import SmaStrategyParams, generate_signals
from ..backtest.core import run_backtest


st.set_page_config(page_title="Trader Bot Dashboard", layout="wide")


@st.cache_data(show_spinner=False)
def load_data(ticker: str, interval: str, period: str):
    return fetch_ohlcv(ticker=ticker, interval=interval, period=period)


def price_chart(df):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["timestamp"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="Price",
            )
        ]
    )
    if "sma_fast" in df and "sma_slow" in df:
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["sma_fast"], name="SMA Fast"))
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["sma_slow"], name="SMA Slow"))

    # Buy/Sell markers
    if "signal" in df:
        buys = df[df["signal"] > 0]
        sells = df[df["signal"] < 0]
        fig.add_trace(
            go.Scatter(
                x=buys["timestamp"],
                y=buys["close"],
                mode="markers",
                name="Buy",
                marker=dict(color="green", size=8, symbol="triangle-up"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=sells["timestamp"],
                y=sells["close"],
                mode="markers",
                name="Sell",
                marker=dict(color="red", size=8, symbol="triangle-down"),
            )
        )

    fig.update_layout(height=600, xaxis_rangeslider_visible=False)
    return fig


def main():
    st.title("Akıllı Hisse Senedi Alım-Satım Botu")

    with st.sidebar:
        st.header("Ayarlar")
        ticker = st.text_input("Ticker", value=settings.default_ticker)
        interval = st.selectbox(
            "Interval",
            options=["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"],
            index=0,
        )
        period = st.selectbox("Period", options=["7d", "1mo", "3mo", "6mo", "1y", "2y"], index=5)
        fast = st.number_input("SMA Fast", min_value=2, max_value=200, value=10)
        slow = st.number_input("SMA Slow", min_value=5, max_value=400, value=30)
        run_btn = st.button("Veriyi Yükle ve Çalıştır")

    if run_btn:
        with st.spinner("Veri yükleniyor..."):
            data = load_data(ticker, interval, period)
        params = SmaStrategyParams(fast_window=int(fast), slow_window=int(slow))
        signals = generate_signals(data, params)
        result = run_backtest(signals)

        # Layout
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Fiyat ve Sinyaller")
            st.plotly_chart(price_chart(signals), use_container_width=True)
        with col2:
            st.subheader("Özet")
            st.metric("Toplam Getiri", f"{result.summary['total_return']*100:.2f}%")
            st.metric("Sharpe", f"{result.summary['sharpe']:.2f}")
            st.metric("Max Drawdown", f"{result.summary['max_drawdown']*100:.2f}%")
            st.metric("İşlem Sayısı", int(result.summary['num_trades']))

        st.subheader("Sermaye Eğrisi")
        st.line_chart(result.equity_curve.set_index("timestamp") if "timestamp" in result.equity_curve.columns else result.equity_curve)


if __name__ == "__main__":
    main()
