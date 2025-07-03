from api.sina.sina_finance import get_corp_news

if __name__ == "__main__":
    stock_code = "sz301628"
    r = get_corp_news(stock_code)
    print(r)