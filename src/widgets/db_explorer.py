from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Placeholder, Tree
from drivers.postgres import PostgresDriver


class VimTree(Tree):
    BINDINGS = [
        ("k", "cursor_up", "Up"),
        ("j", "cursor_down", "Down"),
        ("l", "select_cursor", "Select"),
    ]


class DbExplorer(Widget):
    BORDER_TITLE = "Database Explorer"

    def __init__(self, driver: PostgresDriver):
        super().__init__()
        self.driver = driver

    async def on_mount(self) -> None:
        tree = self.query_one(Tree)
        tables = await self.driver.list_tables("public")
        for table in tables:
            node = tree.root.add(table.name)
            for column in table.columns:
                node.add_leaf(f"{column.name}: {column.data_type}")

    def compose(self) -> ComposeResult:
        yield VimTree("Tables")
        # yield Placeholder("Database Tables & Schema")
