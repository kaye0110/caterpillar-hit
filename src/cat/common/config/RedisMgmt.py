from redis import ConnectionPool, Redis

from src.cat.common.config.ApolloMgmt import ApolloMgmt


class RedisMgmt:
    # 从环境变量中获取 Redis 连接信息
    REDIS_HOST = ApolloMgmt.get_property('redis.host', 'localhost')
    REDIS_PORT = int(ApolloMgmt.get_property('redis.port', 6379))
    REDIS_DB = int(ApolloMgmt.get_property('redis.db', 0))
    REDIS_PASSWORD = ApolloMgmt.get_property('redis.password', None)

    # 创建全局 Redis 连接池
    REDIS_POOL = ConnectionPool(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD
    )

    # 创建全局 Redis 连接
    REDIS_CLIENT = Redis(connection_pool=REDIS_POOL)


class RedisLock:
    def __init__(self, lock_name, expire=10):
        self.redis_client = RedisMgmt.REDIS_CLIENT
        self.lock_name = lock_name
        self.expire = expire

    def acquire(self):
        """
        Try to acquire the lock
        """
        return self.redis_client.set(self.lock_name, "locked", nx=True, ex=self.expire)

    def release(self):
        """
        Release the lock
        """
        self.redis_client.delete(self.lock_name)
