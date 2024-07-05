import wx
from amulet_map_editor.api.wx.ui.simple import (
    SimpleDialog,
    SimpleScrollablePanel,
    SimpleChoice,
)
from typing import Dict, Tuple, Optional, Union, Sequence

from amulet_map_editor.api.image import ADD_ICON, SUBTRACT_ICON, EDIT_ICON

ModifierKeyType = str
KeyType = Union[int, str]
KeybindGroupIdType = str
KeyActionType = str
ModifierType = Tuple[ModifierKeyType, ...]
SerialisedKeyType = Tuple[ModifierType, KeyType]
KeybindGroup = Dict[KeyActionType, SerialisedKeyType]
ActionLookupType = Dict[SerialisedKeyType, KeyActionType]
KeybindContainer = Dict[KeybindGroupIdType, KeybindGroup]

MouseLeft = "MOUSE_LEFT"
MouseMiddle = "MOUSE_MIDDLE"
MouseRight = "MOUSE_RIGHT"
MouseAux1 = "MOUSE_AUX_1"
MouseAux2 = "MOUSE_AUX_2"
MouseWheelScrollUp = "MOUSE_WHEEL_SCROLL_UP"
MouseWheelScrollDown = "MOUSE_WHEEL_SCROLL_DOWN"
Control = "CTRL"
Shift = "SHIFT"
Alt = "ALT"

Space = "SPACE"
PageUp = "PAGE_UP"
PageDown = "PAGE_DOWN"
Back = "BACK"
Tab = "TAB"
Return = "RETURN"
Escape = "ESCAPE"
Delete = "DELETE"
Start = "START"
Menu = "MENU"
Pause = "PAUSE"
Capital = "CAPITAL"
End = "END"
Home = "HOME"
Left = "LEFT"
Up = "UP"
Right = "RIGHT"
Down = "DOWN"
Select = "SELECT"
Print = "PRINT"
Execute = "EXECUTE"
Snapshot = "SNAPSHOT"
Insert = "INSERT"
Help = "HELP"
Numpad0 = "NUMPAD0"
Numpad1 = "NUMPAD1"
Numpad2 = "NUMPAD2"
Numpad3 = "NUMPAD3"
Numpad4 = "NUMPAD4"
Numpad5 = "NUMPAD5"
Numpad6 = "NUMPAD6"
Numpad7 = "NUMPAD7"
Numpad8 = "NUMPAD8"
Numpad9 = "NUMPAD9"
Multiply = "MULTIPLY"
Add = "ADD"
Separator = "SEPARATOR"
Subtract = "SUBTRACT"
Decimal = "DECIMAL"
Divide = "DIVIDE"
F1 = "F1"
F2 = "F2"
F3 = "F3"
F4 = "F4"
F5 = "F5"
F6 = "F6"
F7 = "F7"
F8 = "F8"
F9 = "F9"
F10 = "F10"
F11 = "F11"
F12 = "F12"
F13 = "F13"
F14 = "F14"
F15 = "F15"
F16 = "F16"
F17 = "F17"
F18 = "F18"
F19 = "F19"
F20 = "F20"
F21 = "F21"
F22 = "F22"
F23 = "F23"
F24 = "F24"
Numlock = "NUMLOCK"
Scroll = "SCROLL"
Numpad_Space = "NUMPAD_SPACE"
Numpad_Tab = "NUMPAD_TAB"
Numpad_Enter = "NUMPAD_ENTER"
Numpad_F1 = "NUMPAD_F1"
Numpad_F2 = "NUMPAD_F2"
Numpad_F3 = "NUMPAD_F3"
Numpad_F4 = "NUMPAD_F4"
Numpad_Home = "NUMPAD_HOME"
Numpad_Left = "NUMPAD_LEFT"
Numpad_Up = "NUMPAD_UP"
Numpad_Right = "NUMPAD_RIGHT"
Numpad_Down = "NUMPAD_DOWN"
Numpad_Pageup = "NUMPAD_PAGEUP"
Numpad_Pagedown = "NUMPAD_PAGEDOWN"
Numpad_End = "NUMPAD_END"
Numpad_Begin = "NUMPAD_BEGIN"
Numpad_Insert = "NUMPAD_INSERT"
Numpad_Delete = "NUMPAD_DELETE"
Numpad_Equal = "NUMPAD_EQUAL"
Numpad_Multiply = "NUMPAD_MULTIPLY"
Numpad_Add = "NUMPAD_ADD"
Numpad_Separator = "NUMPAD_SEPARATOR"
Numpad_Subtract = "NUMPAD_SUBTRACT"
Numpad_Decimal = "NUMPAD_DECIMAL"
Numpad_Divide = "NUMPAD_DIVIDE"

