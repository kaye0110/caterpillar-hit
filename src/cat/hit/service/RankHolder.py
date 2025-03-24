from src.cat.hit.model.Rank import Rank


class RankHolder:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.rank = []

    def set_rank(self, rank: [Rank]) -> "RankHolder":
        self.rank = rank
        return self

    def get_rank(self) -> [Rank]:
        return self.rank
