from src.cat.common.config.ApolloMgmt import ApolloMgmt
from src.cat.common.config.AzureMgmt import AzureMgmt
from src.cat.common.config.DeepSeekMgmt import DeepSeekMgmt
from src.cat.common.config.LoggerMgmt import LoggerMgmt


class Config(object):
    apollo = ApolloMgmt()
    logger = LoggerMgmt()
    database = None  # PostgreSQLMgmt()
    deepseek = DeepSeekMgmt()
    azure = AzureMgmt()

    @staticmethod
    def get_db():
        db = Config.database.SessionLocal()
        try:
            yield db
        finally:
            db.close()