key_string_map = {
    wx.WXK_CONTROL: Control,
    wx.WXK_SHIFT: Shift,
    wx.WXK_ALT: Alt,
    wx.WXK_SPACE: Space,
    wx.WXK_PAGEUP: PageUp,
    wx.WXK_PAGEDOWN: PageDown,
    wx.WXK_BACK: Back,
    wx.WXK_TAB: Tab,
    wx.WXK_RETURN: Return,
    wx.WXK_ESCAPE: Escape,
    wx.WXK_DELETE: Delete,
    wx.WXK_START: Start,
    wx.WXK_MENU: Menu,
    wx.WXK_PAUSE: Pause,
    wx.WXK_CAPITAL: Capital,
    wx.WXK_END: End,
    wx.WXK_HOME: Home,
    wx.WXK_LEFT: Left,
    wx.WXK_UP: Up,
    wx.WXK_RIGHT: Right,
    wx.WXK_DOWN: Down,
    wx.WXK_SELECT: Select,
    wx.WXK_PRINT: Print,
    wx.WXK_EXECUTE: Execute,
    wx.WXK_SNAPSHOT: Snapshot,
    wx.WXK_INSERT: Insert,
    wx.WXK_HELP: Help,
    wx.WXK_NUMPAD0: Numpad0,
    wx.WXK_NUMPAD1: Numpad1,
    wx.WXK_NUMPAD2: Numpad2,
    wx.WXK_NUMPAD3: Numpad3,
    wx.WXK_NUMPAD4: Numpad4,
    wx.WXK_NUMPAD5: Numpad5,
    wx.WXK_NUMPAD6: Numpad6,
    wx.WXK_NUMPAD7: Numpad7,
    wx.WXK_NUMPAD8: Numpad8,
    wx.WXK_NUMPAD9: Numpad9,
    wx.WXK_MULTIPLY: Multiply,
    wx.WXK_ADD: Add,
    wx.WXK_SEPARATOR: Separator,
    wx.WXK_SUBTRACT: Subtract,
    wx.WXK_DECIMAL: Decimal,
    wx.WXK_DIVIDE: Divide,
    wx.WXK_F1: F1,
    wx.WXK_F2: F2,
    wx.WXK_F3: F3,
    wx.WXK_F4: F4,
    wx.WXK_F5: F5,
    wx.WXK_F6: F6,
    wx.WXK_F7: F7,
    wx.WXK_F8: F8,
    wx.WXK_F9: F9,
    wx.WXK_F10: F10,
    wx.WXK_F11: F11,
    wx.WXK_F12: F12,
    wx.WXK_F13: F13,
    wx.WXK_F14: F14,
    wx.WXK_F15: F15,
    wx.WXK_F16: F16,
    wx.WXK_F17: F17,
    wx.WXK_F18: F18,
    wx.WXK_F19: F19,
    wx.WXK_F20: F20,
    wx.WXK_F21: F21,
    wx.WXK_F22: F22,
    wx.WXK_F23: F23,
    wx.WXK_F24: F24,
    wx.WXK_NUMLOCK: Numlock,
    wx.WXK_SCROLL: Scroll,
    wx.WXK_NUMPAD_SPACE: Numpad_Space,
    wx.WXK_NUMPAD_TAB: Numpad_Tab,
    wx.WXK_NUMPAD_ENTER: Numpad_Enter,
    wx.WXK_NUMPAD_F1: Numpad_F1,
    wx.WXK_NUMPAD_F2: Numpad_F2,
    wx.WXK_NUMPAD_F3: Numpad_F3,
    wx.WXK_NUMPAD_F4: Numpad_F4,
    wx.WXK_NUMPAD_HOME: Numpad_Home,
    wx.WXK_NUMPAD_LEFT: Numpad_Left,
    wx.WXK_NUMPAD_UP: Numpad_Up,
    wx.WXK_NUMPAD_RIGHT: Numpad_Right,
    wx.WXK_NUMPAD_DOWN: Numpad_Down,
    wx.WXK_NUMPAD_PAGEUP: Numpad_Pageup,
    wx.WXK_NUMPAD_PAGEDOWN: Numpad_Pagedown,
    wx.WXK_NUMPAD_END: Numpad_End,
    wx.WXK_NUMPAD_BEGIN: Numpad_Begin,
    wx.WXK_NUMPAD_INSERT: Numpad_Insert,
    wx.WXK_NUMPAD_DELETE: Numpad_Delete,
    wx.WXK_NUMPAD_EQUAL: Numpad_Equal,
    wx.WXK_NUMPAD_MULTIPLY: Numpad_Multiply,
    wx.WXK_NUMPAD_ADD: Numpad_Add,
    wx.WXK_NUMPAD_SEPARATOR: Numpad_Separator,
    wx.WXK_NUMPAD_SUBTRACT: Numpad_Subtract,
    wx.WXK_NUMPAD_DECIMAL: Numpad_Decimal,
    wx.WXK_NUMPAD_DIVIDE: Numpad_Divide,
}

