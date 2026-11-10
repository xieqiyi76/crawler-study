# 爬虫第4课：自动翻页，爬全站 100 条名言
import requests
from bs4 import BeautifulSoup
import csv
import time          # 新朋友：时间控制，爬虫合规的关键

BASE = "https://quotes.toscrape.com"
all_data = []        # 大账本：装所有页的数据

page = 1
while True:          # “无限循环”，靠里面的判断决定什么时候停
    url = f"{BASE}/page/{page}/"          # 网址规律：page/1、page/2…
    resp = requests.get(url, timeout=10)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    quote_boxes = soup.select("div.quote")
    if not quote_boxes:                   # 这一页一条名言都没有 = 到头了
        print(f"第 {page} 页没有数据，全站爬完，收工！")
        break                             # 跳出无限循环

    for box in quote_boxes:
        text = box.select_one("span.text").text
        author = box.select_one("small.author").text
        tags = ",".join(t.text for t in box.select("a.tag"))
        all_data.append([text, author, tags])

    print(f"第 {page} 页完成，累计 {len(all_data)} 条")

    # 找“下一页”按钮：有就翻，没有就停（双保险停机法）
    next_btn = soup.select_one("li.next a")
    if not next_btn:
        print("没有下一页了，收工！")
        break

    page += 1                             # 页码 +1，进入下一轮循环
    time.sleep(1)                         # ★ 爬 1 秒歇 1 秒：对网站温柔

# 最后统一存 CSV（和第 3 课一样的手法）
with open("quotes_all.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["名言", "作者", "标签"])
    writer.writerows(all_data)

print(f"全部完成！共 {len(all_data)} 条名言已存入 quotes_all.csv")
