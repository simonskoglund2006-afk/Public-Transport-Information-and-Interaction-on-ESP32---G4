import json

SETTINGS_FILE = 'settings.json'

def load_settings(stop_count, type_count):
    'Restores stop_index and type_index from flash or just (0,0) if nothing is saved'
    try:
        with open(SETTINGS_FILE) as file:
            data = json.load(file)
        stop = data['stop']
        kind = data['type']
        if 0 <= stop < stop_count and 0 <= kind < type_count:
            return stop, kind
    except (OSError, ValueError, KeyError, TypeError):
        pass
    return (0,0)

def save(stop_index, type_index):
    'Write the selection to flash. Return True on success and False on failure'
    try:
        with open(SETTINGS_FILE, 'w') as file:
            json.dump({'stop': stop_index, 'type': type_index}, file)
            return True
    except OSError:
        return False

    