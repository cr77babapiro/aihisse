from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..config import settings


@dataclass
class Order:
    symbol: str
    qty: float
    side: str  # "buy" or "sell"
    type: str = "market"
    time_in_force: str = "day"


class AlpacaBroker:
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, base_url: Optional[str] = None) -> None:
        self.api_key = api_key or settings.alpaca_api_key
        self.api_secret = api_secret or settings.alpaca_api_secret
        self.base_url = base_url or settings.alpaca_paper_base_url
        self._client = None

    def _ensure_client(self) -> None:
        if self._client is None:
            try:
                from alpaca_trade_api.rest import REST
            except Exception as exc:
                raise RuntimeError("alpaca-trade-api not installed") from exc
            if not self.api_key or not self.api_secret:
                raise RuntimeError("Alpaca API credentials missing")
            self._client = REST(key_id=self.api_key, secret_key=self.api_secret, base_url=self.base_url)

    def get_account(self) -> Dict[str, Any]:
        self._ensure_client()
        acc = self._client.get_account()
        return acc._raw

    def place_order(self, order: Order) -> Dict[str, Any]:
        self._ensure_client()
        resp = self._client.submit_order(
            symbol=order.symbol,
            qty=order.qty,
            side=order.side,
            type=order.type,
            time_in_force=order.time_in_force,
        )
        return resp._raw

    def list_positions(self) -> List[Dict[str, Any]]:
        self._ensure_client()
        return [p._raw for p in self._client.list_positions()]
