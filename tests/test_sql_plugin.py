from click.testing import CliRunner
from groundwork_sql.plugins import GwSqlPlugin


def test_plugin_init(basicApp):
    plugin = GwSqlPlugin(basicApp)
    plugin.activate()

    plugins = basicApp.plugins.get()
    assert plugin.name in plugins.keys()


def test_plugin_list(basicApp):
    plugin = GwSqlPlugin(basicApp)
    plugin.activate()

    runner = CliRunner()
    runner.invoke(basicApp.commands.get("database_list").click_command)
