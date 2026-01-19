"""Setup wizard for first-time configuration."""

import tkinter as tk
from tkinter import ttk
from config import COLORS, save_settings, DEFAULTS


class SetupWizard:
    """Setup wizard for initial configuration."""
    
    LANGUAGES = [
        ('Türkçe', 'tr'),
        ('English', 'en'),
        ('Deutsch', 'de'),
        ('Français', 'fr'),
        ('Español', 'es'),
        ('Italiano', 'it'),
        ('Русский', 'ru'),
        ('日本語', 'ja'),
        ('한국어', 'ko'),
        ('中文', 'zh-cn'),
    ]
    
    HOTKEY_OPTIONS = [
        ('Ctrl + Space', 'ctrl+space'),
        ('Ctrl + Shift + T', 'ctrl+shift+t'),
        ('Alt + T', 'alt+t'),
        ('Ctrl + Alt + T', 'ctrl+alt+t'),
        ('Ctrl + Q', 'ctrl+q'),
    ]
    
    def __init__(self):
        self.root = None
        self.result = None
        self.selected_language = None
        self.selected_hotkey = None
        
    def run(self) -> dict:
        """Run the setup wizard and return settings."""
        self.root = tk.Tk()
        self.selected_language = tk.StringVar(value='tr')
        self.selected_hotkey = tk.StringVar(value='ctrl+space')

        self.root.title("Quick Translator - Kurulum")
        self.root.configure(bg=COLORS['background'])
        self.root.resizable(True, True)
        
        # Window size and center
        width, height = 500, 550
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=COLORS['background'], padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🌐 Quick Translator",
            font=('Segoe UI', 20, 'bold'),
            fg=COLORS['text'],
            bg=COLORS['background'],
        )
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Hızlı çeviri uygulaması",
            font=('Segoe UI', 11),
            fg=COLORS['text_secondary'],
            bg=COLORS['background'],
        )
        subtitle_label.pack(pady=(0, 25))
        
        # Language selection
        lang_label = tk.Label(
            main_frame,
            text="Ana Diliniz:",
            font=('Segoe UI', 12),
            fg=COLORS['text'],
            bg=COLORS['background'],
            anchor='w',
        )
        lang_label.pack(fill=tk.X, pady=(0, 8))
        
        lang_frame = tk.Frame(main_frame, bg=COLORS['background'])
        lang_frame.pack(fill=tk.X, pady=(0, 20))
        
        for i, (name, code) in enumerate(self.LANGUAGES):
            rb = tk.Radiobutton(
                lang_frame,
                text=name,
                variable=self.selected_language,
                value=code,
                font=('Segoe UI', 10),
                fg=COLORS['text'],
                bg=COLORS['background'],
                selectcolor=COLORS['input_bg'],
                activebackground=COLORS['background'],
                activeforeground=COLORS['text'],
            )
            rb.grid(row=i // 5, column=i % 5, sticky='w', padx=5, pady=2)
        
        # Hotkey selection
        hotkey_label = tk.Label(
            main_frame,
            text="Açılış Kısayolu:",
            font=('Segoe UI', 12),
            fg=COLORS['text'],
            bg=COLORS['background'],
            anchor='w',
        )
        hotkey_label.pack(fill=tk.X, pady=(10, 8))
        
        hotkey_frame = tk.Frame(main_frame, bg=COLORS['background'])
        hotkey_frame.pack(fill=tk.X, pady=(0, 25))
        
        for i, (name, key) in enumerate(self.HOTKEY_OPTIONS):
            rb = tk.Radiobutton(
                hotkey_frame,
                text=name,
                variable=self.selected_hotkey,
                value=key,
                font=('Segoe UI', 10),
                fg=COLORS['text'],
                bg=COLORS['background'],
                selectcolor=COLORS['input_bg'],
                activebackground=COLORS['background'],
                activeforeground=COLORS['text'],
            )
            rb.grid(row=i // 3, column=i % 3, sticky='w', padx=5, pady=2)
        
        # Info label
        info_label = tk.Label(
            main_frame,
            text="✓ Arka planda çalışır\n✓ System tray'de görünür\n✓ Windows başlangıcında açılır",
            font=('Segoe UI', 10),
            fg=COLORS['text_secondary'],
            bg=COLORS['background'],
            justify='left',
        )
        info_label.pack(fill=tk.X, pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=COLORS['background'])
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Start button
        start_btn = tk.Button(
            button_frame,
            text="Başlat",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg=COLORS['accent'],
            activebackground='#3367d6',
            activeforeground='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.on_start,
            padx=30,
            pady=8,
        )
        start_btn.pack(side=tk.RIGHT)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="İptal",
            font=('Segoe UI', 11),
            fg=COLORS['text'],
            bg=COLORS['input_bg'],
            activebackground=COLORS['border'],
            activeforeground=COLORS['text'],
            relief=tk.FLAT,
            cursor='hand2',
            command=self.on_cancel,
            padx=20,
            pady=8,
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        self.root.mainloop()
        return self.result
        
    def on_start(self):
        """Handle start button click."""
        settings = DEFAULTS.copy()
        settings['primary_language'] = self.selected_language.get()
        settings['hotkey'] = self.selected_hotkey.get()
        
        # Save settings
        save_settings(settings)
        
        self.result = settings
        self.root.destroy()
        
    def on_cancel(self):
        """Handle cancel button click."""
        self.result = None
        self.root.destroy()


def run_setup_if_needed() -> dict:
    """Run setup wizard if no settings exist, otherwise load existing."""
    from config import get_config_path, load_settings
    
    config_path = get_config_path()
    if not config_path.exists():
        wizard = SetupWizard()
        return wizard.run()
    else:
        return load_settings()
