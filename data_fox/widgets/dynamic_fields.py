from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.message import Message
from textual.widgets import Button, Input, Static, Switch


class DynamicField(Static):
    """
    Enableable and removable field
    """

    DEFAULT_CSS = """
    DynamicField {
        layout: grid;
        grid-size: 4 1;
        grid-columns: auto 1fr 2fr auto; /* Set 1:2 ratio between Inputs */
    }
    """

    class Enabled(Message):
        """
        Sent when the user enables the field.
        """

        def __init__(self, field_enabled: 'DynamicField') -> None:
            super().__init__()
            self.field_enabled = field_enabled

    class Disabled(Message):
        """
        Sent when the user disables the field.
        """

        def __init__(self, field_disabled: 'DynamicField') -> None:
            super().__init__()
            self.field_disabled = field_disabled

    class RemoveRequested(Message):
        """
        Sent when the user clicks the remove button.
        The listener of this event decides whether to actually remove the field or not.
        """

        def __init__(self, field_to_remove: 'DynamicField') -> None:
            super().__init__()
            self.field_to_remove = field_to_remove

    def compose(self) -> ComposeResult:
        yield Switch(value=False, tooltip='Send this field?')
        yield Input(placeholder='Key', id='input-key')
        yield Input(placeholder='Value', id='input-value')
        yield Button(label='➖', tooltip='Remove field')

    def on_mount(self) -> None:
        self._switch_enable: Switch = self.query_one(Switch)
        self._input_key: Input = self.query_one('#input-key')
        self._input_value: Input = self.query_one('#input-value')
        self._button_remove: Button = self.query_one(Button)

    @property
    def enabled(self) -> bool:
        return self._switch_enable.value

    @property
    def key(self) -> str:
        return self._input_key.value

    @property
    def value(self) -> str:
        return self._input_value.value

    @on(Switch.Changed)
    def enabled_or_disabled(self, message: Switch.Changed) -> None:
        if message.value is True:
            self.post_message(self.Enabled(field_enabled=self))
        elif message.value is False:
            self.post_message(message=self.Disabled(field_disabled=self))
        message.stop()

    @on(Button.Pressed)
    def remove_requested(self, message: Button.Pressed) -> None:
        self.post_message(self.RemoveRequested(field_to_remove=self))
        message.stop()


class DynamicFields(Static):
    """
    Enableable and removable fields
    """

    def __init__(self, fields_count: int = 1, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields_count = fields_count

    def compose(self) -> ComposeResult:
        yield VerticalScroll()
        yield Button(label='➕', tooltip='Add field', classes='w-full')

    async def on_mount(self) -> None:
        self._container_fields = self.query_one(VerticalScroll)
        self._button_add_field = self.query_one(Button)

        await self.add_initial_fields()

    @property
    def fields(self) -> list[DynamicField]:
        return list(self.query(DynamicField))

    @property
    def values(self) -> list[dict[str, str | bool]]:
        return [
            {
                'enabled': field.enabled,
                'key': field.key,
                'value': field.value,
            }
            for field in self.fields
        ]

    @on(Button.Pressed)
    async def add_field_requested(self, message: Button.Pressed) -> None:
        await self.add_field()
        message.stop()

    @on(DynamicField.RemoveRequested)
    async def remove_field_requested(
        self, message: DynamicField.RemoveRequested
    ) -> None:
        await self.remove_field(field=message.field_to_remove)
        message.stop()

    async def add_initial_fields(self) -> None:
        for _ in range(self.fields_count):
            await self.add_field()

    async def add_field(self) -> None:
        await self._container_fields.mount(DynamicField())

    async def remove_field(self, field: DynamicField) -> None:
        if len(self.fields) == 1:
            self.app.bell()
            return

        field.add_class('hidden')
        self.fields[self.fields.index(field) - 1]._button_remove.focus()
        await field.remove()
