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

To use groundwork-sql inside a groundwork plugin, simply integrated it as followed::

    from groundwork import App
    from groundwork_sql.patterns import GwSql

    class MyPlugin(GwSql):
        def _init_(self, *args, **kwargs):
            self.name = "My Plugin"
            super().__init__(*args, **kwargs)

        def activate(self):
            self.db.models.register(MyModel)


    if __name__ == "__main__":
        my_app = App(plugins=[MyPlugin])
        my_app.plugins.activate(["My Plugin"])