_mouse_events = {
    wx.EVT_LEFT_DOWN.evtType[0]: MouseLeft,
    wx.EVT_LEFT_UP.evtType[0]: MouseLeft,
    wx.EVT_MIDDLE_DOWN.evtType[0]: MouseMiddle,
    wx.EVT_MIDDLE_UP.evtType[0]: MouseMiddle,
    wx.EVT_RIGHT_DOWN.evtType[0]: MouseRight,
    wx.EVT_RIGHT_UP.evtType[0]: MouseRight,
    wx.EVT_MOUSE_AUX1_DOWN.evtType[0]: MouseAux1,
    wx.EVT_MOUSE_AUX1_UP.evtType[0]: MouseAux1,
    wx.EVT_MOUSE_AUX2_DOWN.evtType[0]: MouseAux2,
    wx.EVT_MOUSE_AUX2_UP.evtType[0]: MouseAux2,
}


def serialise_modifier(
    evt: Union[wx.KeyEvent, wx.MouseEvent], key: int
) -> ModifierType:
    modifier = []
    if evt.ControlDown():
        if key not in (wx.WXK_SHIFT, wx.WXK_ALT):
            # if control is pressed the real key must not be a modifier
            modifier.append(Control)
            if evt.ShiftDown():
                modifier.append(Shift)
            if evt.AltDown():
                modifier.append(Alt)
    return tuple(modifier)


def serialise_key(evt: Union[wx.KeyEvent, wx.MouseEvent]) -> Optional[KeyType]:
    """Get the serialised version of the key that was pressed/released."""
    if isinstance(evt, wx.KeyEvent):
        key = evt.GetUnicodeKey() or evt.GetKeyCode()

        if 33 <= key <= 126:
            key = chr(key).upper()
        elif key in key_string_map:
            key = key_string_map[key]
        else:
            key = f"UNKNOWN KEY {key}"
        return key
    elif isinstance(evt, wx.MouseEvent):
        key = evt.GetEventType()
        if key in wx.EVT_MOUSEWHEEL.evtType:
            if evt.GetWheelRotation() < 0:
                return MouseWheelScrollDown
            elif evt.GetWheelRotation() > 0:
                return MouseWheelScrollUp
        elif key in _mouse_events:
            return _mouse_events[key]


def serialise_key_event(
    evt: Union[wx.KeyEvent, wx.MouseEvent]
) -> Optional[SerialisedKeyType]:
    if isinstance(evt, wx.KeyEvent):
        key = evt.GetUnicodeKey() or evt.GetKeyCode()
        if key == wx.WXK_CONTROL:
            return
        modifier = serialise_modifier(evt, key)

        if 33 <= key <= 126:
            key = chr(key).upper()
        elif key in key_string_map:
            key = key_string_map[key]
        else:
            key = f"UNKNOWN KEY {key}"
        return modifier, key
    elif isinstance(evt, wx.MouseEvent):
        key = evt.GetEventType()
        modifier = serialise_modifier(evt, key)
        if key in wx.EVT_MOUSEWHEEL.evtType:
            if evt.GetWheelRotation() < 0:
                return modifier, MouseWheelScrollDown
            elif evt.GetWheelRotation() > 0:
                return modifier, MouseWheelScrollUp
        elif key in _mouse_events:
            return modifier, _mouse_events[key]


