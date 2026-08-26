from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Placeholder, TextArea
from textual.reactive import reactive
from textual import events
from enum import Enum, auto
import time

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
        "o": "insert_new_line_below",
        "O": "insert_new_line_above",
    }

    INSERT_BINDINGS = {"jk": "enter_normal", "escape": "enter_normal"}

    JK_TIMEOUT = 0.25

    mode: reactive[Mode] = reactive(Mode.NORMAL)

    def __init__(self) -> None:
        super().__init__(TEXT, language="sql", theme="dracula")
        self._last_key: str | None = None
        self._last_key_time: float = 0.0

    def enter_insert(self):
        self.mode = Mode.INSERT

    def enter_normal(self):
        self.mode = Mode.NORMAL

    def insert_new_line_below(self):
        while not self.cursor_at_end_of_line:
            self.cursor_right()
        self.enter_insert()
        self.insert("\n")

    def insert_new_line_above(self):
        while not self.cursor_at_start_of_line:
            self.cursor_left()
        self.enter_insert()
        self.insert("\n")
        self.cursor_up()

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

        elif self.mode == Mode.INSERT:
            now = time.monotonic()

            if (
                event.key == "k"
                and self._last_key == "j"
                and (now - self._last_key_time) <= self.JK_TIMEOUT
            ):
                row, col = self.cursor_location
                self.delete((row, col - 1), (row, col))
                self.mode = Mode.NORMAL
                event.prevent_default()
                event.stop()
            else:
                self._last_key = event.key
                self._last_key_time = now

    def watch_mode(self, mode: Mode) -> None:
        self.border_subtitle = f"-- {mode.name} --"
