"""Configuration settings for Quick Translator."""

import json
import os
from pathlib import Path

# Default settings
DEFAULTS = {
    "hotkey": "ctrl+space",
    "primary_language": "tr",  # User's primary language
    "window_width": 600,
    "window_height": 60,
}

# Colors (Dark Theme)
COLORS = {
    "background": "#2d2d2d",
    "input_bg": "#3d3d3d",
    "result_bg": "#383838",
    "text": "#ffffff",
    "text_secondary": "#a0a0a0",
    "accent": "#4285f4",  # Google Blue
    "border": "#4a4a4a",
}

# Config file path
def get_config_path() -> Path:
    """Get the config file path in AppData."""
    appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
    config_dir = Path(appdata) / 'QuickTranslator'
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / 'settings.json'

def load_settings() -> dict:
    """Load settings from config file."""
    config_path = get_config_path()
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                # Merge with defaults
                settings = DEFAULTS.copy()
                settings.update(saved)
                return settings
        except:
            pass
    
    return DEFAULTS.copy()

def save_settings(settings: dict):
    """Save settings to config file."""
    config_path = get_config_path()
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

# Load settings on import
SETTINGS = load_settings()

# Convenience accessors
HOTKEY = SETTINGS.get('hotkey', DEFAULTS['hotkey'])
PRIMARY_LANGUAGE = SETTINGS.get('primary_language', DEFAULTS['primary_language'])
WINDOW_WIDTH = SETTINGS.get('window_width', DEFAULTS['window_width'])
WINDOW_HEIGHT = SETTINGS.get('window_height', DEFAULTS['window_height'])
