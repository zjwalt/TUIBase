from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical
from widgets import DbExplorer, QueryEditor, QueryResults
from drivers.postgres import PostgresDriver
from drivers.base import ConnectionConfig


class TUIBase(App):
    CSS_PATH = "styles/TUIBase.tcss"

    BINDINGS = [
        ("q", "quit", "QUIT"),
    ]

    def compose(self) -> ComposeResult:
        config = ConnectionConfig(
            host="aws-1-us-east-1.pooler.supabase.com",
            port=6543,
            user="postgres.jfyphgxpdznacepykfkp",
            password="haR9rlsU7v1dJS5d",
            database="postgres",
        )
        yield Header()
        with Horizontal(id="main"):
            with Vertical(classes="column"):
                yield QueryEditor()
                yield QueryResults()
        yield Footer()

    async def on_mount(self) -> None:
        self.driver = PostgresDriver()
        config = ConnectionConfig(
            host="aws-1-us-east-1.pooler.supabase.com",
            port=6543,
            user="postgres.jfyphgxpdznacepykfkp",
            password="haR9rlsU7v1dJS5d",
            database="postgres",
        )
        await self.driver.connect(config)

        main = self.query_one("#main", Horizontal)
        await main.mount(DbExplorer(self.driver), before=0)


if __name__ == "__main__":
    app = TUIBase()
    app.run()
