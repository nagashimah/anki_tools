import csv
import json
import requests

with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

ANKI_URL = config["anki_url"]
DECK_NAME = config["deck_name"]
MODEL_NAME = config["model_name"]

def add_note(front, back, tags=None):
    if tags is None:
        tags = ["None"]

    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": DECK_NAME,
                "modelName": MODEL_NAME,
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "options": {
                    "allowDuplicate": False
                },
                "tags": tags
            }
        }
    }

    try:
        res = requests.post(ANKI_URL, json=payload)
        res.raise_for_status()
        result = res.json()
        if result.get("error"):
            print(f"❌ {front} → {result['error']}")
        else:
            print(f"✅ {front} を追加")
    except Exception as e:
        print(f"接続エラー: {e}")

with open("notes.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    for row in reader:
        if len(row) >= 2:
            front = row[0].strip()
            back = row[1].strip()
            if not front or not back:
                print(f"⚠️ スキップ（空データ）: {row}")
                continue
            tags = [tag.strip() for tag in row[2:] if tag.strip()]
            add_note(front, back, tags)
        else:
            print(f"⚠️ スキップ（列数不足）: {row}")