def stringify_key(key: SerialisedKeyType) -> str:
    return " + ".join([str(s) for s in key[0] + (key[1],)])


class KeyCatcher(wx.Dialog):
    def __init__(self, parent: wx.Window, action: str):
        super().__init__(
            parent,
            title=f"Press the key you want assigned to {action}",
            style=wx.DEFAULT_DIALOG_STYLE | wx.WANTS_CHARS,
        )

        self._key = ((), "NONE")

        panel = wx.Panel(self)
        panel.SetFocus()

        panel.Bind(wx.EVT_LEFT_DOWN, self._on_key)
        panel.Bind(wx.EVT_MIDDLE_DOWN, self._on_key)
        panel.Bind(wx.EVT_RIGHT_DOWN, self._on_key)
        panel.Bind(wx.EVT_KEY_DOWN, self._on_key)
        panel.Bind(wx.EVT_MOUSEWHEEL, self._on_key)
        panel.Bind(wx.EVT_MOUSE_AUX1_DOWN, self._on_key)
        panel.Bind(wx.EVT_MOUSE_AUX2_DOWN, self._on_key)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def _on_key(self, evt):
        key = serialise_key_event(evt)
        if key is not None:
            self._key = key
            self.EndModal(1)

    @property
    def key(self) -> SerialisedKeyType:
        return self._key


# TODO: make any key able to be a modifier. Instead of registering keys on press register them on release.
#  When a key is pressed store it to a set of persistent keys. When a key is released that is the triggering
#  key and all persistent keys are modifiers.
#  In the actual program detect all keys on press/release as normal but also store the set of persistent keys.
#  When serialising give the key that was pressed/released along with all the modifiers.
#  Return all actions that use the triggering key as the triggering key and use a sub-set of the persistent keys.


class KeyConfigDialog(SimpleDialog):
    def __init__(
        self,
        parent: wx.Window,
        selected_group: KeybindGroupIdType,
        entries: Sequence[KeyActionType],
        fixed_keybinds: KeybindContainer,
        user_keybinds: KeybindContainer,
    ):
        super().__init__(parent, "Key Select")
        self._key_config = KeyConfig(
            self, selected_group, entries, fixed_keybinds, user_keybinds
        )
        self.sizer.Add(self._key_config, 1, wx.EXPAND)
        self.Layout()
        self.Fit()

    @property
    def options(self) -> Tuple[KeybindContainer, KeybindGroupIdType, KeybindGroup]:
        return self._key_config.options


