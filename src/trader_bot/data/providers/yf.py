from __future__ import annotations

from datetime import datetime
from typing import Optional

import pandas as pd
import yfinance as yf

from ...logging_config import get_logger


LOGGER = get_logger(__name__)


_SUPPORTED_INTERVALS = {
    # intraday
    "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h",
    # daily and above
    "1d", "5d", "1wk", "1mo", "3mo",
}


def _validate_interval(interval: str) -> str:
    normalized = interval.strip()
    if normalized not in _SUPPORTED_INTERVALS:
        raise ValueError(f"Unsupported interval '{interval}'. Supported: {_SUPPORTED_INTERVALS}")
    return normalized


def fetch_ohlcv(
    ticker: str,
    interval: str = "1m",
    period: Optional[str] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    auto_adjust: bool = False,
) -> pd.DataFrame:
    """Fetch OHLCV data from yfinance and return a standardized DataFrame.

    Columns: timestamp, open, high, low, close, volume
    """
    interval = _validate_interval(interval)

    # sensible default periods if not provided
    if period is None and start is None:
        if interval.endswith("m") or interval.endswith("h"):
            period = "7d"  # yfinance limitation for 1m data
        else:
            period = "1y"

    LOGGER.info(
        "Fetching data",
    )

    df = yf.download(
        tickers=ticker,
        interval=interval,
        period=period,
        start=start,
        end=end,
        auto_adjust=auto_adjust,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"No data returned for {ticker} interval={interval} period={period} start={start} end={end}")

    # Single ticker -> flat columns
    # Ensure expected columns exist
    expected_cols = {"Open", "High", "Low", "Close", "Volume"}
    missing = expected_cols.difference(set(df.columns))
    if missing:
        # sometimes Adj Close appears; ignore
        pass

    # drop Adj Close if present
    cols = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
    df = df[cols].copy()

    # drop timezone to make it consistent
    idx = df.index
    try:
        if getattr(idx, "tz", None) is not None:
            df.index = idx.tz_convert("UTC").tz_localize(None)
    except Exception:
        # if tz_convert fails because naive, ignore
        try:
            df.index = idx.tz_localize(None)
        except Exception:
            pass

    df.reset_index(inplace=True)
    df.rename(
        columns={
            df.columns[0]: "timestamp",  # Date / Datetime
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        },
        inplace=True,
    )

    # enforce dtypes
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=False)
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df.dropna(inplace=True)
    df.sort_values("timestamp", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
