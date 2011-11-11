import redis


class Storage(object):
    aliases = 'aliases:'
    emails = 'emails:'

    def __init__(self, **kw):
        self.redis = redis.Redis(**kw)

    def resolve_alias(self, alias):
        return self.redis.get(self.aliases + alias)

    def add_alias(self, email, alias):
        self.redis.set(self.aliases + alias, email)
        self.redis.rpush(self.emails + email, alias)
        return alias

    def get_aliases(self, email):
        return self.redis.lrange(self.emails + email, 0, -1)

    def delete_alias(self, email, alias):
        self.redis.delete(self.aliases + alias)
        self.redis.lrem(self.emails + email, alias)
