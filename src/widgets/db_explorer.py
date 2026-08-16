from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Placeholder, Tree
from drivers.postgres import PostgresDriver


class DbExplorer(Widget):
    BORDER_TITLE = "Database Explorer"

    def __init__(self, driver: PostgresDriver):
        super().__init__()
        self.driver = driver

    def compose(self) -> ComposeResult:
        tree = Tree("Tables")
        node = tree.root.add("players")
        node.add_leaf("id: integer")

        yield tree
        # yield Placeholder("Database Tables & Schema")
