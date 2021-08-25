
from .anking_options import AnkingOptions


class FieldACOptions(AnkingOptions):

    action_label = "Field Autocomplete"

    # Anking links submenu options
    submenu_name = "Get Anki Help"
    submenu_property = "anking_get_help"
    submenu_ver = 2
    addon_name_for_link = "autocomplete"
    menu_options = [
        (
            "Online Mastery Course",
            f'https://courses.ankipalace.com/?utm_source=anking_{addon_name_for_link}_add-on&utm_medium=anki_add-on&utm_campaign=mastery_course'
        ),
        ("Daily Q and A Support", "https://www.ankipalace.com/memberships"),
        ("1-on-1 Tutoring", "https://www.ankipalace.com/tutoring"),
    ]

    mapped_widgets = (
        ("form.checkBox_search_mode",
         (("value", {"dataPath": "synced/loose_search"}),)),
        ("form.keyGrabToggle",
         (("value", {"dataPath": "profile/hotkeys/toggle"}),)),
    )


    def __init__(self, config, mw, parent=None, **kwargs):
        super().__init__(config, mw, parent, **kwargs)
