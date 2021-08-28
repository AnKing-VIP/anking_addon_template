from aqt import mw
from aqt.qt import *
from aqt.utils import openLink

from ..config import config
from ..libaddon.anki import ANKI
from ..libaddon.gui.dialogs.options import OptionsDialog


from .anking_icons import AnkingIconsHeader
from .forms.anki21 import options as qtform_options


class FieldACOptions(OptionsDialog):
    addon_name_for_links = "autocomplete"
    mapped_widgets = (
        ("form.checkBox_search_mode",
         (("value", {"dataPath": "synced/loose_search"}),)),
        ("form.keyGrabToggle",
         (("value", {"dataPath": "profile/hotkeys/toggle"}),)),
    )

    def __init__(self, parent=None, **kwargs):
        self.parent = parent or mw
        self.mw = mw
        super().__init__(self.mapped_widgets, config,
                         form_module=qtform_options, parent=self.parent, **kwargs)

    def _setupUI(self):
        super()._setupUI()

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

        self.anking_icons = AnkingIconsHeader(self.form.AnkingHeader)

    def _setupEvents(self):
        f = self.form
        f.toolButton_palace.clicked.connect(lambda _: self.openPalaceLink)

    def openPalaceLink(self):
        openLink(
            f'https://courses.ankipalace.com/?utm_source=anking_{self.addon_name_for_links}_add-on&utm_medium=anki_add-on&utm_campaign=mastery_course'
        )
