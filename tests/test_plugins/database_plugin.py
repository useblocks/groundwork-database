from groundwork_database.patterns import GwSqlPattern


class DatabasePlugin(GwSqlPattern):
    def __init__(self, app, name=None, *args, **kwargs):
        self.name = name or self.__class__.__name__
        super(DatabasePlugin, self).__init__(app, *args, **kwargs)

    def activate(self):
        self.databases.register("my_db", "sqlite:///:memory:", "test_database")

    def deactivate(self):
        pass
