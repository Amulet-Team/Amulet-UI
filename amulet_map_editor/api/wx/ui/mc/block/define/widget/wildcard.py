import wx
import wx.lib.scrolledpanel

import PyMCTranslate
import amulet_nbt
from amulet_map_editor.api.wx.ui.events import EVT_CHILD_SIZE

from amulet_map_editor.api.wx.ui.mc.block import (
    MultiplePropertySelect,
    EVT_MULTIPLE_PROPERTIES_CHANGE,
)
from amulet_map_editor.api.wx.ui.mc.block.define.widget.base import BaseBlockDefine
from amulet_map_editor.api.wx.ui.mc.block.define.events import (
    WildcardBlockChangeEvent,
    EVT_WILDCARD_BLOCK_CHANGE,
)
from amulet_map_editor.api.wx.ui.mc.state import BlockState


class WildcardBlockDefine(BaseBlockDefine):
    """
    A UI that merges a version select widget with a block select widget and a multi property select.
    """

    state: BlockState
    _property_picker: MultiplePropertySelect

    def __init__(
        self,
        parent,
        state: BlockState,
        *,
        show_pick_block: bool = False,
        orientation=wx.VERTICAL,
    ):
        assert isinstance(state, BlockState)
        BaseBlockDefine.__init__(
            self,
            parent,
            state,
            orientation=orientation,
            show_pick_block=show_pick_block,
        )

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        border = wx.LEFT if orientation == wx.HORIZONTAL else wx.TOP
        self._sizer.Add(right_sizer, 1, wx.EXPAND | border, 5)
        self._property_picker = MultiplePropertySelect(self, state)
        right_sizer.Add(self._property_picker, 1, wx.EXPAND)
        self._property_picker.Bind(EVT_MULTIPLE_PROPERTIES_CHANGE, self._post_change)
        self._child_state_holders.append(self._property_picker)

        self.Layout()

    def _post_change(self, evt):
        wx.PostEvent(
            self,
            WildcardBlockChangeEvent(
                self.state.platform,
                self.state.version_number,
                self.state.force_blockstate,
                self.state.namespace,
                self.state.base_name,
                self.state.properties_multiple,
            ),
        )


def demo():
    """
    Show a demo version of the UI.
    An app instance must be created first.
    """
    translation_manager = PyMCTranslate.new_translation_manager()

    def create_dialog(block):
        dialog = wx.Dialog(
            None,
            title=f"WildcardBlockDefine with block {block['namespace']}:{block['base_name']}",
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.DIALOG_NO_PARENT,
        )
        sizer = wx.BoxSizer()
        dialog.SetSizer(sizer)
        obj = WildcardBlockDefine.from_data(
            dialog,
            translation_manager,
            platform="java",
            version_number=(1, 16, 0),
            force_blockstate=False,
            **block,
            orientation=wx.HORIZONTAL,
        )

        sizer.Add(
            obj,
            1,
            wx.ALL,
            5,
        )

        def on_change(evt: WildcardBlockChangeEvent):
            print(
                evt.platform,
                evt.version_number,
                evt.force_blockstate,
                evt.namespace,
                evt.base_name,
                evt.selected_properties,
            )

        def on_close(evt):
            dialog.Destroy()

        def on_child_size(evt):
            dialog.Layout()
            evt.Skip()

        obj.Bind(EVT_WILDCARD_BLOCK_CHANGE, on_change)
        dialog.Bind(wx.EVT_CLOSE, on_close)
        dialog.Bind(EVT_CHILD_SIZE, on_child_size)
        dialog.Show()
        dialog.Fit()

    for block_ in (
        {
            "namespace": "minecraft",
            "base_name": "oak_fence",
            "properties_multiple": {
                "east": (
                    amulet_nbt.TAG_String("true"),
                    amulet_nbt.TAG_String("false"),
                ),
                "north": (
                    amulet_nbt.TAG_String("true"),
                    amulet_nbt.TAG_String("false"),
                ),
                "south": (amulet_nbt.TAG_String("false"),),
                "west": (amulet_nbt.TAG_String("true"),),
            },
        },
        {
            "namespace": "modded",
            "base_name": "block",
            "properties_multiple": {
                "test": (
                    amulet_nbt.TAG_String("hello"),
                    amulet_nbt.TAG_String("hello2"),
                ),
            },
        },
    ):
        create_dialog(block_)


if __name__ == "__main__":

    def main():
        app = wx.App()
        demo()
        app.MainLoop()

    main()
