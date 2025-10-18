from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class IbOrder:
    symbol: str
    qty: float
    side: str  # "buy" or "sell"


class IbBroker:
    """Placeholder for Interactive Brokers execution. Requires IB API/IB-insync in real use."""

    def __init__(self, host: str = "127.0.0.1", port: int = 7497, client_id: int = 1) -> None:
        self.host = host
        self.port = port
        self.client_id = client_id

    def place_order(self, order: IbOrder) -> Dict[str, Any]:
        # Placeholder implementation
        return {"status": "submitted", "symbol": order.symbol, "qty": order.qty, "side": order.side}
