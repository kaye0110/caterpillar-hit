from typing import Optional

from pydantic import BaseModel


class Rank(BaseModel):
    code: str
    name: str
    data_date: str
    data_time: str
    open_price: float
    last_price: float
    high_price: float
    low_price: float
    pre_close_price: float
    change_rate: float
    first_derivative: Optional[float]
    second_derivative: Optional[float]
    second_derivative_mean: Optional[float]
    last_first_derivative: Optional[float]
    last_sec_derivative: Optional[float]
    last_sec_derivative_mean: Optional[float]
    rank: Optional[int]
    last_rank: Optional[int]
    rank_first_derivative: Optional[int]
    rank_second_derivative: Optional[int]
    rank_second_derivative_mean: Optional[int]
