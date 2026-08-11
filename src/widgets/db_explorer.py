from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Placeholder


class DbExplorer(Widget):
    BORDER_TITLE = "Database Explorer"

    def compose(self) -> ComposeResult:
        yield Placeholder("Database Tables & Schema")
