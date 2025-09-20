# anki_tools

Anki にカードを自動追加するための Python ツールです。  
[AnkiConnect](https://ankiweb.net/shared/info/2055492159) アドオンを利用します。

---

## ディレクトリ構成

```
anki_tools/
├── data/
│   ├── notes_sample.csv      # サンプル入力（CSV）
│   ├── notes_sample.json     # サンプル入力（JSON）
├── tools/
│   ├── __init__.py
│   ├── add_notes.py          # メインスクリプト
│   └── client.py             # AnkiConnect クライアント
├── config.sample.yaml        # 設定サンプル
├── requirements.txt          # 必要ライブラリ
└── README.md
```

---

## 特徴
- **JSON / CSV** からカードを追加可能
- **設定ファイル (`config.yaml`)** に基づいて実行
- クローン直後でも **サンプルデータ** で動作確認が可能

---

## インストール

```bash
git clone https://github.com/yourname/anki_tools.git
cd anki_tools
````

必要なライブラリをインストールします：

```bash
pip install -r requirements.txt
```

---

## 使い方

1. **Anki を起動**し、AnkiConnect アドオン（ID: 2055492159）が有効になっていることを確認してください。

2. サンプルで動作確認（そのままでもOK）

   ```bash
   python -m tools.add_notes
   ```

   → デッキ「Default」にサンプルカードが追加されます。

3. 実運用する場合は `config.sample.yaml` をコピーして編集します。

   ```bash
   cp config.sample.yaml config.yaml
   ```

   * `deck`: 追加先デッキ名
   * `model`: ノートタイプ（通常は `"Basic"`）
   * `input`: 入力ファイル（`.json` または `.csv`）
   * `tags`: 追加時に付与するタグのリスト

   例 (`config.yaml`)：

   ```yaml
   deck: "MyDeck"
   model: "Basic"
   input: "data/my_notes.json"
   host: "http://localhost"
   port: 8765
   allow_duplicate: false
   tags:
     - "imported"
   ```

4. 実行：

   ```bash
   python -m tools.add_notes
   ```

---

## 入力ファイル形式

### JSON

```json
[
  {"front": "Hello", "back": "こんにちは", "tags": ["greet", "en-ja"]},
  {"front": "Apple", "back": "りんご"}
]
```

### CSV

```csv
front,back,tags
Dog,犬,"animal;en-ja"
Cat,猫,
```

* `tags` 列は `;` 区切り
* 空でも可

---

## 注意事項

* `config.yaml` は **.gitignore** で無視されます。各自の環境で作成してください。
* `config.sample.yaml` と `data/notes_sample.*` は **サンプル用** なのでそのままコミットされています。

---