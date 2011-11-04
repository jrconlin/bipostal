import redis


class Storage(object):

    def __init__(self, **kw):
        self.redis = redis.Redis(**kw)

    def resolve_alias(self, alias):
        return self.redis.get(alias)

    def add_alias(self, email, alias):
        self.redis.set(alias, email)
        self.redis.rpush(email, alias)
        return alias

    def get_aliases(self, email):
        return self.redis.lrange(email, 0, -1)

    def delete_alias(self, email, alias):
        self.redis.delete(alias)
        self.redis.lrem(email, alias)
