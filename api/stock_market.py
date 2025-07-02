# BaoStock
# http://baostock.com/baostock/index.php/Python_API%E6%96%87%E6%A1%A3

import baostock as bs
import pandas as pd

from baostock.data.resultset import ResultData

from .time import TimeLevel


class BaoStockMarket:
    def __init__(self):
        self.is_login = False

    def __del__(self):
        pass

    def _check_login(self):
        if not self.is_login:
            _ = bs.login()
            self.is_login = True

    @staticmethod
    def _get_result(res: ResultData) -> pd.DataFrame:
        if res.error_code != "0":
            print(f"[Error] baostock get result error! {res.error_msg}")
        data_list = []
        while res.error_code == "0" and res.next():
            data_list.append(res.get_row_data())
        result = pd.DataFrame(data_list)
        return result

    def query_stock_history(
        self, code: str, start_date: str, end_date: str, frequency: TimeLevel
    ) -> pd.DataFrame:
        self._check_login()
        f = frequency.get_baostock_freq()
        fields = "date,time,open,high,low,close,volume"
        if frequency.is_day_or_more():
            fields = "date,open,high,low,close,volume"

        r = bs.query_history_k_data_plus(
            code=code,
            fields=fields,
            start_date=start_date,
            end_date=end_date,
            frequency=f,
            adjustflag="2",
        )  # 前复权
        result = self._get_result(r)

        if len(result) == 0:
            return pd.DataFrame()

        result.columns = r.fields
        result.replace("", 0, inplace=True)
        for item in ["open", "high", "low", "close"]:
            result[item] = result[item].astype(float)
        result["volume"] = result["volume"].astype(int)
        result = result.rename(
            columns={
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "volume": "Volume",
            }
        )
        return result

    def query_all_code(self, day: str = None) -> pd.DataFrame:
        self._check_login()
        r = bs.query_all_stock(day)
        return self._get_result(r)

    def query_all_code_by_cache(self) -> pd.DataFrame:
        # 从all_stock.csv中读取数据
        import os

        cache_path = os.path.abspath(__file__)
        cache_path = os.path.join(os.path.dirname(cache_path), "all_stock.csv")
        return pd.read_csv(cache_path, dtype={"code": str, "status": int, "name": str})

    def get_stock_pool(self) -> pd.DataFrame:
        # 获取股票池
        df = self.query_all_code_by_cache()

        # 获取科创版 sh.688* , 创业板 sz.300*， sz.301*，ST股票
        df = df[
            (df["code"].str.startswith("sh.688"))
            | (df["code"].str.startswith("sz.300"))
            | (df["code"].str.startswith("sz.301"))
            | (df["name"].str.contains("ST"))
        ]

        return df
