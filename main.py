from api.sina.sina_finance import get_financial_info


def main():
    code = "300059"
    financial = get_financial_info(code)
    financial.to_csv(f"financial_{code}.csv", index=False)
    print(financial)

if __name__ == "__main__":
    main()
