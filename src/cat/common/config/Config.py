from src.cat.common.config.ApolloMgmt import ApolloMgmt
from src.cat.common.config.AzureMgmt import AzureMgmt
from src.cat.common.config.DeepSeekMgmt import DeepSeekMgmt
from src.cat.common.config.LoggerMgmt import LoggerMgmt
from src.cat.common.config.RedisMgmt import RedisMgmt


class Config(object):
    apollo = ApolloMgmt()
    logger = LoggerMgmt()
    database = None  # PostgreSQLMgmt()
    deepseek = DeepSeekMgmt()
    azure = AzureMgmt()
    redis_client = RedisMgmt.REDIS_CLIENT

    @staticmethod
    def get_db():
        db = Config.database.SessionLocal()
        try:
            yield db
        finally:
            db.close()
