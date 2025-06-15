import os
import json
import platform

def get_config_path():
    system = platform.system().lower()
    if system == 'windows':
        config_dir = os.path.join(os.getenv('APPDATA'), 'entracte')
    else:
        config_dir = os.path.join(os.path.expanduser("~"), ".config", "glint")
    
    return os.path.join(config_dir, "glint.json")

CONFIG_PATH = get_config_path()

def ensure_config_exists():
    default_config = {
        "engine": "",
    }
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        write_timer_config(default_config)

def read_timer_config():
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        ensure_config_exists()
        return read_timer_config()

def write_timer_config(config):
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)