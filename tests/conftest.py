import pytest


@pytest.fixture
def basicApp():
    """
    Loads a basic groundwork application and returns it.
    :return: app
    """
    from groundwork import App
    from tests.test_plugins import EmptyDatabasePlugin

    app = App(plugins=[EmptyDatabasePlugin], strict=True)
    app.plugins.activate(["EmptyDatabasePlugin"])
    return app


@pytest.fixture
def EmptyDatabasePlugin():
    from tests.test_plugins.empty_database_plugin import EmptyDatabasePlugin
    return EmptyDatabasePlugin


@pytest.fixture
def DatabasePlugin():
    from tests.test_plugins.database_plugin import DatabasePlugin
    return DatabasePlugin
