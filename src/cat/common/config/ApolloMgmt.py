import os


class ApolloMgmt:
    # 从环境变量中获取数据库连接信息

    @staticmethod
    def get_property(key: str, default_value=None):
        return os.getenv(key, default_value)
