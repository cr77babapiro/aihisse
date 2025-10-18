from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ..features.indicators import add_sma_signals


@dataclass
class SmaStrategyParams:
    fast_window: int = 10
    slow_window: int = 30


def generate_signals(price_data: pd.DataFrame, params: SmaStrategyParams) -> pd.DataFrame:
    if params.fast_window >= params.slow_window:
        raise ValueError("fast_window must be less than slow_window for SMA strategy")
    return add_sma_signals(price_data, fast_window=params.fast_window, slow_window=params.slow_window)
