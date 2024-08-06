from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widget import Widget
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Pretty,
    Select,
    Static,
    Switch,
    TabbedContent,
    TextArea,
    Tree,
)

from data_fox.consts import HTTP_METHODS


class ActivableField(Static):
    DEFAULT_CSS = """
    ActivableField {
        layout: grid;
        grid-size: 3 1;
        grid-columns: 0.8fr 2fr 3fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Switch(value=False, tooltip='Send this field?')
        yield Input(placeholder='Key', classes='w-full')
        yield Input(placeholder='Value', classes='w-full')
        # yield Input(placeholder='Description')


class ActivableHeader(ActivableField):
    pass


class ActivableQueryParam(ActivableField):
    pass


class URLArea(Widget):
    BORDER_TITLE = 'URL'
    DEFAULT_CSS = """
    URLArea {
        layout: grid;
        grid-size: 3 1;
        grid-columns: 1fr 6fr 1fr;
        border: heavy black;
    }
    """

    def compose(self) -> ComposeResult:
        yield Select.from_values(values=HTTP_METHODS, allow_blank=False)
        yield Input(placeholder='Enter URL')
        yield Button(label='Make request')


class RequestArea(Widget):
    BORDER_TITLE = 'Request'
    DEFAULT_CSS = """
    RequestArea {
        border: heavy black;
    }
    """

    def compose(self) -> ComposeResult:
        with TabbedContent('Headers', 'Query params', 'Body'):
            yield ActivableHeader()
            yield ActivableQueryParam()
            with Container():
                yield Select.from_values(('JSON', 'File'), allow_blank=False)
                yield TextArea.code_editor(language='json')

    @on(Select.Changed)
    def ae(self) -> None:
        self.app.bell()


class ResponseArea(Widget):
    BORDER_TITLE = 'Response'
    DEFAULT_CSS = """
    ResponseArea {
        border: heavy black;
    }
    """

    def compose(self) -> ComposeResult:
        with TabbedContent('Headers', 'Body'):
            yield Button('h')
            yield Pretty({})


class CollectionsArea(Widget):
    BORDER_TITLE = 'Collections'
    DEFAULT_CSS = """
    CollectionsArea {
        border: heavy black;
        overflow-y: auto;
        overflow-x: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield Tree(label='')


class DataFoxApp(App):
    TITLE = 'DataFox'
    SUB_TITLE = (
        'A minimalist API client with the cunning simplicity of a fox 🦊'
    )
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = 'style.tcss'
    DEFAULT_CSS = """
    CollectionsArea {
        width: 16%;
    }

    #MainContent {
        layout: grid;
        grid-size: 2 2;
        grid-columns: 1fr 1fr;
        grid-rows: 0.8fr 5fr;
    }

    URLArea {
        column-span: 2;
    }

    """
    BINDINGS = [
        ('ctrl+b', 'toggle_collections_area', 'Show/Hide collections'),
        ('ctrl+t', 'toggle_dark_mode', 'Toggle dark mode'),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal():
            yield CollectionsArea()
            with Container(id='MainContent'):
                yield URLArea()
                yield RequestArea()
                yield ResponseArea()

        yield Footer()

    def action_toggle_collections_area(self) -> None:
        self.query_one(CollectionsArea).toggle_class('hidden')

    def action_toggle_dark_mode(self) -> None:
        self.dark = not self.dark
