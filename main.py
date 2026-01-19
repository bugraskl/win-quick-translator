"""Quick Translator - Main entry point."""

import sys
import threading
import keyboard
from PIL import Image, ImageDraw
import pystray

from window import TranslatorWindow
from config import COLORS, load_settings, get_config_path
from setup_wizard import SetupWizard


class QuickTranslator:
    """Main application class with system tray support."""
    
    def __init__(self, settings: dict):
        self.settings = settings
        self.hotkey = settings.get('hotkey', 'ctrl+space')
        self.window = TranslatorWindow()
        self.tray = None
        self.should_toggle = False
        
    def create_icon_image(self):
        """Create a simple translator icon."""
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw blue circle
        accent_color = tuple(int(COLORS['accent'][i:i+2], 16) for i in (1, 3, 5))
        draw.ellipse([4, 4, size-4, size-4], fill=accent_color)
        
        # Draw "T" letter
        draw.text((size//2 - 8, size//2 - 14), "T", fill='white')
        
        return image
        
    def on_tray_click(self, icon, item):
        """Handle tray menu click."""
        item_str = str(item)
        if "Göster" in item_str:
            self.should_toggle = True
        elif "Çıkış" in item_str:
            self.quit()
            
    def setup_tray(self):
        """Setup system tray icon."""
        icon_image = self.create_icon_image()
        hotkey_display = self.hotkey.upper().replace('+', ' + ')
        
        menu = pystray.Menu(
            pystray.MenuItem(f"Göster ({hotkey_display})", self.on_tray_click),
            pystray.MenuItem("Çıkış", self.on_tray_click)
        )
        
        self.tray = pystray.Icon(
            "quick_translator",
            icon_image,
            f"Quick Translator - {hotkey_display}",
            menu
        )
        
        tray_thread = threading.Thread(target=self.tray.run, daemon=True)
        tray_thread.start()
        
    def register_hotkey(self):
        """Register global hotkey."""
        keyboard.add_hotkey(self.hotkey, self.on_hotkey)
        
    def on_hotkey(self):
        """Handle hotkey press."""
        self.should_toggle = True
        
    def check_toggle(self):
        """Check if we should toggle the window."""
        if self.should_toggle:
            self.should_toggle = False
            self.window.toggle_window()
        self.window.root.after(100, self.check_toggle)
        
    def quit(self):
        """Quit the application."""
        keyboard.unhook_all_hotkeys()
        if self.tray:
            self.tray.stop()
        if self.window.root:
            self.window.root.quit()
        sys.exit(0)
        
    def run(self):
        """Run the application."""
        hotkey_display = self.hotkey.upper().replace('+', ' + ')
        print("=" * 50)
        print("  Quick Translator başlatıldı!")
        print("=" * 50)
        print(f"  Açmak için: {hotkey_display}")
        print("  Kapatmak için: ESC veya pencere dışına tıklayın")
        print("  Çıkmak için: System tray'den 'Çıkış' seçin")
        print("=" * 50)
        
        root = self.window.create_window()
        self.setup_tray()
        self.register_hotkey()
        root.after(100, self.check_toggle)
        root.mainloop()


def main():
    """Entry point."""
    # Check if first run (no config exists)
    config_path = get_config_path()
    
    if not config_path.exists():
        # Run setup wizard
        wizard = SetupWizard()
        settings = wizard.run()
        
        if settings is None:
            # User cancelled
            print("Kurulum iptal edildi.")
            sys.exit(0)
    else:
        settings = load_settings()
    
    # Start main application
    app = QuickTranslator(settings)
    app.run()


if __name__ == "__main__":
    main()
