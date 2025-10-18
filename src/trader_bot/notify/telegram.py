from __future__ import annotations

import os
from typing import Optional

import requests

from ..config import settings


def send_message(text: str, token: Optional[str] = None, chat_id: Optional[str] = None) -> None:
    token = token or settings.telegram_bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = chat_id or settings.telegram_chat_id or os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise RuntimeError("Telegram token/chat_id missing. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resp = requests.post(url, json={"chat_id": chat_id, "text": text})
    resp.raise_for_status()
