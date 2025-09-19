# tools/client.py
from __future__ import annotations
import requests
from typing import Any, Dict, List, Optional

class AnkiConnectError(RuntimeError):
    pass

class AnkiConnectClient:
    """AnkiConnect 最小クライアント: addNotes(Basic) のみ"""
    def __init__(self, host: str = "http://localhost", port: int = 8765, timeout: float = 5.0) -> None:
        self.endpoint = f"{host}:{port}"
        self.timeout = timeout

    def _post(self, action: str, params: Optional[Dict[str, Any]] = None) -> Any:
        payload = {"action": action, "version": 6, "params": params or {}}
        try:
            resp = requests.post(self.endpoint, json=payload, timeout=self.timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise AnkiConnectError(f"Connect/post failed to {self.endpoint}: {e}") from e

        data = resp.json()
        if data.get("error") is not None:
            raise AnkiConnectError(f"AnkiConnect error: {data['error']}")
        return data.get("result")

    def add_notes_basic(
        self,
        deck_name: str,
        pairs: List[Dict[str, Any]],
        model_name: str = "Basic",
        allow_duplicate: bool = False,
        default_tags: Optional[List[str]] = None,
    ) -> List[Optional[int]]:
        """pairs: [{'front': str, 'back': str, 'tags': [..] (optional)}, ...]"""
        default_tags = default_tags or []
        notes = []
        for p in pairs:
            front = str(p.get("front", ""))
            back = str(p.get("back", ""))
            tags = list(p.get("tags", []))
            notes.append({
                "deckName": deck_name,
                "modelName": model_name,
                "fields": {"Front": front, "Back": back},
                "options": {"allowDuplicate": bool(allow_duplicate)},
                "tags": [*default_tags, *tags],
            })
        return self._post("addNotes", {"notes": notes})
