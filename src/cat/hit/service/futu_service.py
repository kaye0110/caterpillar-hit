import warnings

from futu import *

warnings.filterwarnings("ignore", category=DeprecationWarning)
all_data = pd.DataFrame()


class QuoteCalculator:
    def __init__(self):
        self.all_data = pd.DataFrame()

    def append(self, data: pd.DataFrame) -> "QuoteCalculator":
        self.all_data = pd.concat([self.all_data, data], axis=0)
        self.all_data = self.all_data.drop_duplicates(subset=['code', 'data_date', 'data_time'], keep='last')

        return self

    def calculate(self) -> "QuoteCalculator":
        if self.all_data is None:
            return self

        # 根据 code 分组，按 data_date 和 data_time 正向排序
        grouped = self.all_data.groupby('code').apply(lambda x: x.sort_values(['data_date', 'data_time']))
        # 重置索引，将 code 从索引中移除
        grouped = grouped.reset_index(drop=True)
        grouped = grouped.dropna(subset=['last_price'])
        # 计算一阶导数（价格变化速度）
        grouped['first_derivative'] = grouped.groupby('code')['last_price'].diff()

        # 计算二阶导数（速度变化的加速度）
        grouped['second_derivative'] = grouped.groupby('code')['first_derivative'].diff()

        # 筛选出非空的一阶导数和二阶导数数据
        valid_data = grouped.dropna(subset=['first_derivative', 'second_derivative'])

        if len(valid_data) == 0:
            return self

        # 筛选出上涨和下跌的数据
        rising_data = valid_data[valid_data['first_derivative'] > 0]
        falling_data = valid_data[valid_data['first_derivative'] < 0]

        # 分别取出上涨、下跌状态下加速度和变化速度倒序前 10 个
        rising_top_10_speed = rising_data.nlargest(10, 'first_derivative')
        rising_top_10_acceleration = rising_data.nlargest(10, 'second_derivative')
        falling_top_10_speed = falling_data.nsmallest(10, 'first_derivative')
        falling_top_10_acceleration = falling_data.nsmallest(10, 'second_derivative')

        def get_last_10_mean(series):
            return series.tail(10).mean()

        # 计算每个 code 最近 10 次二阶导数的均值
        second_derivative_mean = grouped.groupby('code')['second_derivative'].apply(get_last_10_mean).reset_index(name='second_derivative_mean')

        # 筛选出非空的均值数据
        valid_second_derivative_mean = second_derivative_mean.dropna(subset=['second_derivative_mean'])

        # 分别取出上涨、下跌状态下加速度均值倒序前 10 个
        rising_second_derivative_mean = valid_second_derivative_mean[valid_second_derivative_mean['second_derivative_mean'] > 0]
        falling_second_derivative_mean = valid_second_derivative_mean[valid_second_derivative_mean['second_derivative_mean'] < 0]

        rising_top_10_acceleration_mean = rising_second_derivative_mean.nlargest(10, 'second_derivative_mean')
        falling_top_10_acceleration_mean = falling_second_derivative_mean.nsmallest(10, 'second_derivative_mean')

        print("上涨 - 变化速度前 10:")
        print(rising_top_10_speed[['code', 'name', 'first_derivative']])
        print("上涨 - 加速度前 10:")
        print(rising_top_10_acceleration[['code', 'name', 'second_derivative']])
        print("上涨 - 加速度 Mean 前 10:")
        print(rising_top_10_acceleration_mean[['code', 'name', 'second_derivative']])

        print("下跌 - 变化速度前 10:")
        print(falling_top_10_speed[['code', 'name', 'first_derivative']])
        print("下跌 - 加速度前 10:")
        print(falling_top_10_acceleration[['code', 'name', 'second_derivative']])
        print("下跌 - 加速度 Mean 前 10:")
        print(falling_top_10_acceleration_mean[['code', 'name', 'second_derivative']])

        return self


calculator = QuoteCalculator()


class SimpleQuoteHandler(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(SimpleQuoteHandler, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("StockQuoteTest: error, msg: %s" % data)
            return RET_ERROR, data

        calculator.append(data).calculate()

        return RET_OK, data


quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
handler = SimpleQuoteHandler()
quote_ctx.set_handler(handler)  # 设置实时报价回调
ret, data = quote_ctx.subscribe(['SH.600021', 'SH.600020', 'SH.600022', 'SH.600025'], [SubType.QUOTE])  # 订阅实时报价类型，OpenD 开始持续收到服务器的推送
if ret == RET_OK:
    print(data)
else:
    print('error:', data)
time.sleep(60 * 60 * 60)  # 设置脚本接收 OpenD 的推送持续时间为15秒
quote_ctx.close()  # 关闭当条连接，OpenD 会在1分钟后自动取消相应股票相应类型的订阅
