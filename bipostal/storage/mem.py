class Storage(object):

    def __init__(self, **kw):
        self.db = {}

    def resolve_alias(self, alias):
        return self.db.get(alias)

    def add_alias(self, email, alias):
        self.db[alias] = email
        self.db.setdefault(email, []).append(alias)
        return alias

    def get_aliases(self, email):
        return self.db.get(email, [])

    def delete_alias(self, email, alias):
        if alias in self.db:
            del self.db[alias]
            self.db[email].remove(alias)
