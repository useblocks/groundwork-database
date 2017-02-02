import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from groundwork.patterns import GwBasePattern


class GwSqlPattern(GwBasePattern):
    """

    """

    def __init__(self, app, **kwargs):
        super(GwSqlPattern, self).__init__(app, **kwargs)
        if not hasattr(self.app, "databases"):
            self.app.databases = SqlDatabasesApplication(self.app)

        #: Instance of :class:`~.SqlDatabasesPlugin`.
        #: Provides functions to register and manage sql database interfaces
        self.databases = SqlDatabasesPlugin(self)


class SqlDatabasesPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

        # Let's register a receiver, which cares about the deactivation process of sql databases for this plugin.
        # We do it after the original plugin deactivation, so we can be sure that the registered function is the last
        # one which cares about sql databases for this plugin.
        self.plugin.signals.connect(receiver="%s_sql_deactivation" % self.plugin.name,
                                    signal="plugin_deactivate_post",
                                    function=self.__deactivate_sql_databases,
                                    description="Deactivates sql databases for %s" % self.plugin.name,
                                    sender=self.plugin)
        self.log.debug("Pattern sql databases initialised")

    def __deactivate_sql_databases(self, plugin, *args, **kwargs):
        databases = self.get()
        for databases in databases.keys():
            self.unregister(databases)

    def register(self, database, database_url, description):
        """
        Registers a new sql database for a plugin.
        """
        return self.app.databases.register(database, database_url, description, self.plugin)

    def unregister(self, database):
        """
        Unregisters an existing database, so that this database is no longer.
        This function is mainly used during plugin deactivation.
        """
        return self.app.databases.unregister(database)

    def get(self, name=None):
        """
        Returns databases, which can be filtered by name.

        :param name: name of the database
        :type name: str
        :return: None, single database or dict of databases
        """
        return self.app.databases.get(name, self.plugin)


class SqlDatabasesApplication:
    def __init__(self, app):
        self.app = app
        self.log = logging.getLogger(__name__)
        self._databases = {}
        self.log.info("Application sql databases initialised")

        self.app.signals.register("db_registered", self.app,
                                  "Fired if a new database was registered by a plugin. "
                                  "Provided arguments are: database and plugin")

        self.app.signals.register("db_class_registered", self.app,
                                  "Fired if a new database class was registered by a plugin "
                                  "Provided arguments are: database, db_class and plugin")

    def register(self, database, database_url, description, plugin=None):
        """
        Registers a new sql database for a plugin.
        """
        if database in self._databases.keys():
            raise DatabaseExistException("Database %s already registered by %s" % (
                database, self._databases[database].plugin.name))

        if plugin is None:
            new_database = Database(database, database_url, description, app=self.app)
        else:
            new_database = Database(database, database_url, description, plugin=plugin)

        self._databases[database] = new_database
        self.log.debug("Database registered: %s" % database)

        if plugin is not None:
            plugin.signals.send("db_registered", database=new_database)
        else:
            self.app.signals.send("db_registered", plugin=self.app, database=new_database)
        return new_database

    def unregister(self, database):
        """
        Unregisters an existing database, so that this database is no longer.
        This function is mainly used during plugin deactivation.
        """
        if database not in self._databases.keys():
            self.log.warning("Can not unregister database %s. Reason: Database does not exist." % database)
        else:
            del (self._databases[database])
            self.log.debug("Database %s git unregistered" % database)

    def get(self, name=None, plugin=None):
        """
        Returns databases, which can be filtered by name.

        :param name: name of the database
        :type name: str
        :return: None, single database or dict of databases
        """
        if plugin is not None:
            if name is None:
                database_list = {}
                for key in self._databases.keys():
                    if self._databases[key].plugin == plugin:
                        database_list[key] = self._databases[key]
                return database_list
            else:
                if name in self._databases.keys():
                    if self._databases[name].plugin == plugin:
                        return self._databases[name]
                    else:
                        return None
                else:
                    return None
        else:
            if name is None:
                return self._databases
            else:
                if name in self._databases.keys():
                    return self._databases[name]
                else:
                    return None


class Database:
    def __init__(self, name, url, description, plugin=None, app=None):
        self.name = name
        self.database_url = url
        self.description = description
        self.plugin = plugin
        self.app = app

        self.engine = create_engine(url)

        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=self.engine))
        self.Base = declarative_base()

        # This allows to perform Class.query (e.g. User.query), which is normally not
        # available on pure sqlalchemy models. But this kind of usage is provided by libs like flask-sqlalachemy,
        # what makes it very handy to query classes.
        # Fore more visit: http://stackoverflow.com/a/28025843
        self.Base.query = self.session.query_property()

        self.classes = DatabaseClass(self, self.plugin, self.app)

    def create_all(self):
        return self.Base.metadata.create_all(self.engine)

    def commit(self, *args, **kwargs):
        return self.session.commit(*args, **kwargs)

    def query(self, *args, **kwargs):
        return self.session.query(*args, **kwargs)

    def add(self, *args, **kwargs):
        return self.session.add(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.session.delete(*args, **kwargs)

    def rollback(self, *args, **kwargs):
        return self.session.rollback(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self.session.close(*args, **kwargs)


class DatabaseClass:
    def __init__(self, database, plugin=None, app=None):
        self.database = database
        self._Base = database.Base
        self.plugin = plugin
        self.app = app
        self._classes = {}

    def register(self, clazz, name=None):
        if name is None:
            name = clazz.__name__

        if name in self._classes.keys():
            raise DatabaseClassExistException("Database class %s already registered")

        # NOT LONGER USED
        # But implementation may be a solution for upcoming problems, so we keep the following comments.
        #
        # We need to "combine" the given user class with the Base class of our database.
        # Normally the user class inherits from this Base class.
        # But we need to do it dynamically and changing __bases__ of a class to add an inheritance does not work well.
        # Therefore we create a new class, which inherits from both (user class and Base class).
        # To not confusing developers during debug session, the new class gets the same name as the given user class.
        # TempClass = type(clazz.__name__, (self._Base, clazz), dict())
        # self._classes[name] = TempClass

        self._classes[name] = clazz
        if self.plugin is not None:
            self.plugin.signals.send("db_class_registered", database=self.database, db_class=clazz)
        else:
            self.app.signals.send("db_class_registered", database=self.database, db_class=clazz, plugin=self.app)

        return self._classes[name]

    def unregister(self, name):
        return self._classes.pop(name, None)

    def get(self, clazz_name=None):
        if clazz_name is None:
            return self._classes
        elif clazz_name in self._classes.keys():
            return self._classes[clazz_name]

        return None


class DatabaseExistException(BaseException):
    pass


class DatabaseClassExistException(BaseException):
    pass
