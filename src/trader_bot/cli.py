from __future__ import annotations

from typing import Optional

import pandas as pd
import typer

from .config import settings
from .logging_config import configure_logging, get_logger
from .data.providers.yf import fetch_ohlcv
from .strategy.sma import SmaStrategyParams, generate_signals
from .backtest.core import run_backtest
from .gui import app as gui_app


app = typer.Typer(add_completion=False, no_args_is_help=True)
LOGGER = get_logger(__name__)


def main() -> None:  # entry point
    app()


@app.callback()
def _init(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
    json_logs: bool = typer.Option(False, "--json-logs", help="Output logs as JSON"),
) -> None:
    configure_logging(level="DEBUG" if verbose else "INFO", json_logs=json_logs)
    LOGGER.info("Environment: %s", settings.environment)


@app.command()
def fetch(
    ticker: str = typer.Argument(settings.default_ticker, help="Ticker symbol"),
    interval: str = typer.Option(settings.default_interval, "--interval", "-i", help="Data interval (e.g., 1m, 5m, 1d)"),
    period: Optional[str] = typer.Option(None, help="Period (e.g., 7d, 1y). Mutually exclusive with start/end."),
    start: Optional[str] = typer.Option(None, help="Start datetime (YYYY-MM-DD or ISO)"),
    end: Optional[str] = typer.Option(None, help="End datetime (YYYY-MM-DD or ISO)"),
    csv: Optional[str] = typer.Option(None, help="Optional path to save CSV"),
) -> None:
    """Fetch OHLCV via yfinance and optionally save to CSV."""
    start_dt = pd.to_datetime(start) if start else None
    end_dt = pd.to_datetime(end) if end else None
    df = fetch_ohlcv(ticker=ticker, interval=interval, period=period, start=start_dt, end=end_dt)
    typer.echo(df.head().to_string())
    if csv:
        df.to_csv(csv, index=False)
        LOGGER.info("Saved CSV: %s", csv)


@app.command()
def backtest(
    ticker: str = typer.Argument(settings.default_ticker, help="Ticker symbol"),
    interval: str = typer.Option(settings.default_interval, "--interval", "-i", help="Data interval"),
    fast: int = typer.Option(10, help="Fast SMA window"),
    slow: int = typer.Option(30, help="Slow SMA window"),
    period: Optional[str] = typer.Option(None, help="Period (e.g., 1y)"),
) -> None:
    """Run SMA crossover backtest on yfinance data."""
    data = fetch_ohlcv(ticker=ticker, interval=interval, period=period)
    params = SmaStrategyParams(fast_window=fast, slow_window=slow)
    signals = generate_signals(data, params)
    result = run_backtest(signals)
    typer.echo("Summary:")
    for k, v in result.summary.items():
        typer.echo(f"- {k}: {v:.4f}" if isinstance(v, float) else f"- {k}: {v}")


@app.command()
def gui() -> None:
    """Launch Streamlit dashboard."""
    # Allow running inside Cursor without shelling out; if that fails, print hint.
    try:
        gui_app.main()
    except SystemExit:
        # Streamlit may call sys.exit in some contexts; ignore for in-process run
        pass
    except Exception as exc:
        typer.echo("Could not start embedded GUI. Try: streamlit run -m trader_bot.gui.app")
        raise exc


if __name__ == "__main__":
    main()
