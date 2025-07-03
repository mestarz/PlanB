import time
import random
import requests
import re
from bs4 import BeautifulSoup


def get_url_content(url: str) -> BeautifulSoup:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    }

    try:
        time.sleep(random.uniform(0.5, 2))
        # response = requests.get(url, headers=headers, timeout=10)
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"网络访问失败: {e}, {url}")
        return None


def _decode_sina_content(html_bytes):
    """专门处理新浪财经的复杂编码情况"""
    # 方法1：优先尝试从HTML meta标签提取真实编码
    try:
        meta_charset = re.search(rb'<meta[^>]+charset=["\']?([\w-]+)', html_bytes, re.I)
        if meta_charset:
            encoding = meta_charset.group(1).decode("ascii").lower()
            if "gb" in encoding:
                return html_bytes.decode("gb18030", errors="replace")
            return html_bytes.decode(encoding, errors="replace")
    except:
        pass

    # 方法2：尝试常见中文编码
    for encoding in ["gb18030", "gbk", "utf-8", "gb2312"]:
        try:
            return html_bytes.decode(encoding)
        except:
            continue

    # 方法3：最终回退方案
    return html_bytes.decode("gb18030", errors="replace")


def get_sina_new_content(url: str) -> str:
    # 使用示例
    url = "https://finance.sina.com.cn/roll/2025-07-03/doc-infeevpm3957267.shtml"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    }

    try:
        # 获取原始字节数据
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 使用专用解码函数
        html_content = _decode_sina_content(response.content)

        # 使用BeautifulSoup修复可能的编码残留问题
        soup = BeautifulSoup(html_content, "lxml")

        # 提取正文内容（新浪财经的特定选择器）
        main_content = soup.select_one(".article") or soup.select_one("#artibody")

        if main_content:
            # 清理不需要的元素
            for elem in main_content.select(
                ".app-kaihu-qr, .creaders, .source, .show_author"
            ):
                elem.decompose()

            # 获取纯文本
            clean_text = main_content.get_text(separator="\n", strip=True)
            return clean_text
        else:
            print("未找到正文内容，请检查选择器")
            print(soup.prettify()[:2000])  # 输出部分HTML用于调试
            return ""

    except Exception as e:
        print(f"发生错误: {e}")
        return ""
