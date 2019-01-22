from sqlalchemy import Column, Integer, String
from groundwork_database.patterns import GwSqlPattern


def test_plugin_init(basicApp):
    plugins = basicApp.plugins.get()
    assert "EmptyDatabasePlugin" in plugins.keys()


def test_plugin_db_init(basicApp, DatabasePlugin):
    basicApp.plugins.classes.register([DatabasePlugin])
    basicApp.plugins.activate(["DatabasePlugin"])

    db = basicApp.databases.get("my_db")
    assert db is not None

    plugin = basicApp.plugins.get("DatabasePlugin")
    db2 = plugin.databases.get("my_db")
    assert db2 is not None

    assert db.session is not None
    assert db.engine is not None
    assert db.Base is not None


def test_plugin_db_registration(basicApp):
    class MyPlugin(GwSqlPattern):
        def __init__(self, app, name=None, *args, **kwargs):
            self.name = name or self.__class__.__name__
            super(MyPlugin, self).__init__(app, *args, **kwargs)

        def activate(self):
            self.databases.register("my_test_db", "sqlite:///:memory:", "my_test_database")

        def deactivate(self):
            pass

    plugin = MyPlugin(basicApp)
    plugin.activate()
    databases = plugin.databases.get()
    assert len(databases) == 1

    plugin.databases.unregister("my_test_db")
    databases = plugin.databases.get()
    assert len(databases) == 0


def test_plugin_db_activation(basicApp):
    class MyPlugin(GwSqlPattern):
        def __init__(self, app, name=None, *args, **kwargs):
            self.name = name or self.__class__.__name__
            super(MyPlugin, self).__init__(app, *args, **kwargs)

        def activate(self):
            pass

        def deactivate(self):
            pass

    plugin = MyPlugin(basicApp)
    plugin.activate()

    plugin.databases.register("my_test_db", "sqlite:///:memory:", "my_test_database")
    databases = basicApp.databases.get()
    assert len(databases) == 1

    plugin.deactivate()
    databases = basicApp.databases.get()
    assert len(databases) == 0


def test_plugin_db_session(basicApp, DatabasePlugin):
    basicApp.plugins.classes.register([DatabasePlugin])
    basicApp.plugins.activate(["DatabasePlugin"])
    plugin = basicApp.plugins.get("DatabasePlugin")
    db = plugin.databases.get("my_db")
    session = db.session
    session.autoflush = True

    User = _create_user_class(db.Base)
    db.create_all()

    user = User(name="test", fullname="Test Test", password="password")

    found_users = db.query(User).filter_by(name="test").first()
    assert found_users is None

    session.add(user)
    found_users = session.query(User).filter_by(name="test").first()
    assert user is found_users

    session.commit()
    found_users2 = session.query(User).filter_by(name="test").first()
    assert user is found_users2

    session.delete(user)
    session.commit()
    found_users2 = session.query(User).filter_by(name="test").first()
    assert found_users2 is None

    user2 = User(name="test2", fullname="Test Test", password="password")
    session.add(user2)
    found_users2 = session.query(User).filter_by(name="test2").first()
    assert user2 is found_users2
    session.rollback()
    found_users2 = session.query(User).filter_by(name="test2").first()
    assert found_users2 is None

    session.close()


def _create_user_class(Base):
    class User(Base):
        """
        User database model
        
        Stores all user related data
        
        :param id: Unique id of user. Used internally only.
        :type id: Integer, primary_key
        
        :param name: user name of the user
        :type name: String
        
        :param fullname: Fullname of the user
        :type fullname: String
        
        :param password: Password of the user. Encrypted via xy.
        :type password: String
        
        :return: Nothing to return
        :rtype: None-Type
        """
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        fullname = Column(String)
        password = Column(String)
        no_docstring = Column(String)

    return User


def test_plugin_class_registration(basicApp, DatabasePlugin):
    basicApp.plugins.classes.register([DatabasePlugin])
    basicApp.plugins.activate(["DatabasePlugin"])
    plugin = basicApp.plugins.get("DatabasePlugin")
    db = plugin.databases.get("my_db")
    session = db.session
    session.autoflush = True
    User = _create_user_class(db.Base)

    assert hasattr(db, "classes") is True
    db.classes.register(User)
    assert User == db.classes.get("User").clazz
    db.create_all()

    user = User(name="test", fullname="Test Test", password="password")
    session.add(user)
    found_users = session.query(User).filter_by(name="test").first()
    assert found_users is not None


class User(object):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
