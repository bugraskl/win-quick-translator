"""Qt Style Sheets for the application."""

from config import COLORS

MAIN_STYLE = f"""
QWidget#MainWindow {{
    background-color: {COLORS['background']};
    border-radius: 12px;
}}

QLineEdit#SearchInput {{
    background-color: {COLORS['input_bg']};
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 16px;
    color: {COLORS['text']};
    selection-background-color: {COLORS['accent']};
}}

QLineEdit#SearchInput:focus {{
    background-color: {COLORS['input_bg']};
}}

QLineEdit#SearchInput::placeholder {{
    color: {COLORS['text_secondary']};
}}

QFrame#ResultFrame {{
    background-color: {COLORS['result_bg']};
    border-radius: 8px;
    padding: 8px;
}}

QLabel#TranslatedText {{
    color: {COLORS['text']};
    font-size: 15px;
    padding: 8px 12px;
}}

QLabel#SourceInfo {{
    color: {COLORS['text_secondary']};
    font-size: 12px;
    padding: 4px 12px;
}}

QLabel#GoogleIcon {{
    padding: 8px;
}}
"""
