import webbrowser
from urllib.request import urlopen
from urllib.error import URLError
import json
import wx
import wx.adv
import wx.lib.inspection

from amulet_map_editor.api import image, lang
from .base_page import BasePageUI
from amulet_map_editor.api.wx.ui.select_world import open_level_from_dialog


class AmuletMainMenu(wx.Panel, BasePageUI):
    def __init__(self, parent: wx.Window):
        super(AmuletMainMenu, self).__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self._lang_button = wx.BitmapButton(
            self, bitmap=image.icon.tablericons.language.bitmap(64, 64)
        )
        self._lang_button.Bind(wx.EVT_BUTTON, self._select_language)
        sizer.Add(self._lang_button, 0, wx.ALIGN_RIGHT)

        sizer.AddStretchSpacer(1)
        name_sizer = wx.BoxSizer()
        sizer.Add(name_sizer, 0, wx.CENTER)
        icon_img = image.logo.amulet_logo.bitmap(64, 64)

        icon = wx.StaticBitmap(self, wx.ID_ANY, icon_img, (0, 0), (64, 64))
        icon2 = wx.StaticBitmap(self, wx.ID_ANY, icon_img, (0, 0), (64, 64))
        icon2.Bind(
            wx.EVT_LEFT_DOWN, lambda evt: wx.lib.inspection.InspectionTool().Show()
        )
        name_sizer.Add(icon, flag=wx.CENTER)

        self._amulet_name = wx.StaticText(self)
        self._amulet_name.SetFont(wx.Font(40, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        name_sizer.Add(
            self._amulet_name, flag=wx.CENTER | wx.LEFT | wx.RIGHT, border=10
        )
        name_sizer.Add(icon2, flag=wx.CENTER)
        button_font = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self._open_world_button = wx.Button(self, size=(400, 70))
        self._open_world_button.SetFont(button_font)
        self._open_world_button.Bind(
            wx.EVT_BUTTON, lambda _: open_level_from_dialog(self)
        )
        sizer.Add(self._open_world_button, 0, wx.ALL | wx.CENTER, 5)

        self._user_manual_button = wx.Button(self, size=(400, 70))
        self._user_manual_button.SetFont(button_font)
        self._user_manual_button.Bind(wx.EVT_BUTTON, self._documentation)
        sizer.Add(self._user_manual_button, 0, wx.ALL | wx.CENTER, 5)

        self._bug_tracker_button = wx.Button(self, size=(400, 70))
        self._bug_tracker_button.SetFont(button_font)
        self._bug_tracker_button.Bind(wx.EVT_BUTTON, self._bugs)
        sizer.Add(self._bug_tracker_button, 0, wx.ALL | wx.CENTER, 5)

        self._discord_button = wx.Button(self, size=(400, 70))
        self._discord_button.SetFont(button_font)
        self._discord_button.Bind(wx.EVT_BUTTON, self._discord)
        sizer.Add(self._discord_button, 0, wx.ALL | wx.CENTER, 5)

        sizer.AddStretchSpacer(2)

        sponsor_header = wx.BoxSizer(wx.HORIZONTAL)
        self._sponsor_label = wx.StaticText(self)
        self._sponsor_link = wx.adv.HyperlinkCtrl(
            self, url="https://github.com/sponsors/Amulet-Team"
        )
        sponsor_header.AddStretchSpacer(1)
        sponsor_header.Add(self._sponsor_label)
        sponsor_header.AddSpacer(10)
        sponsor_header.Add(self._sponsor_link)
        sponsor_header.AddStretchSpacer(1)
        sizer.Add(sponsor_header, 0, wx.EXPAND, 0)

        sponsor_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(sponsor_sizer, 1, wx.EXPAND, 0)
        pathway_bitmap = image.logo.pathway_logo.bitmap(300, 130)
        pathway_button = wx.StaticBitmap(
            self, wx.ID_ANY, pathway_bitmap, (0, 0), (300, 130)
        )
        pathway_button.Bind(wx.EVT_LEFT_DOWN, self._pathway)
        sponsor_sizer.Add(pathway_button, 0, wx.EXPAND, 0)

        try:
            with urlopen(
                "https://raw.githubusercontent.com/Amulet-Team/sponsors/main/sponsors.json"
            ) as f:
                sponsors = json.load(f)
            github_sponsor_text = wx.TextCtrl(
                self,
                value="   ".join(sponsors),
                style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_CENTRE | wx.BORDER_NONE,
                size=wx.Size(-1, 150),
            )
            github_sponsor_text.SetBackgroundColour(self.GetBackgroundColour())
            sponsor_sizer.Add(github_sponsor_text, 1)
        except (URLError, json.JSONDecodeError):
            pass

        self._load_strings()

    def _load_strings(self):
        self._amulet_name.SetLabel(lang.get("meta.amulet"))
        self._open_world_button.SetLabel(lang.get("main_menu.open_world"))
        self._user_manual_button.SetLabel(lang.get("main_menu.user_manual"))
        self._user_manual_button.SetToolTip(lang.get("app.browser_open_tooltip"))
        self._bug_tracker_button.SetLabel(lang.get("main_menu.bug_tracker"))
        self._bug_tracker_button.SetToolTip(lang.get("app.browser_open_tooltip"))
        self._discord_button.SetLabel(lang.get("main_menu.discord"))
        self._discord_button.SetToolTip(lang.get("app.browser_open_tooltip"))
        self._sponsor_label.SetLabel(lang.get("main_menu.our_sponsors"))
        self._sponsor_link.SetLabel(lang.get("main_menu.sponsor_link"))

    @staticmethod
    def _documentation(_):
        webbrowser.open(
            "https://github.com/Amulet-Team/Amulet-Map-Editor/blob/master/amulet_map_editor/readme.md"
        )

    @staticmethod
    def _bugs(_):
        webbrowser.open(
            "https://github.com/Amulet-Team/Amulet-Map-Editor/issues?q=is%3Aissue"
        )

    @staticmethod
    def _discord(_):
        webbrowser.open("https://www.amuletmc.com/discord")

    @staticmethod
    def _pathway(_):
        webbrowser.open("https://www.pathway.studio/")

    def enable(self):
        self.GetTopLevelParent().create_menu()

    def _select_language(self, evt):
        dialog = LangSelectDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            lang.set_language(dialog.get_language())
        dialog.Destroy()
        self._load_strings()


class LangSelectDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: LangSelectDialog.__init__
        kwds["style"] = (
            kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle(lang.get("language_select.title"))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self._label = wx.StaticText(self, label=lang.get("language_select.help"))
        sizer_1.Add(self._label, 0, wx.ALIGN_CENTER)

        self.hyperlink_1 = wx.adv.HyperlinkCtrl(
            self,
            wx.ID_ANY,
            lang.get("language_select.contribute"),
            "https://github.com/Amulet-Team/Amulet-Map-Editor#contributing",
        )
        sizer_1.Add(self.hyperlink_1, 0, wx.ALIGN_CENTER)

        self._lang_list_box = wx.ListBox(self, choices=lang.get_languages())
        self._lang_list_box.SetSelection(
            self._lang_list_box.FindString(lang.get_language())
        )
        sizer_1.Add(self._lang_list_box, 1, wx.EXPAND, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

        self._button_ok = wx.Button(self, wx.ID_OK, "")
        self._button_ok.SetDefault()
        sizer_2.AddButton(self._button_ok)

        self._button_cancel = wx.Button(self, wx.ID_CANCEL, "")
        sizer_2.AddButton(self._button_cancel)

        sizer_2.Realize()

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.SetAffirmativeId(self._button_ok.GetId())
        self.SetEscapeId(self._button_cancel.GetId())

        self.Layout()

    def get_language(self):
        return self._lang_list_box.GetStringSelection()
