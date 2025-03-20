class StrTools:
    @staticmethod
    def split_string_if_has_comma(s):
        """
        判断字符串中是否包含逗号，如果包含则按逗号分割成列表，否则返回原字符串作为列表的唯一元素
        :param s: 输入的字符串
        :return: 分割后的列表
        """
        if ',' in s:
            return s.split(',')
        return [s]
