from groundwork.patterns import GwCommandsPattern


class GwDatabasePlugin(GwCommandsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super(GwDatabasePlugin, self).__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("database_list", "List all databases", self._list_db)

    def _list_db(self):
        print("Registered databases")
        databases = self.app.databases.get()
        for key, db in databases.items():
            print("  %s\n  %s\n  %s\n" % (db.name, db.description, db.database_url))
