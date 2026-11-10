# 爬虫第1课：用 requests 抓取一个网页
import requests   # 老朋友：发 HTTP 请求

# 目标：抓一个公开的、允许爬取的网站
url = "https://quotes.toscrape.com/"

# 发请求（GET），拿到响应
resp = requests.get(url, timeout=10)

# 看响应状态码
print("状态码:", resp.status_code)     # 200 = 成功
print("网页长度:", len(resp.text), "字符")
print("---- 前 200 个字符 ----")
print(resp.text[:2000])
