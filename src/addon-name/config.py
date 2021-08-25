from aqt import mw

from .libaddon.addon import ADDON
from .libaddon.anki.config.manager import ConfigManager

__all__ = ["config"]


config_defaults = {
    "synced": {
        "loose_search": False,
        "active_note_type_field_ids": [],
        "version": ADDON.VERSION,
    },
    "profile":{
        "hotkeys":{
            "toggle": "Alt+Shift+A",
        },
        "version": ADDON.VERSION,
    },

}

config = ConfigManager(
    mw, config_dict=config_defaults, conf_key="field_autocomplete", reset_req=True
)
