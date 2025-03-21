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
    first_derivative: float
    second_derivative: float
    second_derivative_mean: float
    last_first_derivative: float
    last_sec_derivative: float
    last_sec_derivative_mean: float
    rank: int
    last_rank: int
    rank_first_derivative: int
    rank_second_derivative: int
    rank_second_derivative_mean: int
