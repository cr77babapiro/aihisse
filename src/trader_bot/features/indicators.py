from __future__ import annotations

import pandas as pd


def add_sma(data: pd.DataFrame, fast_window: int = 10, slow_window: int = 30) -> pd.DataFrame:
    if "close" not in data.columns:
        raise ValueError("Data must include a 'close' column")
    result = data.copy()
    result["sma_fast"] = result["close"].rolling(window=fast_window, min_periods=fast_window).mean()
    result["sma_slow"] = result["close"].rolling(window=slow_window, min_periods=slow_window).mean()
    return result


def add_sma_signals(data: pd.DataFrame, fast_window: int = 10, slow_window: int = 30) -> pd.DataFrame:
    result = add_sma(data, fast_window=fast_window, slow_window=slow_window)
    result["position"] = (result["sma_fast"] > result["sma_slow"]).astype(int)
    # trade signal is change in position: +1 -> buy, -1 -> sell
    result["signal"] = result["position"].diff().fillna(0).astype(int)
    return result
