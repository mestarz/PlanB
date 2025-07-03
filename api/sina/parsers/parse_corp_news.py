import re

from bs4 import BeautifulSoup

from ..utils import get_sina_new_content


def parse_core_news_urls(soup: BeautifulSoup) -> list[str]:
    datalist = soup.find("div", id="con02-7")
    # 只查看第一页
    list = datalist.find_all(
        "a", target="_blank", href=re.compile(r"^https://finance.sina.com.cn/")
    )
    news_links = [i.get("href") for i in list]
    return news_links


def parse_corp_news(urls: list[str]) -> list[str]:
    news = []
    for url in urls:
        news.append(get_sina_new_content(url))
    return news
