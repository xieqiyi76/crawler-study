# 爬虫第3课：完整流水线 —— 抓取 → 解析 → 存 CSV
import requests
from bs4 import BeautifulSoup
import csv                     # Python 自带，专门读写 CSV

# ========== 第1步：抓取 ==========
url = "https://quotes.toscrape.com/"
resp = requests.get(url, timeout=10)
resp.encoding = "utf-8"

# ========== 第2步：解析 ==========
soup = BeautifulSoup(resp.text, "html.parser")

# 这次换个更聪明的抓法：按“一条名言一个盒子”来取
# 每条名言整体包在 <div class="quote"> 里，先拿盒子，再从盒子里挑东西
quote_boxes = soup.select("div.quote")       # 10 个盒子，一盒一条名言

data = []   # 空列表，准备装整理好的数据
for box in quote_boxes:
    text = box.select_one("span.text").text       # 盒子里的名言
    author = box.select_one("small.author").text  # 盒子里的作者
    tags = [t.text for t in box.select("a.tag")]  # 盒子里所有标签（列表）
    tags_str = ",".join(tags)                     # 列表拼成字符串："change,deep-thoughts"
    data.append([text, author, tags_str])         # 一行数据进列表

# ========== 第3步：存 CSV ==========
with open("quotes.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["名言", "作者", "标签"])       # 第一行：表头
    writer.writerows(data)                       # 后面：数据一行一航入座

print(f"搞定！共 {len(data)} 条名言已存入 quotes.csv")
