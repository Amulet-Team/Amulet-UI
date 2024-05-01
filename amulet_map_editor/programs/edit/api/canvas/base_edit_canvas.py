import logging
import wx
import traceback
from OpenGL.GL import (
    glClearColor,
    glViewport,
)
import os
from typing import Optional, Generator
import weakref
import sys
import time

from minecraft_model_reader.api.resource_pack.java.download_resources import (
    get_java_vanilla_latest_iter,
    get_java_vanilla_fix,
)
from minecraft_model_reader.api.resource_pack.java import (
    JavaResourcePack,
)
from minecraft_model_reader.api.resource_pack.bedrock.download_resources import (
    get_bedrock_vanilla_latest_iter,
    get_bedrock_vanilla_fix,
)
from minecraft_model_reader.api.resource_pack.bedrock import BedrockResourcePack
from minecraft_model_reader.api.resource_pack import (
    load_resource_pack,
    load_resource_pack_manager,
)
from amulet.api.player import LOCAL_PLAYER

from amulet.api.data_types import OperationYieldType, Dimension

from amulet_map_editor import experimental_bedrock_resources
from amulet_map_editor.api.opengl.canvas import EventCanvas
from amulet_map_editor.api.opengl.resource_pack.resource_pack import OpenGLResourcePack
from amulet_map_editor.programs.edit.api.selection import (
    SelectionManager,
    SelectionHistoryManager,
)
from amulet_map_editor import lang
import amulet_map_editor.programs.edit as amulet_edit

from amulet_map_editor.api.opengl.camera import ControllableCamera
from amulet_map_editor.api.wx.util.button_input import ButtonInput
from amulet_map_editor.api.wx.util.mouse_movement import MouseMovement
from amulet_map_editor.api.wx.ui.traceback_dialog import TracebackDialog
from ..renderer import Renderer

from amulet.api.level import BaseLevel

log = logging.getLogger(__name__)


