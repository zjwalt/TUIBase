from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable, Label


class QueryResults(Widget):
    BORDER_TITLE = "Query Results"

    def compose(self) -> ComposeResult:
        yield DataTable()

    def show_error(self, message: str):
        self.mount(Label(message))

    def show_results(self, columns, values):
        table = self.query_one(DataTable)
        table.add_columns(*columns)
        table.add_rows(values)
