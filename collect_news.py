import csv, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone

CONFIGS = [
    ("ko", "전기차", "hl=ko&gl=KR&ceid=KR:ko"),
    ("en", "electric vehicle", "hl=en-US&gl=US&ceid=US:en"),
]
MAX = 100
now = datetime.now(timezone.utc)
collected_at = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
rows = []
for lang, kw, loc in CONFIGS:
    q = urllib.parse.quote(f"{kw} when:30d")
    url = f"https://news.google.com/rss/search?q={q}&{loc}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
    n = 0
    for it in root.iter("item"):
        pub = parsedate_to_datetime(it.findtext("pubDate"))
        if now - pub > timedelta(days=30):
            continue
        src = it.find("source")
        rows.append({"언어": lang, "제목": it.findtext("title"),
                     "발행일": pub.astimezone().strftime("%Y-%m-%d %H:%M:%S"),
                     "매체": src.text if src is not None else "",
                     "링크": it.findtext("link"), "수집시각": collected_at})
        n += 1
        if n >= MAX: break
with open("ev_news_raw.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["언어","제목","발행일","매체","링크","수집시각"])
    w.writeheader(); w.writerows(rows)
for lang, _, _ in CONFIGS:
    r = [x for x in rows if x["언어"] == lang]
    print(f"[{lang}] {len(r)}건")
    for x in r[:3]: print("  -", x["제목"])
