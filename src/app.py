from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical
from widgets import DbExplorer, QueryEditor, QueryResults
from drivers.postgres import PostgresDriver
from drivers.base import ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()


class TUIBase(App):
    CSS_PATH = "styles/TUIBase.tcss"

    BINDINGS = [
        ("q", "quit", "QUIT"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main"):
            with Vertical(classes="column"):
                yield QueryEditor()
                yield QueryResults()
        yield Footer()

    async def on_mount(self) -> None:
        self.driver = PostgresDriver()
        config = ConnectionConfig(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
        )
        await self.driver.connect(config)

        main = self.query_one("#main", Horizontal)
        await main.mount(DbExplorer(self.driver), before=0)

    async def on_query_editor_submitted(self, message: QueryEditor.Submitted) -> None:
        sql = message.sql

        try:
            results = await self.driver.execute_query(sql)
            self.log("RESULTS:\n", results)
        except Exception as ex:
            results_pane = self.query_one(QueryResults)
            results_pane.show_error(str(ex))


if __name__ == "__main__":
    app = TUIBase()
    app.run()
