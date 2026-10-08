```
import json
import os
import urllib.request

PRODUCT_URL = "https://markaware.jp/products/cashmere-double-faced-cloth-duffle-coat-black.js"
PAGE_URL = "https://markaware.jp/products/cashmere-double-faced-cloth-duffle-coat-black"

WEBHOOK = os.environ["DISCORD_WEBHOOK"]
STATE_FILE = "state.json"

def get_product():
    request = urllib.request.Request(
        PRODUCT_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))

def find_size_1(product):
    for variant in product["variants"]:
        title = str(variant.get("title", "")).strip()

        if title == "1":
            return variant

    return None

def send_discord(message):
    data = json.dumps({
        "content": message
    }).encode("utf-8")

    request = urllib.request.Request(
        WEBHOOK,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    urllib.request.urlopen(request, timeout=20)

def load_state():
    if not os.path.exists(STATE_FILE):
        return False

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("size_1_available", False)
    except Exception:
        return False

def save_state(available):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"size_1_available": available},
            f,
            ensure_ascii=False,
            indent=2
        )

product = get_product()
variant = find_size_1(product)

if variant is None:
    raise RuntimeError("サイズ1のバリエーションが見つかりませんでした。")

available = bool(variant.get("available", False))
previous = load_state()

print("サイズ1:", "在庫あり" if available else "在庫なし")

if available and not previous:
    send_discord(
        "🚨 サイズ1の在庫が入りました！\n\n"
        "MARKAWARE カシミヤリバー / ダッフルコート, Black\n\n"
        + PAGE_URL
    )

save_state(available)
```
