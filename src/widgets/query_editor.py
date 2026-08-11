from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Placeholder


class QueryEditor(Widget):
    BORDER_TITLE = "Query Editor"

    def compose(self) -> ComposeResult:
        yield Placeholder("Query Editor")
