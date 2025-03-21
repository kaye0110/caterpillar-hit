import logging
import warnings

from src.cat.hit.model.Rank import Rank

warnings.filterwarnings("ignore", category=DeprecationWarning)


class QuoteAnalysis:
    def __init__(self, quote):
        self.quote = quote
        self.grouped_data = None
        self.rising_data = None
        self.falling_data = None

        self.result_rising = None
        self.result_falling = None

        self.top_size = 10
        pass

    def analysis(self) -> "QuoteAnalysis":
        if self.quote.all_data is None or len(self.quote.all_data) == 0:
            return self

        # 根据 code 分组，按 data_date 和 data_time 正向排序
        self.grouped_data = self.quote.all_data.groupby('code').apply(lambda x: x.sort_values(['data_date', 'data_time']))
        # 重置索引，将 code 从索引中移除
        self.grouped_data = self.grouped_data.reset_index(drop=True)
        self.grouped_data = self.grouped_data.dropna(subset=['last_price'])

        self.grouped_data['change_rate'] = round((self.grouped_data['last_price'] - self.grouped_data['open_price']) / self.grouped_data['open_price'], 4)
        # 计算一阶导数（价格变化速度）
        self.grouped_data['first_derivative'] = self.grouped_data.groupby('code')['last_price'].diff()

        # 计算二阶导数（速度变化的加速度）
        self.grouped_data['second_derivative'] = self.grouped_data.groupby('code')['first_derivative'].diff()

        # 计算每个 code 最近 10 次二阶导数的均值
        second_derivative_mean = self.grouped_data.groupby('code')['second_derivative'].apply(self._get_last_mean).reset_index(name='second_derivative_mean')

        valid_data = self.grouped_data.sort_values('data_time').groupby('code').last()
        valid_data = valid_data.merge(second_derivative_mean[['code', 'second_derivative_mean']], on='code', how='left')

        # 筛选出非空的一阶导数和二阶导数数据
        valid_data = valid_data.dropna(subset=['first_derivative', 'second_derivative'])

        if len(valid_data) == 0:
            return self

        # 筛选出上涨和下跌的数据
        self.rising_data = valid_data[valid_data['change_rate'] > 0]
        self.falling_data = valid_data[valid_data['change_rate'] < 0]

        # 分别取出上涨、下跌状态下加速度和变化速度倒序前 10 个
        rising_top_speed = self.rising_data.nlargest(self.top_size, 'first_derivative')
        rising_top_acceleration = self.rising_data.nlargest(self.top_size, 'second_derivative')
        rising_top_acceleration_mean = self.rising_data.nlargest(self.top_size, 'second_derivative_mean')

        falling_top_speed = self.falling_data.nsmallest(self.top_size, 'first_derivative')
        falling_top_acceleration = self.falling_data.nsmallest(self.top_size, 'second_derivative')
        falling_top_acceleration_mean = self.falling_data.nsmallest(self.top_size, 'second_derivative_mean')

        result_rising_top_speed = rising_top_speed.apply(lambda row: self._convert_to_entity(row), axis=1).tolist()
        result_rising_top_acceleration = rising_top_acceleration.apply(lambda row: self._convert_to_entity(row), axis=1).tolist()
        result_rising_top_acceleration_mean = rising_top_acceleration_mean.apply(lambda row: self._convert_to_entity(row), axis=1).tolist()

        result_falling_top_speed = falling_top_speed.apply(lambda row: self._convert_to_entity(row), axis=1).tolist()
        result_falling_top_acceleration = falling_top_acceleration.apply(lambda row: self._convert_to_entity(row), axis=1).tolist()
        result_falling_top_acceleration_mean = falling_top_acceleration_mean.apply(lambda row: self._convert_to_entity(row), axis=1).tolist()

        logging.getLogger(__name__).info("rising_top_speed: %s", result_rising_top_speed)
        logging.getLogger(__name__).info("rising_top_acceleration: %s", result_rising_top_acceleration)
        logging.getLogger(__name__).info("rising_top_acceleration_mean: %s", result_rising_top_acceleration_mean)
        logging.getLogger(__name__).info("falling_top_speed: %s", result_falling_top_speed)
        logging.getLogger(__name__).info("falling_top_acceleration: %s", result_falling_top_acceleration)
        logging.getLogger(__name__).info("falling_top_acceleration_mean: %s", result_falling_top_acceleration_mean)

        self.result_rising = result_rising_top_speed + result_rising_top_acceleration + result_rising_top_acceleration_mean

        return self

    @staticmethod
    def _convert_to_entity(row):
        data = {"code": row['code'],
                "name": row['name'],
                "first_derivative": row['first_derivative'],
                "open_price": row['open_price'],
                "close_price": row['close_price'],
                "high_price": row['high_price'],
                "low_price": row['low_price'],
                "pre_close_price": row['pre_close_price'],
                "change_rate": row['change_rate'],
                "second_derivative": row['second_derivative'],
                "second_derivative_mean": row['second_derivative_mean'],
                "last_sec_derivative": row['last_sec_derivative'],
                "last_sec_derivative_mean": row['last_sec_derivative_mean'],
                "rank": 0,
                "last_rank": 0}
        return Rank(**data)

    @staticmethod
    def _get_last_mean(series):
        return series.tail(10).mean()
