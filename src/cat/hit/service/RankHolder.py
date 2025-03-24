import json

from src.cat.common.config.Config import Config
from src.cat.common.model.constant.redis_keys import redis_key__rank_list
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
        Config.redis_client.set(redis_key__rank_list, json.dumps([r.dict() for r in rank]))
        return self

    def get_rank(self) -> [Rank]:
        # 从 Redis 中获取数据
        rank_json = Config.redis_client.get(redis_key__rank_list)
        if rank_json:
            # 将 JSON 字符串反序列化为字典列表
            rank_dicts = json.loads(rank_json)
            # 将字典列表转换为 Rank 对象列表
            return [Rank(**rank_dict) for rank_dict in rank_dicts]
        return []
