from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable, Label


class QueryResults(Widget):
    BORDER_TITLE = "Query Results"

    def show_error(self, message: str):
        self.mount(Label(message))