class BaseEditCanvas(EventCanvas):
    """Adds base logic for drawing everything related to the edit program to the canvas.
    All the user interaction code is implemented in ControllableEditCanvas to make them easier to read.
    """

    background_colour = (0.61, 0.70, 0.85)

    def __init__(self, parent: wx.Window, world: BaseLevel):
        super().__init__(parent)
        self._world = weakref.ref(world)

        self._selection: Optional[SelectionHistoryManager] = SelectionHistoryManager(
            SelectionManager(self)
        )
        self.world.history_manager.register(self._selection, False)

        self._camera: ControllableCamera = ControllableCamera(self)

        self._camera.move_speed = 2.0
        self._camera.rotate_speed = 2.0

        self._buttons: ButtonInput = ButtonInput(self)
        self._mouse: MouseMovement = MouseMovement(self)
        self._mouse.set_middle()

        resource_packs_dir = os.path.join(os.environ["DATA_DIR"], "resource_packs")
        readme_path = os.path.join(resource_packs_dir, "readme.txt")
        # create the resource packs location
        os.makedirs(resource_packs_dir, exist_ok=True)
        if not os.path.isfile(readme_path):
            with open(readme_path, "w") as f:
                f.write("Put the Java resource pack you want loaded in here.")

        self._renderer: Optional[Renderer] = None
        self._opengl_resource_pack = None

    def thread_setup(self) -> Generator[OperationYieldType, None, None]:
        """
        Set up objects that take a while to set up.
        All code in here must be thread safe and not touch the OpenGL state.
        """
        packs = []
        resource_packs_dir = os.path.join(os.environ["DATA_DIR"], "resource_packs")
        user_packs = [
            load_resource_pack(os.path.join(resource_packs_dir, rp))
            for rp in os.listdir(resource_packs_dir)
            if os.path.isdir(os.path.join(resource_packs_dir, rp))
        ]
        if (
            self.world.level_wrapper.platform == "bedrock"
            and experimental_bedrock_resources
        ):
            packs.append(
                load_resource_pack(
                    os.path.join(
                        os.path.dirname(amulet_edit.__file__),
                        "amulet_resource_pack",
                        "bedrock",
                    )
                )
            )
            yield 0.1, lang.get(
                "program_3d_edit.canvas.downloading_bedrock_vanilla_resource_pack"
            )
            gen = get_bedrock_vanilla_latest_iter()
            try:
                while True:
                    yield next(gen) * 0.4 + 0.1
            except StopIteration as e:
                packs.append(e.value)
            yield 0.5, lang.get("program_3d_edit.canvas.loading_resource_packs")

            packs += [
                pack for pack in user_packs if isinstance(pack, BedrockResourcePack)
            ]
            packs.append(get_bedrock_vanilla_fix())

            translator = self.world.translation_manager.get_version(
                "bedrock", (999, 0, 0)
            )
        else:
            packs.append(
                load_resource_pack(
                    os.path.join(
                        os.path.dirname(amulet_edit.__file__),
                        "amulet_resource_pack",
                        "java",
                    )
                )
            )
            yield 0.1, lang.get(
                "program_3d_edit.canvas.downloading_java_vanilla_resource_pack"
            )
            while True:
                gen = get_java_vanilla_latest_iter()
                try:
                    while True:
                        yield next(gen) * 0.4 + 0.1
                except StopIteration as e:
                    packs.append(e.value)
                    break
                except Exception as e:
                    if sys.platform == "darwin" and "CERTIFICATE_VERIFY_FAILED" in str(e):
                        msg = lang.get(
                            "program_3d_edit.canvas.java_rp_failed_mac_certificates"
                        )
                    else:
                        msg = lang.get("program_3d_edit.canvas.java_rp_failed_default")
                    log.error(
                        msg,
                        exc_info=True,
                    )
                    wait = True
                    tb = traceback.format_exc()

                    def show_error():
                        nonlocal wait
                        try:
                            dialog = TracebackDialog(
                                self,
                                lang.get("program_3d_edit.canvas.java_rp_failed"),
                                f"{msg}\n{e}",
                                tb,
                            )
                            dialog.ShowModal()
                            dialog.Destroy()
                        finally:
                            wait = False

                    wx.CallAfter(show_error)
                    while wait:
                        time.sleep(0.1)

                    msg = wx.MessageDialog(
                        self,
                        lang.get("program_3d_edit.canvas.retry_download"),
                        style=wx.YES_NO,
                    )
                    if msg.ShowModal() == wx.ID_NO:
                        break

            yield 0.5, lang.get("program_3d_edit.canvas.loading_resource_packs")
            packs += [pack for pack in user_packs if isinstance(pack, JavaResourcePack)]
            packs.append(get_java_vanilla_fix())

            translator = self.world.translation_manager.get_version("java", (999, 0, 0))

        resource_pack = load_resource_pack_manager(packs, load=False)
        for i in resource_pack.reload():
            yield i / 4 + 0.5

        self._opengl_resource_pack = OpenGLResourcePack(resource_pack, translator)

        yield 0.75, lang.get("program_3d_edit.canvas.creating_texture_atlas")
        for i in self._opengl_resource_pack.setup():
            yield i / 4 + 0.75

    def post_thread_setup(self) -> Generator[OperationYieldType, None, None]:
        """
        Any logic that needs to be run after everything has been set up.
        Code here will be run from the main thread.
        The canvas has still not been shown here so do not touch the OpenGL state. Do this in _init_opengl.
        """
        yield 1.0, lang.get("program_3d_edit.canvas.setting_up_renderer")
        self._renderer: Optional[Renderer] = Renderer(
            self,
            self.world,
            self.context_identifier,
            self._opengl_resource_pack,
        )

    def _init_opengl(self):
        super()._init_opengl()
        glClearColor(*self.background_colour, 1.0)

        try:
            player = self.world.get_player(LOCAL_PLAYER)
            location, rotation = player.location, player.rotation
            self.dimension = player.dimension
        except:
            location, rotation = (0.0, 100.0, 0.0), (45.0, 45.0)

        self._camera.location_rotation = location, rotation
        self._renderer.move_camera(location, rotation)

    def bind_events(self):
        """Set up all events required to run.
        Note this will also bind subclass events."""
        self.Bind(wx.EVT_SIZE, self._on_size)
        self.selection.bind_events()
        self.buttons.bind_events()
        self.mouse.bind_events()
        self.renderer.bind_events()

    def enable(self):
        """Enable the canvas and start it working."""
        self.SetCurrent(self._context)
        self.renderer.enable()
        self.buttons.enable()

    def disable(self):
        """Disable the canvas and unload all geometry."""
        self.renderer.disable()
        self.buttons.disable()

    def is_closeable(self):
        """Check that the canvas and contained data is safe to be closed."""
        return self.renderer.is_closeable()

    def close(self):
        """Destroy all contained data so that the window can be safely destroyed."""
        self.renderer.close()

    @property
    def world(self) -> BaseLevel:
        """The amulet-core `BaseLevel` subclass representing the "world" that is open."""
        return self._world()

    @property
    def renderer(self) -> Renderer:
        """The `Renderer` class that handles the drawable objects and draws them."""
        return self._renderer

    @property
    def dimension(self) -> Dimension:
        """The currently loaded dimension in the renderer."""
        return self.renderer.dimension

    @dimension.setter
    def dimension(self, dimension: Dimension):
        """Set the currently loaded dimension in the renderer."""
        self.renderer.dimension = dimension

    @property
    def camera(self) -> ControllableCamera:
        """A class holding the state of the camera with methods to access and modify the state."""
        return self._camera

    @property
    def buttons(self) -> ButtonInput:
        """A class that manages converting button presses into actions based on set keybinds."""
        return self._buttons

    @property
    def mouse(self) -> MouseMovement:
        """A class that manages mouse movement."""
        return self._mouse

    @property
    def selection(self) -> SelectionManager:
        """A simple class for storing the selection state."""
        return self._selection.value

    def _on_size(self, evt):
        wx.CallAfter(self._set_size)
        evt.Skip()

    def _set_size(self):
        size = self.GetClientSize() * self.GetContentScaleFactor()
        width, height = size
        self.SetCurrent(self._context)
        glViewport(0, 0, width, height)
        if height > 0:
            self.camera.aspect_ratio = width / height
        else:
            self.camera.aspect_ratio = 1
