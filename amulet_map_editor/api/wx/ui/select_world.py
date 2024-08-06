import os
import wx
import glob
from sys import platform
from typing import List, Dict, Tuple, Callable, TYPE_CHECKING
import traceback
import logging

from amulet import load_format
from amulet.api.errors import FormatError

from amulet_map_editor import lang, CONFIG
from amulet_map_editor.api.wx.ui import simple
from amulet_map_editor.api.wx.util.ui_preferences import preserve_ui_preferences
from amulet_map_editor.api.framework import app


if TYPE_CHECKING:
    from amulet.api.wrapper import WorldFormatWrapper

log = logging.getLogger(__name__)


# Windows 	%APPDATA%\.minecraft
# macOS 	~/Library/Application Support/minecraft
# Linux 	~/.minecraft

minecraft_world_paths = {}

if platform == "win32":
    minecraft_world_paths[lang.get("world.java_platform")] = os.path.join(
        os.getenv("APPDATA"), ".minecraft", "saves"
    )
    minecraft_world_paths[lang.get("world.bedrock_platform")] = os.path.join(
        os.getenv("LOCALAPPDATA"),
        "Packages",
        "Microsoft.MinecraftUWP_8wekyb3d8bbwe",
        "LocalState",
        "games",
        "com.mojang",
        "minecraftWorlds",
    )
    minecraft_world_paths[lang.get("world.bedrock_education_platform")] = os.path.join(
        os.getenv("LOCALAPPDATA"),
        "Packages",
        "Microsoft.MinecraftEducationEdition_8wekyb3d8bbwe",
        "LocalState",
        "games",
        "com.mojang",
        "minecraftWorlds",
    )
elif platform == "darwin":
    minecraft_world_paths[lang.get("world.java_platform")] = os.path.join(
        os.path.expanduser("~"), "Library", "Application Support", "minecraft", "saves"
    )
elif platform == "linux":
    minecraft_world_paths[lang.get("world.java_platform")] = os.path.join(
        os.path.expanduser("~"), ".minecraft", "saves"
    )

world_images: Dict[str, Tuple[int, wx.Bitmap, int]] = {}


def get_world_image(image_path: str) -> Tuple[wx.Bitmap, int]:
    if (
        image_path not in world_images
        or world_images[image_path][0] != os.stat(image_path)[8]
    ):
        img = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        width = min(int((img.GetWidth() / img.GetHeight()) * 128), 300)

        world_images[image_path] = (
            os.stat(image_path)[8],
            img.Scale(width, 128, wx.IMAGE_QUALITY_NEAREST).ConvertToBitmap(),
            width,
        )

    return world_images[image_path][1:3]


class WorldUI(wx.Panel):
    """A Panel UI element with the world image, name and description"""

    def __init__(self, parent: wx.Window, world_format: "WorldFormatWrapper"):
        super().__init__(parent)
        self.SetWindowStyle(wx.TAB_TRAVERSAL | wx.BORDER_RAISED)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)

        img, width = get_world_image(world_format.world_image_path)

        self.img = wx.StaticBitmap(self, wx.ID_ANY, img, (0, 0), (width, 128))
        sizer.Add(self.img)

        self.world_name = wx.StaticText(
            self,
            label="\n".join(
                [
                    world_format.level_name,
                    world_format.game_version_string,
                    os.path.join(
                        *os.path.normpath(world_format.path).split(os.sep)[-3:]
                    ),
                ]
            ),
        )
        sizer.Add(self.world_name, 0, wx.ALL | wx.ALIGN_CENTER, 5)


class WorldUIButton(WorldUI):
    """A Panel UI element that behaves like a button with the world image, name and description"""

    def __init__(
        self,
        parent: wx.Window,
        world_format: "WorldFormatWrapper",
        open_world_callback,
    ):
        super().__init__(parent, world_format)
        self.path = world_format.path
        self.open_world_callback = open_world_callback

        self.Bind(wx.EVT_LEFT_UP, self._call_callback)
        self.img.Bind(wx.EVT_LEFT_UP, self._call_callback)
        self.world_name.Bind(wx.EVT_LEFT_DOWN, self._call_callback)

    def _call_callback(self, evt):
        self.open_world_callback(self.path)


class WorldList(wx.Panel):
    """A Panel containing zero or more `WorldUIButton`s."""

    def __init__(self, parent: wx.Window, world_dirs, open_world_callback, sort=True):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.worlds = []

        world_formats = []
        for world_path in world_dirs:
            if os.path.isdir(world_path):
                try:
                    world_formats.append(load_format(world_path))
                except FormatError as e:
                    log.info(f"Could not find loader for {world_path} {e}")
                except Exception:
                    log.error(
                        f"Error loading format wrapper for {world_path} {traceback.format_exc()}"
                    )
        if sort:
            world_formats = reversed(sorted(world_formats, key=lambda f: f.last_played))

        for world_format in world_formats:
            try:
                world_button = WorldUIButton(self, world_format, open_world_callback)
                sizer.Add(
                    world_button, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5
                )
                self.worlds.append(world_button)
            except Exception as e:
                log.info(f"Failed to display world button for {world_format.path} {e}")

        self.Layout()


class CollapsibleWorldListUI(wx.CollapsiblePane):
    """a drop down list of `WorldUIButton`s for a given directory"""

    def __init__(self, parent, paths: List[str], group_name: str, open_world_callback):
        super().__init__(parent, label=group_name)
        self.parent = parent
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.eval_layout)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        panel = self.GetPane()
        panel.sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(panel.sizer)
        panel.sizer.Add(WorldList(panel, paths, open_world_callback), 0, wx.EXPAND)

    def eval_layout(self, evt):
        self.Layout()
        self.parent.FitInside()
        evt.Skip()


