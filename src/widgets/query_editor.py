from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Placeholder, TextArea

TEXT = """\
SELECT * FROM players;
"""


class QueryEditor(Widget):
    BORDER_TITLE = "Query Editor"

    def compose(self) -> ComposeResult:
        yield TextArea.code_editor(TEXT, language="sql")
        # yield Placeholder("Query Editor")
