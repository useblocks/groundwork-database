import os
from groundwork import App


def start_app():
    app = App([os.path.join(os.path.dirname(__file__), "configuration.py")])
    app.plugins.activate(["GwSqlPlugin", "GwPluginsInfo"])
    app.commands.start_cli()
