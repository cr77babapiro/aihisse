from __future__ import annotations

from typing import Dict

import pandas as pd
import yfinance as yf


_SYMBOLS = {
    "DXY": "DX-Y.NYB",  # Dollar Index proxy
    "GOLD": "GC=F",
    "OIL": "CL=F",
    "EURUSD": "EURUSD=X",
}


def fetch_macro_proxies(period: str = "1y", interval: str = "1d") -> Dict[str, pd.DataFrame]:
    out: Dict[str, pd.DataFrame] = {}
    for name, symbol in _SYMBOLS.items():
        df = yf.download(symbol, period=period, interval=interval, progress=False)
        if not df.empty:
            df = df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"})
            df = df[[c for c in ["open", "high", "low", "close", "volume"] if c in df.columns]].copy()
            df.reset_index(inplace=True)
            df.rename(columns={df.columns[0]: "timestamp"}, inplace=True)
            out[name] = df
    return out
