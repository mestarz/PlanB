# 新浪财经

from .parsers.parse_corp_info import parse_corp_info
from .parsers.parse_financial_info import parse_financial_info
from .parsers.parse_corp_news import parse_corp_news, parse_core_news_urls
from .utils import get_url_content


# 获取公司简介信息
# https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/{code}.phtml
def get_corpInfo(code: str) -> dict:
    """
    获取公司简介信息
    :param code: 股票代码(如: 600000)
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/{code}.phtml"
    context = get_url_content(url=url)
    if context is None:
        return None
    return parse_corp_info(context)


# 获取公司财务信息
# https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{code}/displaytype/0.phtml
def get_financial_info(code: str) -> dict:
    """
    获取公司财务信息
    :param code: 股票代码(如: 600000)
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{code}/displaytype/0.phtml"

    context = get_url_content(url=url)
    if context is None:
        return None

    return parse_financial_info(context)


# 获取公司新闻
# https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/{code}.phtml
def get_corp_news(code: str) -> list:
    """
    获取公司新闻
    :param code: 股票代码(如: sz.600000)
    :return: 包含公司新闻的列表，失败返回空列表
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/{code}.phtml"

    context = get_url_content(url=url)

    if context is None:
        return None

    urls = parse_core_news_urls(context)
    return parse_corp_news(urls)
