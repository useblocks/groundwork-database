from click.testing import CliRunner
from groundwork_database.plugins import GwDatabasePlugin


def test_plugin_init(basicApp):
    plugin = GwDatabasePlugin(basicApp)
    plugin.activate()

    plugins = basicApp.plugins.get()
    assert plugin.name in plugins.keys()


def test_plugin_list(basicApp):
    plugin = GwDatabasePlugin(basicApp)
    plugin.activate()

    runner = CliRunner()
    runner.invoke(basicApp.commands.get("database_list").click_command)
