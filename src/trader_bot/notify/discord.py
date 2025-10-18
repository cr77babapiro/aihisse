from __future__ import annotations

import os
from typing import Optional

import requests


def send_webhook(content: str, webhook_url: Optional[str] = None) -> None:
    url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")
    if not url:
        raise RuntimeError("Set DISCORD_WEBHOOK_URL or pass webhook_url")
    resp = requests.post(url, json={"content": content})
    resp.raise_for_status()
