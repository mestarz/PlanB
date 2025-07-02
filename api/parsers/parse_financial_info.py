import re
import pandas as pd

from bs4 import BeautifulSoup, Tag


def parse_financial_info(html_content: str) -> pd.DataFrame:
    """
    从新浪财经财务数据HTML中提取关键财务指标并按年份组织
    :param html_content: 包含财务数据的HTML内容
    :return: 按年份组织的财务指标字典
    """
    soup = BeautifulSoup(html_content, "html.parser")
    financial_data = None

    # 查找所有财务表格 - 更精确地匹配表格ID
    tables = soup.find_all("table", id=re.compile(r"BalanceSheetNewTable\d+"))

    for table in tables:
        # 提取报告日期行
        data = parse_financial_table(table)
        if financial_data is None:
            financial_data = data
        else:
            financial_data = pd.concat([financial_data, data], ignore_index=True)

    return financial_data


def parse_financial_table(table: Tag) -> pd.DataFrame:
    """
    解析单个财务表格数据
    :param table: BeautifulSoup表格对象
    :return: 按年份组织的财务指标字典
    """
    # 提取报告日期行
    tbody = table.find("tbody")
    date_rows = tbody.find_all("tr")
    r = {}
    for row in date_rows:
        tds = row.find_all("td")
        if len(tds) <= 1: 
            continue
        r[tds[0].get_text(strip=True)] = [td.get_text(strip=True) for td in tds[1:]]

    r = pd.DataFrame(r)
    return r
