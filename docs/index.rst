.. image:: https://img.shields.io/pypi/l/groundwork-sql.svg
   :target: https://pypi.python.org/pypi/groundwork-sql
   :alt: License
.. image:: https://img.shields.io/pypi/pyversions/groundwork-sql.svg
   :target: https://pypi.python.org/pypi/groundwork-sql
   :alt: Supported versions
.. image:: https://readthedocs.org/projects/groundwork-sql/badge/?version=latest
   :target: https://readthedocs.org/projects/groundwork-sql/
.. image:: https://travis-ci.org/useblocks/groundwork-sql.svg?branch=master
   :target: https://travis-ci.org/useblocks/groundwork-sql
   :alt: Travis-CI Build Status
.. image:: https://coveralls.io/repos/github/useblocks/groundwork-sql/badge.svg?branch=master
   :target: https://coveralls.io/github/useblocks/groundwork-sql?branch=master
.. image:: https://img.shields.io/scrutinizer/g/useblocks/groundwork-sql.svg
   :target: https://scrutinizer-ci.com/g/useblocks/groundwork-sql/
   :alt: Code quality
.. image:: https://img.shields.io/pypi/v/groundwork-sql.svg
   :target: https://pypi.python.org/pypi/groundwork-sql
   :alt: PyPI Package latest release



.. _groundwork: https://groundwork.readthedocs.io

Welcome to groundwork-sql
=========================

groundwork-sql is a plugin for the application framework `groundwork`_.

It provides a pattern for sql database support and a small console plugin to inspect those databases.

The main features are:

 * Support of multiple database connections
 * Support of various SQL based database like:

  * `PostgresSQL <https://www.postgresql.org/>`_
  * `sqlite <https://www.sqlite.org/>`_
  * `MySQL <https://www.mysql.de/>`_
  * `MariaDB <https://mariadb.org/>`_
  * and all other databases, which are supported by `SQLAlchemy <http://www.sqlalchemy.org/>`_

.. note::

    groundwork-sql is based on `SQLAlchemy <http://www.sqlalchemy.org/>`_. All functions from SQLAlchemy are
    available inside groundwork plugins, which are using groundwork-sql as pattern.

Quickstart
==========

To use groundwork-sql inside a groundwork plugin, simply integrate it as followed::

    from groundwork import App
    from groundwork_sql.patterns import GwSqlPattern

    class MyPlugin(GwSqlPattern):
        def _init_(self, app, *args, **kwargs):
            self.name = "My Plugin"
            super().__init__(app, *args, **kwargs)

        def activate(self):
            name = "my_db"
            database_url = "sqlite:///:memory:"
            description = "My personal test database"
            db = self.databases.register(name, database_url, description)

            User = _get_user_class(db.Base)
            my_user = User(name="Me")
            db.add(my_user)
            db.commit()

        def print_user(name):
            db = self.databases.get("my_db")
            user = db.query(User).filter_by(name=name).first()
            if user is not None:
                print(user.name)
            else:
                print("User %s not found." % name)

        def _get_user_class(base):
            class User(base):
                id = Column(Integer, primary_key=True)
                name = Column(String)
            return User


    if __name__ == "__main__":
        my_app = App()
        my_plugin = MyPlugin(my_app)
        my_plugin.activate()
        my_plugin.print_user("me")

