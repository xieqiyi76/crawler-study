# 爬虫第2课：解析网页，提取名言 + 作者 + 标签
import requests
from bs4 import BeautifulSoup     # 今天的新武器：HTML 解析器

# 还是新手村木桩（quotes.toscrape.com）
url = "https://quotes.toscrape.com/"

# 第1步：拿网页（上一课学的）
resp = requests.get(url, timeout=10)
resp.encoding = "utf-8"           # 告诉程序用 utf-8 读，防中文乱码

# 第2步：交给 BeautifulSoup 解析
soup = BeautifulSoup(resp.text, "html.parser")   # 现在手里有个"可查询的"网页对象

# 第3步：用 CSS 选择器"点菜"——只挑我要的部分
quotes = soup.select("span.text")       # 拿到这一页所有"名言"（10条）
authors = soup.select("small.author")   # 拿到所有"作者名"
tags = soup.select("div.tags a.tag")    # 拿到所有"标签"

# 第4步：把提取结果打印出来看看
print("这一页有", len(quotes), "条名言\n")
for i in range(len(quotes)):
    # .text 属性 = 只取标签里的文字，扔掉标签本身
    q = quotes[i].text
    a = authors[i].text
    tag_list = [t.text for t in tags[i*0:]]  # 先简化：标签下节课细抠
    print(f"{i+1}. {a} 说：{q[:50]}...")      # 每条只打印前50字，防刷屏

# 顺手验证一下第一句名言的标签
print("\n第一条名言的标签：")
for t in soup.select("div.quote")[0].select("a.tag"):
    print(" -", t.text)
