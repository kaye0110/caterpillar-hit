from futu import *

from src.cat.common.config.ApolloMgmt import ApolloMgmt
from src.cat.common.config.Config import Config
from src.cat.common.config.RedisMgmt import RedisLock
from src.cat.common.model.constant.redis_keys import redis_key__lock_futu, redis_key__processor_futu_subscribe
from src.cat.hit.model.StockCodeTechAll import stock_code_tech_all
from src.cat.hit.service.QuoteAnalysis import QuoteAnalysis
from src.cat.hit.service.QuoteHolder import QuoteHolder
from src.cat.hit.service.RankHolder import RankHolder

quote = QuoteHolder()


class QuoteHandler(StockQuoteHandlerBase):
    # 定义一个处理股票报价的类，继承自StockQuoteHandlerBase
    def on_recv_rsp(self, rsp_pb):
        # 定义一个方法来处理接收到的响应，参数rsp_pb是响应的protobuf对象
        ret_code, data = super(QuoteHandler, self).on_recv_rsp(rsp_pb)
        # 调用父类的on_recv_rsp方法处理响应，获取返回码ret_code和数据data
        if ret_code != RET_OK:
            # 如果返回码不是RET_OK（表示成功），则打印错误信息
            logging.getLogger(__name__).info(f"StockQuoteTest: error, msg: {data}")
            # 打印错误信息，%s是字符串格式化占位符，data是错误信息内容
            return RET_ERROR, data

            # 返回错误码RET_ERROR和错误信息data
        RankHolder().set_rank(QuoteAnalysis(quote.append(data)).analysis().result_rising)

        # 创建一个QuoteHolder对象，将数据data追加到其中
        # 然后创建一个QuoteAnalysis对象，传入包含数据的QuoteHolder对象，并调用其analysis方法进行数据分析
        return RET_OK, data


class FutuService:
    def __init__(self):
        self.is_registered = False
        self.process_id = os.getpid()

    def unsubscribe(self) -> "FutuService":
        Config.redis_client.delete(redis_key__processor_futu_subscribe)
        Config.redis_client.delete(redis_key__lock_futu)
        return self._do_unsubscribe()

    def subscribe(self, stock_list: [] = stock_code_tech_all):
        lock = RedisLock(redis_key__lock_futu, expire=10)
        if lock.acquire():
            try:
                process_id = Config.redis_client.get(redis_key__processor_futu_subscribe)
                if process_id is None or int(process_id) == self.process_id:
                    logging.getLogger(__name__).info("Lock acquired, performing critical section...")
                    # Simulate critical section operations
                    redis_resp = Config.redis_client.set(redis_key__processor_futu_subscribe, self.process_id)
                    if redis_resp:
                        logging.getLogger(__name__).info(f"Lock acquired, {redis_resp} {self.process_id}")
                else:

                    logging.getLogger(__name__).info(f"Lock acquired by another process. {process_id}")
                    return

            finally:
                lock.release()
                logging.getLogger(__name__).info("Lock released.")
        else:
            logging.getLogger(__name__).info(f"Failed to acquire lock. {self.process_id}")

        self._do_unsubscribe()
        self._do_subscribe(stock_list=stock_list)

    def _is_current_process(self):
        return Config.redis_client.get(redis_key__processor_futu_subscribe) == self.process_id

    def _do_unsubscribe(self) -> "FutuService":

        quote_ctx = OpenQuoteContext(host=ApolloMgmt.get_property("futu.host"), port=int(ApolloMgmt.get_property("futu.port")))
        handler = QuoteHandler()
        quote_ctx.set_handler(handler)
        ret_unsub, err_message_unsub = quote_ctx.unsubscribe_all()  # 设置实时报价回调
        if ret_unsub == RET_OK:
            logging.getLogger(__name__).info(f'unsubscribe all successfully！current subscription status: {quote_ctx.query_subscription()}')  # 取消订阅后查询订阅状态
        else:
            logging.getLogger(__name__).info(f'Failed to cancel all subscriptions！{err_message_unsub}')

        return self

    def _do_subscribe(self, stock_list: [] = stock_code_tech_all) -> "FutuService":

        quote_ctx = OpenQuoteContext(host=ApolloMgmt.get_property("futu.host"), port=int(ApolloMgmt.get_property("futu.port")))
        handler = QuoteHandler()
        quote_ctx.set_handler(handler)
        ret, data = quote_ctx.subscribe(stock_list, [SubType.QUOTE])  # 订阅实时报价类型，OpenD 开始持续收到服务器的推送
        if ret == RET_OK:
            logging.getLogger(__name__).info(data)
        else:
            logging.getLogger(__name__).info(f'error:{data}')

        time.sleep(60 * 60 * 24)  # 设置脚本接收 OpenD 的推送持续时间为15秒
        quote_ctx.close()  # 关闭当条连接，OpenD 会在1分钟后自动取消相应股票相应类型的订阅

        return self
