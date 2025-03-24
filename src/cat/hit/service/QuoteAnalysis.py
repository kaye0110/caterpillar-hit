import warnings

from src.cat.hit.model.Rank import Rank
from src.cat.hit.service.RankComparator import sort

warnings.filterwarnings("ignore", category=DeprecationWarning)


class QuoteAnalysis:
    def __init__(self, quote):
        self.quote = quote
        self.grouped_data = None
        self.rising_data = None
        self.falling_data = None

        self.result_rising = []
        self.result_falling = []

        self.top_size = 30
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

        if rising_top_speed is not None and len(rising_top_speed) > 0:
            result_rising_top_speed = rising_top_speed.apply(lambda row: self._convert_to_entity(row), axis=1).values.tolist()
            self.result_rising = self.result_rising + result_rising_top_speed
            # logging.getLogger(__name__).info("rising_top_speed: %s", result_rising_top_speed)

        if rising_top_acceleration is not None and len(rising_top_acceleration) > 0:
            result_rising_top_acceleration = rising_top_acceleration.apply(lambda row: self._convert_to_entity(row), axis=1).values.tolist()
            self.result_rising = self.result_rising + result_rising_top_acceleration
            # logging.getLogger(__name__).info("rising_top_acceleration: %s", result_rising_top_acceleration)

        if rising_top_acceleration_mean is not None and len(rising_top_acceleration_mean) > 0:
            result_rising_top_acceleration_mean = rising_top_acceleration_mean.apply(lambda row: self._convert_to_entity(row), axis=1).values.tolist()
            self.result_rising = self.result_rising + result_rising_top_acceleration_mean
            # logging.getLogger(__name__).info("rising_top_acceleration_mean: %s", result_rising_top_acceleration_mean)

        if falling_top_speed is not None and len(falling_top_speed) > 0:
            result_falling_top_speed = falling_top_speed.apply(lambda row: self._convert_to_entity(row), axis=1).values.tolist()
            self.result_falling = self.result_falling + result_falling_top_speed
            # logging.getLogger(__name__).info("falling_top_speed: %s", result_falling_top_speed)

        if falling_top_acceleration is not None and len(falling_top_acceleration) > 0:
            result_falling_top_acceleration = falling_top_acceleration.apply(lambda row: self._convert_to_entity(row), axis=1).values.tolist()
            self.result_falling = self.result_falling + result_falling_top_acceleration
            # logging.getLogger(__name__).info("falling_top_acceleration: %s", result_falling_top_acceleration)

        if falling_top_acceleration_mean is not None and len(falling_top_acceleration_mean) > 0:
            result_falling_top_acceleration_mean = falling_top_acceleration_mean.apply(lambda row: self._convert_to_entity(row), axis=1).values.tolist()
            self.result_falling = self.result_falling + result_falling_top_acceleration_mean
            # logging.getLogger(__name__).info("falling_top_acceleration_mean: %s", result_falling_top_acceleration_mean)

        self.result_falling = sort(self.result_falling)
        self.result_rising = sort(self.result_rising)

        # self.print_rank_table()
        return self

    def print_rank_table(self):
        """
        将 Rank 数组以表格形式打印到控制台。

        Args:
            ranks (List[Rank]): 需要打印的 Rank 对象列表。
        """
        # 定义所有字段名称
        fields = [
            'code', 'name', 'data_date', 'data_time',
            'open_price', 'last_price', 'high_price', 'low_price', 'pre_close_price',
            'change_rate', 'first_derivative', 'second_derivative', 'second_derivative_mean',
            'last_first_derivative', 'last_sec_derivative', 'last_sec_derivative_mean',
            'rank', 'last_rank', 'rank_first_derivative', 'rank_second_derivative', 'rank_second_derivative_mean'
        ]

        # 表头格式化（首字母大写，下划线替换为空格）
        header = [field.replace('_', ' ').title() for field in fields]

        # 准备数据行
        data_rows = []
        for rank in self.result_rising:
            row = []
            for field in fields:
                value = getattr(rank, field)
                # 将 None 显示为 '-'
                row.append(str(value) if value is not None else '-')
            data_rows.append(row)

        # 计算每列的最大宽度
        max_widths = {field: len(header[i]) for i, field in enumerate(fields)}
        for row in data_rows:
            for i, cell in enumerate(row):
                if len(cell) > max_widths[fields[i]]:
                    max_widths[fields[i]] = len(cell)

        # 生成分隔符行
        separator = ['-' * max_widths[field] for field in fields]

        # 打印表格
        print(' | '.join(header))
        print(' | '.join(separator))
        for row in data_rows:
            # 对齐每列
            formatted_row = [cell.ljust(max_widths[fields[i]]) for i, cell in enumerate(row)]
            print(' | '.join(formatted_row))

    @staticmethod
    def _convert_to_entity(row):
        data = {
            "code": row.get('code', None),
            "name": row.get('name', None),
            "data_date": row.get('data_date', None),
            "data_time": row.get('data_time', None),
            "first_derivative": row.get('first_derivative', 0),
            "last_price": row.get('last_price', 0),
            "open_price": row.get('open_price', 0),
            "high_price": row.get('high_price', 0),
            "low_price": row.get('low_price', 0),
            "pre_close_price": row.get('prev_close_price', 0),
            "change_rate": row.get('change_rate', 0),
            "second_derivative": row.get('second_derivative', 0),
            "second_derivative_mean": row.get('second_derivative_mean', 0),
            "last_sec_derivative": row.get('last_sec_derivative', 0),
            "last_sec_derivative_mean": row.get('last_sec_derivative_mean', 0),
            "rank": 0,
            "last_rank": 0,
            "last_first_derivative": 0,
            "rank_first_derivative": 0,
            "rank_second_derivative": 0,
            "rank_second_derivative_mean": 0
        }
        return Rank(**data)

    @staticmethod
    def _get_last_mean(series):
        return series.tail(10).mean()
