from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical
from widgets import DbExplorer, QueryEditor, QueryResults
from drivers.postgres import PostgresDriver


class TUIBase(App):
    CSS_PATH = "styles/TUIBase.tcss"

    BINDINGS = [
        ("q", "quit", "QUIT"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield DbExplorer(PostgresDriver())
            with Vertical(classes="column"):
                yield QueryEditor()
                yield QueryResults()
        yield Footer()


if __name__ == "__main__":
    app = TUIBase()
    app.run()
