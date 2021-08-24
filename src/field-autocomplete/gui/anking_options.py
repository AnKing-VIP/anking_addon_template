# -*- coding: utf-8 -*-

# Review Heatmap Add-on for Anki
#
# Copyright (C) 2016-2020  Aristotelis P. <https//glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the accompanied license file.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License which
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

"""
Options dialog and associated components
"""


from aqt import mw
from aqt.qt import *
from aqt.utils import openLink

from ..config import config
from ..libaddon.anki import ANKI
from ..libaddon.gui.dialogs.options import OptionsDialog
from .forms.anki21 import options as qtform_options


class AnkingOptions(OptionsDialog):
    # base class for option dialogs which:
    # - is based on libaddon.gui.dialogs.options.OptionsDialog (maps widgets to config data)
    # - sets up click events for link buttons (anking, youtube, ...)
    # - has class methods for adding the dialog to the the Anking menu (with some settings)
    # - adjusts the ui (in _setupUI)

    def __init__(self, config, mw, parent=None, **kwargs):
        # Mediator methods defined in mapped_widgets might need access to
        # certain instance attributes. As super().__init__ calls these
        # mediator methods it is important that we set the attributes
        # beforehand:
        self.parent = parent or mw
        self.mw = mw
        super(AnkingOptions, self).__init__(
            self.mapped_widgets,
            config,
            form_module=qtform_options,
            parent=self.parent,
            **kwargs
        )
        # Instance methods that modify the initialized UI should either be
        # called from self._setupUI or from here

    def _setupUI(self):
        super(AnkingOptions, self)._setupUI()

        # manually adjust title label font sizes on Windows
        # gap between default windows font sizes and sizes that work well
        # on Linux and macOS is simply too big
        # TODO: find a better solution
        if ANKI.PLATFORM == "win":
            default_size = QApplication.font().pointSize()
            for label in [self.form.fmtLabContrib, self.form.labHeading]:
                font = label.font()
                font.setPointSize(int(default_size * 1.5))
                label.setFont(font)

    def _setupEvents(self):
        f = self.form
        f.toolButton_website.clicked.connect(lambda _: self.openWeb("anking"))
        f.toolButton_youtube.clicked.connect(lambda _: self.openWeb("youtube"))
        f.toolButton_patreon.clicked.connect(lambda _: self.openWeb("patreon"))
        f.toolButton_palace.clicked.connect(lambda _: self.openWeb("palace"))
        f.toolButton_instagram.clicked.connect(
            lambda _: self.openWeb("instagram"))
        f.toolButton_facebook.clicked.connect(
            lambda _: self.openWeb("facebook"))

    def openWeb(self, site):
        if site == "anking":
            openLink('https://www.ankingmed.com')
        elif site == "youtube":
            openLink('https://www.youtube.com/theanking')
        elif site == "patreon":
            openLink('https://www.patreon.com/ankingmed')
        elif site == "instagram":
            openLink('https://instagram.com/ankingmed')
        elif site == "facebook":
            openLink('https://facebook.com/ankingmed')
        elif site == "video":
            openLink('https://youtu.be/5XAq0KpU3Jc')
        elif site == "palace":
            openLink(
                f'https://courses.ankipalace.com/?utm_source=anking_{self.addon_name_for_links}_add-on&utm_medium=anki_add-on&utm_campaign=mastery_course'
            )

    @classmethod
    def init(cls):

        def invoke_options_dialog(parent=None):
            dialog = cls(config, mw, parent=parent)
            return dialog.exec_()

        menu = cls._get_anking_menu()
        a = QAction(cls.action_label, mw)
        a.triggered.connect(invoke_options_dialog)
        menu.addAction(a)

    @classmethod
    def _create_get_help_submenu(cls, parent: QMenu) -> QMenu:
        submenu = QMenu(cls.submenu_name, parent)
        for name, url in cls.menu_options:
            act = QAction(name, mw)
            act.triggered.connect(lambda _, u=url: openLink(u))
            submenu.addAction(act)
        return submenu

    @classmethod
    def _maybe_add_get_help_submenu(cls, menu: QMenu) -> None:
        """Adds submenu in 'Anking' menu if needed.

        The submenu is added if:
        - The submenu does not exist in menu
        - The submenu is an outdated version - existing is deleted

        With versioning and anking_get_help property,
        future version can rename, hide, or change contents in the submenu
        """
        for act in menu.actions():
            if act.property(cls.submenu_property) or act.text() == submenu_name:
                ver = act.property("version")
                if ver and ver >= cls.submenu_ver:
                    return
                submenu = cls._create_get_help_submenu(menu)
                menu.insertMenu(act, submenu)
                menu.removeAction(act)
                act.deleteLater()
                new_act = submenu.menuAction()
                new_act.setProperty(cls.submenu_property, True)
                new_act.setProperty("version", cls.submenu_ver)
                return
        else:
            submenu = cls._create_get_help_submenu(menu)
            menu.addMenu(submenu)
            new_act = submenu.menuAction()
            new_act.setProperty(cls.submenu_property, True)
            new_act.setProperty("version", cls.submenu_ver)

    @classmethod
    def _get_anking_menu(cls) -> QMenu:
        """Return AnKing menu. If it doesn't exist, create one. Make sure its submenus are up to date."""
        menu_name = "&AnKing"
        menubar = mw.form.menubar
        for a in menubar.actions():
            if menu_name == a.text():
                menu = a.menu()
                break
        else:
            menu = menubar.addMenu(menu_name)
        cls._maybe_add_get_help_submenu(menu)
        return menu
