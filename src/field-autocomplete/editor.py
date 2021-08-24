import json

from aqt import editor, gui_hooks

from .config import get
from .user_config import getUserOption


def setup_ac(editor):
    note_type = editor.note.note_type()

    enabled_field_ords = []
    for fld in note_type['flds']:
        id = f'{note_type["id"]} {fld["name"]}'
        enabled = get(id)
        if enabled:
            enabled_field_ords += [fld['ord']]

    data = {
        "ords" : enabled_field_ords,
        "looseSearch" : getUserOption('loose_search', refresh=True)
    }
    editor.web.eval(f'Autocomplete.setup({json.dumps(data)})')


def add_ac_toggle_shortcut(shortcuts, editor: editor.Editor):
    shortcuts.append((
        getUserOption('toggle_ac_shortcut', refresh=True),
        lambda: editor.web.eval(f'Autocomplete.toggleAc({editor.currentField})')
    ))


def init_editor():
    gui_hooks.editor_did_load_note.append(setup_ac)
    gui_hooks.editor_did_init_shortcuts.append(add_ac_toggle_shortcut)
