from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Placeholder, TextArea
from textual.reactive import reactive
from textual import events
from enum import Enum, auto

TEXT = ""


class Mode(Enum):
    NORMAL = auto()
    INSERT = auto()
    VISUAL = auto()
    VISUAL_LINE = auto()


class QueryEditor(TextArea):
    BORDER_TITLE = "Query Editor"

    NORMAL_BINDINGS = {
        "h": "cursor_left",
        "j": "cursor_down",
        "k": "cursor_up",
        "l": "cursor_right",
        "i": "enter_insert",
    }

    INSERT_BINDINGS = {"jk": "enter_normal", "escape": "enter_normal"}

    mode: reactive[Mode] = reactive(Mode.NORMAL)

    def __init__(self) -> None:
        super().__init__(TEXT, language="sql")

    def enter_insert(self):
        self.mode = Mode.INSERT

    def enter_normal(self):
        self.mode = Mode.NORMAL

    def cursor_left(self):
        self.move_cursor(self.get_cursor_left_location())

    def cursor_down(self):
        self.move_cursor(self.get_cursor_down_location())

    def cursor_up(self):
        self.move_cursor(self.get_cursor_up_location())

    def cursor_right(self):
        self.move_cursor(self.get_cursor_right_location())

    def _on_key(self, event: events.Key) -> None:
        if self.mode == Mode.NORMAL:
            action_name = self.NORMAL_BINDINGS.get(event.key)
            if action_name is not None:
                method = getattr(self, action_name)
                method()
            event.prevent_default()
            event.stop()

        if self.mode == Mode.INSERT:
            action_name = self.INSERT_BINDINGS.get(event.key)
            if action_name is not None:
                method = getattr(self, action_name)
                method()

    def watch_mode(self, mode: Mode) -> None:
        self.border_subtitle = f"-- {mode.name} --"
