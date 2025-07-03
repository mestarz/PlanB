import re
import pandas as pd

from bs4 import BeautifulSoup, Tag


def parse_financial_info(soup: BeautifulSoup) -> pd.DataFrame:
    financial_data = None

    tables = soup.find_all("table", id=re.compile(r"BalanceSheetNewTable\d+"))

    for table in tables:
        data = parse_financial_table(table)
        if financial_data is None:
            financial_data = data
        else:
            financial_data = pd.concat([financial_data, data], ignore_index=True)

    return financial_data


def parse_financial_table(table: Tag) -> pd.DataFrame:
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
