from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
import pandas as pd


@dataclass
class BacktestResult:
    summary: Dict[str, float]
    equity_curve: pd.DataFrame
    trades: Optional[pd.DataFrame]


def _compute_drawdown(equity: pd.Series) -> pd.Series:
    rolling_max = equity.cummax()
    drawdown = equity / rolling_max - 1.0
    return drawdown


def run_backtest(
    data_with_signals: pd.DataFrame,
    price_col: str = "close",
    position_col: str = "position",
    periods_per_year: float = 252.0,
) -> BacktestResult:
    if position_col not in data_with_signals.columns:
        raise ValueError(f"'{position_col}' column required for backtest")
    if price_col not in data_with_signals.columns:
        raise ValueError(f"'{price_col}' column required for backtest")

    df = data_with_signals.copy()

    df["returns"] = df[price_col].pct_change().fillna(0.0)
    df["strategy_returns"] = df[position_col].shift(1).fillna(0.0) * df["returns"]
    df["equity"] = (1.0 + df["strategy_returns"]).cumprod()

    drawdown = _compute_drawdown(df["equity"]).fillna(0.0)
    max_drawdown = float(drawdown.min())

    mean_ret = float(df["strategy_returns"].mean())
    std_ret = float(df["strategy_returns"].std(ddof=0))
    sharpe = float((mean_ret / std_ret) * np.sqrt(periods_per_year)) if std_ret > 0 else 0.0

    total_return = float(df["equity"].iloc[-1] - 1.0)

    # trades dataframe
    if "signal" in df.columns:
        trade_events = df[df["signal"] != 0][["timestamp", "signal", price_col]].copy() if "timestamp" in df.columns else df[df["signal"] != 0][["signal", price_col]].copy()
    else:
        delta = df[position_col].diff().fillna(0)
        trade_events = df[delta != 0][["timestamp", position_col, price_col]].copy() if "timestamp" in df.columns else df[delta != 0][[position_col, price_col]].copy()

    summary = {
        "total_return": total_return,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "num_periods": float(len(df)),
        "num_trades": float(len(trade_events)),
    }

    return BacktestResult(summary=summary, equity_curve=df[["timestamp", "equity"]] if "timestamp" in df.columns else df[["equity"]], trades=trade_events.reset_index(drop=True))
