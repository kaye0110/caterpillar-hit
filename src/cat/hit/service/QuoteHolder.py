import pandas as pd


class QuoteHolder:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.all_data = pd.DataFrame()

    def append(self, data: pd.DataFrame) -> "QuoteHolder":
        self.all_data = pd.concat([self.all_data, data], axis=0)
        self.all_data = self.all_data.drop_duplicates(subset=['code', 'data_date', 'data_time'], keep='last')
        return self
