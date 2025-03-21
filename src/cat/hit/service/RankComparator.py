import pandas as pd

from src.cat.hit.model.Rank import Rank
from src.cat.hit.service.RankHolder import RankHolder


def remove_duplicates(ranks: [Rank]) -> [Rank]:
    # 将 Rank 对象列表转换为 DataFrame
    df = pd.DataFrame([rank.dict() for rank in ranks])

    # 根据 code、data_date、data_time 删除重复数据
    df = df.drop_duplicates(subset=['code', 'data_date', 'data_time'])

    # 将 DataFrame 转换回 Rank 对象列表
    unique_ranks = [Rank(**row) for row in df.to_dict('records')]

    return unique_ranks


def sort(ranks: [Rank]) -> [Rank]:
    ranks = remove_duplicates(ranks)
    # 处理 first_derivative 的排名
    first_derivatives = [r.first_derivative for r in ranks]
    sorted_first = sorted(first_derivatives, reverse=True)
    first_rank_map = {}
    for idx, value in enumerate(sorted_first):
        if value not in first_rank_map:
            first_rank_map[value] = idx + 1
    for rank in ranks:
        rank.rank_first_derivative = first_rank_map[rank.first_derivative]

    # 处理 second_derivative 的排名
    second_derivatives = [r.second_derivative for r in ranks]
    sorted_second = sorted(second_derivatives, reverse=True)
    second_rank_map = {}
    for idx, value in enumerate(sorted_second):
        if value not in second_rank_map:
            second_rank_map[value] = idx + 1
    for rank in ranks:
        rank.rank_second_derivative = second_rank_map[rank.second_derivative]

    # 处理 second_derivative_mean 的排名
    second_derivative_mean = [r.second_derivative_mean for r in ranks]
    second_derivative_mean = sorted(second_derivative_mean, reverse=True)
    second_derivative_mean_map = {}
    for idx, value in enumerate(second_derivative_mean):
        if value not in second_derivative_mean_map:
            second_derivative_mean_map[value] = idx + 1
    for rank in ranks:
        rank.rank_second_derivative_mean = second_derivative_mean_map[rank.second_derivative_mean]

    return ranks


class RankComparator:
    def __init__(self):
        pass

    def compare(self, last_rank: RankHolder, current_rank: RankHolder):
        pass
