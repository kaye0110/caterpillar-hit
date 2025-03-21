import pandas as pd


class RankHolder:
    def __init__(self):
        self.rank = {}

    def init(self, data: pd.DataFrame):
        self.rank = {}
        for code in data['code'].unique():
            self.rank[code] = data[data['code'] == code]

    def get_rank(self) -> dict:
        return self.rank
