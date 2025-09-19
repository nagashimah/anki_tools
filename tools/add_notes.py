# tools/add_notes.py
from __future__ import annotations
import os, csv, json, yaml
from pathlib import Path
from typing import List, Dict, Any
from .client import AnkiConnectClient, AnkiConnectError

def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def _load_pairs(path: Path) -> List[Dict[str, Any]]:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            rows.append({
                "front": (row.get("front") or "").strip(),
                "back":  (row.get("back") or "").strip(),
                "tags":  [t for t in (row.get("tags") or "").split(";") if t]
            })
    return rows

def main() -> int:
    # 1) CONFIG_PATH > config.yaml > config.sample.yaml の順に探す
    candidates = []
    if os.getenv("CONFIG_PATH"):
        candidates.append(Path(os.getenv("CONFIG_PATH")))
    candidates += [Path("config.yaml"), Path("config.sample.yaml")]

    cfg_path = next((p for p in candidates if p.exists()), None)
    if not cfg_path:
        print("ERROR: config.yaml / config.sample.yaml が見つかりません。")
        return 2

    cfg = _load_yaml(cfg_path)
    input_path = Path(cfg.get("input", "data/notes_sample.json"))
    if not input_path.exists():
        print(f"ERROR: 入力がありません: {input_path}")
        return 2

    try:
        pairs = _load_pairs(input_path)
        client = AnkiConnectClient(
            host=cfg.get("host", "http://localhost"),
            port=int(cfg.get("port", 8765)),
        )
        result = client.add_notes_basic(
            deck_name=cfg.get("deck", "Default"),
            pairs=pairs,
            model_name=cfg.get("model", "Basic"),
            allow_duplicate=bool(cfg.get("allow_duplicate", False)),
            default_tags=list(cfg.get("tags", [])),
        )
        added = sum(1 for x in result if isinstance(x, int))
        failed = sum(1 for x in result if x is None)
        print(f"Added: {added}, Failed: {failed}")
        return 0 if failed == 0 else 3
    except (ValueError, AnkiConnectError) as e:
        print(f"ERROR: {e}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
