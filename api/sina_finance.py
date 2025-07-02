# 新浪财经


import requests
import time
import random
from .parsers.parse_corp_info import parse_corp_info


# 获取公司简介信息
# https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/{code}.phtml
def get_corpInfo(code: str) -> dict:
    """
    获取公司简介信息
    :param code: 股票代码(如: 600000)
    :return: 包含公司信息的字典，失败返回None
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/{code}.phtml"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://finance.sina.com.cn/",
    }

    try:
        time.sleep(random.uniform(0.5, 2))
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return parse_corp_info(response.text)
    except Exception as e:
        print(f"获取公司信息失败: {e}")
        return None


from .parsers.parse_financial_info import parse_financial_info


# 获取公司财务信息
# https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{code}/displaytype/0.phtml
def get_financial_info(code: str) -> dict:
    """
    获取公司财务信息
    :param code: 股票代码(如: 600000)
    :return: 包含财务信息的字典，失败返回None
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{code}/displaytype/0.phtml"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://finance.sina.com.cn/",
    }

    try:
        time.sleep(random.uniform(0.5, 2))
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return parse_financial_info(response.text)
    except Exception as e:
        print(f"获取财务信息失败: {e}")
        return None