class ScrollableWorldsUI(simple.SimpleScrollablePanel):
    # a frame to allow scrolling
    def __init__(self, parent, open_world_callback):
        super(ScrollableWorldsUI, self).__init__(parent)
        self.open_world_callback = open_world_callback

        self.dirs: Dict[str, CollapsibleWorldListUI] = {}
        self.reload()

        self.Layout()

    def reload(self):
        for val in self.dirs.values():
            val.Destroy()
        self.dirs.clear()
        for group_name, directory in minecraft_world_paths.items():
            if os.path.isdir(directory):
                world_list = CollapsibleWorldListUI(
                    self,
                    glob.glob(os.path.join(glob.escape(directory), "*")),
                    group_name,
                    self.open_world_callback,
                )
                self.add_object(world_list, 0, wx.EXPAND)
                self.dirs[directory] = world_list

    def OnChildFocus(self, event):
        event.Skip()


class WorldSelectUI(wx.Panel):
    # a frame containing a refresh button for the UI, a sort order for the worlds
    # and a vertical list of `WorldDirectoryUI`s for each directory
    # perhaps also a select directory option
    def __init__(self, parent, open_world_callback):
        super().__init__(parent)
        self.open_world_callback = open_world_callback

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.header_open_world = wx.Button(
            self, label=lang.get("select_world.open_world_button")
        )
        self.header_open_world.Bind(wx.EVT_BUTTON, self._open_world)
        sizer.Add(self.header_open_world)

        content = ScrollableWorldsUI(self, open_world_callback)
        sizer.Add(content, 1, wx.EXPAND)

    def _open_world(self, evt):
        dir_dialog = wx.DirDialog(
            None,
            lang.get("select_world.open_world_dialogue"),
            "",
            wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST,
        )
        try:
            if dir_dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = dir_dialog.GetPath()
        except Exception:
            wx.LogError(lang.get("select_world.select_directory_failed"))
            return
        finally:
            dir_dialog.Destroy()
        self.open_world_callback(path)


class RecentWorldUI(wx.Panel):
    def __init__(self, parent, open_world_callback):
        super().__init__(parent)
        self._open_world_callback = open_world_callback

        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self._sizer)

        text = wx.StaticText(
            self,
            wx.ID_ANY,
            lang.get("select_world.recent_worlds"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        text.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self._sizer.Add(
            text,
            0,
            wx.ALL | wx.ALIGN_CENTER,
            5,
        )

        self._world_list = None
        self.rebuild()

    def rebuild(self, new_world: str = None):
        meta: dict = CONFIG.get("amulet_meta", {})
        recent_worlds: list = meta.setdefault("recent_worlds", [])
        if new_world is not None:
            while new_world in recent_worlds:
                recent_worlds.remove(new_world)
            recent_worlds.insert(0, new_world)
            while len(recent_worlds) > 5:
                recent_worlds.pop(5)
        if self._world_list is not None:
            self._world_list.Destroy()
        self._world_list = WorldList(
            self, recent_worlds, self._open_world_callback, sort=False
        )
        self._sizer.Add(self._world_list, 1, wx.EXPAND, 5)
        self.Layout()
        CONFIG.put("amulet_meta", meta)


class WorldSelectAndRecentUI(wx.Panel):
    def __init__(self, parent, open_world_callback):
        super(WorldSelectAndRecentUI, self).__init__(parent, wx.HORIZONTAL)
        self._open_world_callback = open_world_callback

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        warning_text = wx.StaticText(
            self,
            label=lang.get("select_world.open_world_warning"),
        )
        warning_text.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        sizer.Add(warning_text, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)
        # bar

        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(bottom_sizer, 1, wx.EXPAND)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        bottom_sizer.Add(left_sizer, 1, wx.EXPAND)
        select_world = WorldSelectUI(self, self._update_recent)
        left_sizer.Add(select_world, 1, wx.ALL | wx.EXPAND, 5)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        bottom_sizer.Add(right_sizer, 1, wx.EXPAND)
        self._recent_worlds = RecentWorldUI(self, self._update_recent)
        right_sizer.Add(self._recent_worlds, 1, wx.EXPAND, 5)

    def _update_recent(self, path):
        self._recent_worlds.rebuild(path)
        self._open_world_callback(path)


@preserve_ui_preferences
class WorldSelectDialog(wx.Dialog):
    def __init__(self, parent: wx.Window, open_world_callback: Callable[[str], None]):
        super().__init__(
            parent,
            title=lang.get("select_world.title"),
            pos=wx.Point(50, 50),
            size=wx.Size(*[int(s * 0.95) for s in parent.GetSize()]),
            style=wx.CAPTION | wx.CLOSE_BOX | wx.MAXIMIZE_BOX
            # | wx.MAXIMIZE
            | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.RESIZE_BORDER,
        )
        self.Bind(wx.EVT_CLOSE, self._hide_event)

        self._open_world_callback = open_world_callback
        self.world_select = WorldSelectAndRecentUI(self, self._run_callback)

    def _run_callback(self, path):
        self._close()
        self._open_world_callback(path)

    def _hide_event(self, evt):
        self._close()
        evt.Skip()

    def _close(self):
        if self.IsModal():
            self.EndModal(0)
        else:
            self.Close()


def open_level_from_dialog(parent: wx.Window):
    """Show the open world dialog and open the selected world."""
    select_world = WorldSelectDialog(parent, app.open_level)
    select_world.ShowModal()
    select_world.Destroy()
