from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.cat.common.config.ApolloMgmt import ApolloMgmt


class PostgreSQLMgmt:
    # 从环境变量中获取数据库连接信息
    DB_USER = ApolloMgmt.get_property('database.postgresql.user', 'user')
    DB_PASSWORD = ApolloMgmt.get_property('database.postgresql.password', 'password')
    DB_HOST = ApolloMgmt.get_property('database.postgresql.host', 'host')
    DB_PORT = ApolloMgmt.get_property('database.postgresql.port', 'port')
    DB_NAME = ApolloMgmt.get_property('database.postgresql.name', 'name')
    DB_SCHEMA = ApolloMgmt.get_property('database.postgresql.schema', 'schema')
    # 构建数据库连接字符串
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    CONNECT_ARGS = {"options": f"-csearch_path={DB_SCHEMA}"}

    def __init__(self):
        # 创建数据库引擎，设置连接池参数
        self.engine = create_engine(
            self.DATABASE_URL,
            pool_size=5,  # 连接池的初始大小
            max_overflow=100,  # 连接池允许的最大连接数
            pool_timeout=30,  # 连接池超时时间
            pool_recycle=3600,  # 连接池中的连接多久后会被回收
            connect_args=self.CONNECT_ARGS
        )
        # 创建会话工厂
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