class KeyConfig(wx.BoxSizer):
    def __init__(
        self,
        parent: wx.Window,
        selected_group: KeybindGroupIdType,
        entries: Sequence[KeyActionType],
        fixed_keybinds: KeybindContainer,
        user_keybinds: KeybindContainer,
    ):
        super().__init__(wx.VERTICAL)
        self._entries = entries
        self._fixed_keybinds = fixed_keybinds
        self._user_keybinds = user_keybinds

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Add(top_sizer, 0, wx.EXPAND)
        self._choice = SimpleChoice(
            parent,
            list(self._fixed_keybinds.keys()) + list(self._user_keybinds.keys()),
            selected_group,
        )
        self._choice.Bind(wx.EVT_CHOICE, self._on_group_change)
        top_sizer.Add(self._choice, 1, wx.ALL | wx.EXPAND, 5)

        add = wx.BitmapButton(parent, bitmap=ADD_ICON.bitmap(32, 32))
        add.Bind(wx.EVT_BUTTON, lambda evt: self._create_new_group())
        top_sizer.Add(add, 0, wx.ALL, 5)

        self._delete = wx.BitmapButton(parent, bitmap=SUBTRACT_ICON.bitmap(32, 32))
        self._delete.Bind(wx.EVT_BUTTON, lambda evt: self._delete_group())
        top_sizer.Add(self._delete, 0, wx.ALL, 5)

        self._rename = wx.BitmapButton(parent, bitmap=EDIT_ICON.bitmap(32, 32))
        self._rename.Bind(wx.EVT_BUTTON, lambda evt: self._rename_group())
        top_sizer.Add(self._rename, 0, wx.ALL, 5)

        self._options = SimpleScrollablePanel(parent, size=(500, 500))
        self.Add(self._options, 1, wx.EXPAND)

        grid_sizer = wx.GridSizer(len(entries), 2, 5, 5)
        self._options.sizer.Add(grid_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self._key_buttons: Dict[str, wx.Button] = {}
        for action in entries:
            grid_sizer.Add(
                wx.StaticText(self._options, label=action.title()), 0, wx.ALIGN_CENTER
            )
            self._key_buttons[action] = button = wx.Button(self._options)
            button.Bind(wx.EVT_BUTTON, lambda evt, a=action: self._modify_button(a))
            grid_sizer.Add(button, 0, wx.EXPAND)
        self._rebuild_buttons()

    def _rebuild_buttons(self):
        group_id = self._choice.GetCurrentString()
        if group_id in self._fixed_keybinds:
            group = self._fixed_keybinds[group_id]
            self._delete.Disable()
            self._rename.Disable()
        else:
            group = self._user_keybinds[group_id]
            self._delete.Enable()
            self._rename.Enable()

        for action in self._entries:
            self._key_buttons[action].SetLabel(
                stringify_key(group.get(action, ((), "NONE")))
            )

    def _rebuild_choice(self, group_name=None):
        index = self._choice.GetSelection()
        self._choice.SetItems(
            list(self._fixed_keybinds.keys()) + list(self._user_keybinds.keys())
        )
        if group_name is not None:
            self._choice.SetSelection(self._choice.FindString(group_name))
        else:
            self._choice.SetSelection(max(index - 1, 0))
        self._rebuild_buttons()

    def _delete_group(self):
        group = self._choice.GetCurrentString()
        if group in self._user_keybinds:
            del self._user_keybinds[group]
            self._rebuild_choice()

    def _request_group_name(self) -> Optional[str]:
        group_name = ""
        while group_name == "":
            msg = wx.TextEntryDialog(self._options, "Enter a new group name.")
            if msg.ShowModal() == wx.ID_OK:
                group_name = msg.GetValue()
                if (
                    group_name in self._fixed_keybinds
                    or group_name in self._user_keybinds
                ):
                    group_name = ""
            else:
                return
        return group_name

    def _rename_group(self):
        old_group_name = self._choice.GetCurrentString()
        if old_group_name in self._user_keybinds:
            group_name = self._request_group_name()
            if group_name is None:
                return
            group = self._user_keybinds[old_group_name]
            del self._user_keybinds[old_group_name]
            self._user_keybinds[group_name] = group
            self._rebuild_choice(group_name)

    def _create_new_group(self):
        group_name = self._request_group_name()
        if group_name is None:
            return
        old_group_name = self._choice.GetCurrentString()
        if old_group_name in self._fixed_keybinds:
            group = self._fixed_keybinds[old_group_name]
        else:
            group = self._user_keybinds[old_group_name]
        self._user_keybinds[group_name] = group.copy()
        self._rebuild_choice(group_name)

    def _modify_button(self, action):
        if self._choice.GetCurrentString() in self._fixed_keybinds:
            msg = wx.MessageDialog(
                self._options,
                "The active key group is not editable. Would you like to create a new group to edit?",
                style=wx.YES_NO,
            )
            if msg.ShowModal() == wx.ID_YES:
                self._create_new_group()
            else:
                return
        group_name = self._choice.GetCurrentString()
        if group_name in self._user_keybinds:
            catcher = KeyCatcher(self._options, action)
            catcher.ShowModal()
            self._user_keybinds[group_name][action] = catcher.key
            self._rebuild_buttons()

    def _on_group_change(self, evt):
        self._rebuild_buttons()

    @property
    def options(self) -> Tuple[KeybindContainer, KeybindGroupIdType, KeybindGroup]:
        keybind_group = self._choice.GetCurrentString()
        if keybind_group in self._fixed_keybinds:
            keybinds = self._fixed_keybinds[keybind_group]
        else:
            keybinds = self._user_keybinds[keybind_group]
        return self._user_keybinds, keybind_group, keybinds
