# 爬虫第5课：服务器定时版 —— 每天一存，文件名带日期，历史不覆盖
import requests
from bs4 import BeautifulSoup
import csv
import time
import os
from datetime import date        # 拿今天的日期

BASE = "https://quotes.toscrape.com"
all_data = []

page = 1
while True:
    url = f"{BASE}/page/{page}/"
    resp = requests.get(url, timeout=10)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    quote_boxes = soup.select("div.quote")
    if not quote_boxes:              # 这页空了 = 到头了
        break
    for box in quote_boxes:
        text = box.select_one("span.text").text
        author = box.select_one("small.author").text
        tags = ",".join(t.text for t in box.select("a.tag"))
        all_data.append([text, author, tags])
    if not soup.select_one("li.next a"):
        break
    page += 1
    time.sleep(1)                    # 爬 1 秒歇 1 秒

# ★ 关键改动1：文件名带日期，每天一个新文件，历史不覆盖
today = date.today().isoformat()
filename = f"/opt/crawler/quotes_{today}.csv"

# ★ 关键改动2：输出目录固定到 /opt/crawler，不存在就自动创建
os.makedirs("/opt/crawler", exist_ok=True)

with open(filename, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["名言", "作者", "标签"])
    writer.writerows(all_data)

print(f"完成：{len(all_data)} 条 → {filename}")
