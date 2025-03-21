from futu import *

from src.cat.hit.service.QuoteAnalysis import QuoteAnalysis
from src.cat.hit.service.QuoteHolder import QuoteHolder

quote = QuoteHolder()

class QuoteHandler(StockQuoteHandlerBase):
    # 定义一个处理股票报价的类，继承自StockQuoteHandlerBase
    def on_recv_rsp(self, rsp_pb):
        # 定义一个方法来处理接收到的响应，参数rsp_pb是响应的protobuf对象
        ret_code, data = super(QuoteHandler, self).on_recv_rsp(rsp_pb)
        # 调用父类的on_recv_rsp方法处理响应，获取返回码ret_code和数据data
        if ret_code != RET_OK:
            # 如果返回码不是RET_OK（表示成功），则打印错误信息
            print("StockQuoteTest: error, msg: %s" % data)
            # 打印错误信息，%s是字符串格式化占位符，data是错误信息内容
            return RET_ERROR, data

            # 返回错误码RET_ERROR和错误信息data
        QuoteAnalysis(quote.append(data)).analysis()

        # 创建一个QuoteHolder对象，将数据data追加到其中
        # 然后创建一个QuoteAnalysis对象，传入包含数据的QuoteHolder对象，并调用其analysis方法进行数据分析
        return RET_OK, data


class FutuService:
    def __init__(self):
        pass

    @staticmethod
    def subscribe():
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        handler = QuoteHandler()
        quote_ctx.set_handler(handler)  # 设置实时报价回调
        ret, data = quote_ctx.subscribe(['SH.600021', 'SH.600020', 'SH.600022', 'SH.600025'], [SubType.QUOTE])  # 订阅实时报价类型，OpenD 开始持续收到服务器的推送
        if ret == RET_OK:
            print(data)
        else:
            print('error:', data)
        time.sleep(60 * 60 * 60)  # 设置脚本接收 OpenD 的推送持续时间为15秒
        quote_ctx.close()  # 关闭当条连接，OpenD 会在1分钟后自动取消相应股票相应类型的订阅


FutuService().subscribe()
