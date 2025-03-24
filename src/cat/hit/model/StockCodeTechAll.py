from src.cat.hit.model.StockCodeAi import stock_code_ai
from src.cat.hit.model.StockCodeIC import stock_code_ic
from src.cat.hit.model.StockCodeMeeting import meeting_0217
from src.cat.hit.model.StockCodeRobot import stock_code_robot


def _convert_to_entity(stock_code_array: []) -> [str]:
    ret = []
    for code in stock_code_array:
        if code and '.' in code:
            parts = code.split('.')
            ret.append(f"{parts[1]}.{parts[0]}")

    return ret


stock_code_tech_all_tmp = stock_code_robot + stock_code_ai + meeting_0217 + stock_code_ic

stock_code_tech_all_set = set(stock_code_tech_all_tmp)

stock_code_tech_all = list(stock_code_tech_all_set)

stock_code_tech_all = _convert_to_entity(stock_code_tech_all)

stock_code_tech_all = stock_code_tech_all[:100]

# print(len(stock_code_tech_all))
