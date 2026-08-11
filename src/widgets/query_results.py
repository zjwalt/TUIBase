from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Placeholder


class QueryResults(Widget):
    BORDER_TITLE = "Query Results"

    def compose(self) -> ComposeResult:
        yield Placeholder("Query Results")
