from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable, Label
from textual import events


class QueryResults(Widget):
    BORDER_TITLE = "Query Results"

    VIM_BINDINGS = {
        "h": "cursor_left",
        "j": "cursor_down",
        "k": "cursor_up",
        "l": "cursor_right",
    }

    def __init__(self):
        super().__init__()
        self.table = None

    def cursor_left(self):
        current_column = self.table.cursor_column
        self.table.move_cursor(column=current_column - 1)

    def cursor_down(self):
        current_row = self.table.cursor_row
        self.table.move_cursor(row=current_row + 1)

    def cursor_up(self):
        current_row = self.table.cursor_row
        self.table.move_cursor(row=current_row - 1)

    def cursor_right(self):
        current_column = self.table.cursor_column
        self.table.move_cursor(column=current_column + 1)

    def compose(self) -> ComposeResult:
        yield DataTable()

    def show_error(self, message: str):
        self.mount(Label(message))

    def show_results(self, columns, values):
        self.table = self.query_one(DataTable)
        self.table.clear(columns=True)
        self.table.add_columns(*columns)
        self.table.add_rows(values)

    def _on_key(self, event: events.Key):
        action_name = self.VIM_BINDINGS.get(event.key)
        if action_name is not None:
            method = getattr(self, action_name)
            method()
