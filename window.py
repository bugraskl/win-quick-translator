"""Main window for Quick Translator using Tkinter with Modern UI."""

import tkinter as tk
import threading
import ctypes
from ctypes import windll, byref, c_int, c_bool
from translator import TranslationService
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, PRIMARY_LANGUAGE

# Windows API Constants
ACCENT_ENABLE_BLURBEHIND = 3
ACCENT_ENABLE_ACRYLICBLURBEHIND = 4
hwnd = None

class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ('AccentState', ctypes.c_int),
        ('AccentFlags', ctypes.c_int),
        ('GradientColor', ctypes.c_int),
        ('AnimationId', ctypes.c_int)
    ]

class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ('Attribute', ctypes.c_int),
        ('Data', ctypes.POINTER(ACCENT_POLICY)),
        ('SizeOfData', ctypes.c_int)
    ]

def apply_acrylic(hwnd, color=0x2d2d2d): # ABGR format usually, but here just hex
    # Enable Acrylic Blur
    policy = ACCENT_POLICY()
    policy.AccentState = ACCENT_ENABLE_ACRYLICBLURBEHIND
    policy.GradientColor = (150 << 24) | (0x2d2d2d & 0xFFFFFF)  # Alpha << 24 | BGR
    # Note: Tkinter colors are RGB, Windows expects BGR for some APIs, 
    # but SetWindowCompositionAttribute GradientColor is AABBGGRR usually.
    # Let's try simple blur first if acrylic is complex to tune color match
    
    # Actually, for just "blur background", let's use BLURBEHIND which is safer
    policy.AccentState = ACCENT_ENABLE_BLURBEHIND
    policy.GradientColor = 0
    
    data = WINDOWCOMPOSITIONATTRIBDATA()
    data.Attribute = 19 # WCA_ACCENT_POLICY
    data.Data = ctypes.pointer(policy)
    data.SizeOfData = ctypes.sizeof(policy)
    
    windll.user32.SetWindowCompositionAttribute(hwnd, byref(data))

def set_rounded_corners(hwnd):
    # DWMWA_WINDOW_CORNER_PREFERENCE = 33
    # DWMWCP_ROUND = 2
    try:
        DwmSetWindowAttribute = windll.dwmapi.DwmSetWindowAttribute
        DwmSetWindowAttribute(hwnd, 33, byref(c_int(2)), 4)
    except:
        pass # Not Windows 11

def force_foreground(hwnd):
    """Force focus to window using Windows API."""
    try:
        # AllowSetForegroundWindow
        windll.user32.AllowSetForegroundWindow(windll.kernel32.GetCurrentProcessId())
        
        # AttachThreadInput
        current_thread = windll.kernel32.GetCurrentThreadId()
        foreground_thread = windll.user32.GetWindowThreadProcessId(windll.user32.GetForegroundWindow(), None)
        
        if current_thread != foreground_thread:
            windll.user32.AttachThreadInput(foreground_thread, current_thread, True)
            windll.user32.SetForegroundWindow(hwnd)
            windll.user32.AttachThreadInput(foreground_thread, current_thread, False)
        else:
            windll.user32.SetForegroundWindow(hwnd)
    except:
        pass


class TranslatorWindow:
    """Main translator window - frameless, dark theme with modern effects."""
    
    def __init__(self):
        self.translator = TranslationService(PRIMARY_LANGUAGE)
        self.typing_timer = None
        self.root = None
        self.is_visible = False
        self.hwnd = None
        self.bg_color = COLORS['background']
        self.copy_button = None
        
    def create_window(self):
        """Create the main window."""
        self.root = tk.Tk()
        self.root.title("Quick Translator")
        
        # Frameless window
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.0) # Start invisible for animation
        
        # Set background color
        self.root.configure(bg=self.bg_color)
        
        # Window size and position (centered)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x = (self.screen_width - WINDOW_WIDTH) // 2
        y = self.screen_height // 3
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=12, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input container
        input_container = tk.Frame(main_frame, bg=COLORS['input_bg'], highlightthickness=1,
                                   highlightbackground=COLORS['border'])
        input_container.pack(fill=tk.X, padx=4)
        
        # Search input
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_text_changed)
        
        self.search_input = tk.Entry(
            input_container,
            textvariable=self.search_var,
            font=('Segoe UI', 14),
            bg=COLORS['input_bg'],
            fg=COLORS['text'],
            insertbackground=COLORS['text'],
            relief=tk.FLAT,
            highlightthickness=0,
            bd=0,
        )
        self.search_input.pack(fill=tk.X, ipady=10, padx=12, pady=2)
        
        # Result frame
        self.result_frame = tk.Frame(main_frame, bg=COLORS['result_bg'])
        
        # Result content
        result_content = tk.Frame(self.result_frame, bg=COLORS['result_bg'])
        result_content.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
        # Result row
        result_row = tk.Frame(result_content, bg=COLORS['result_bg'])
        result_row.pack(fill=tk.X)
        
        # Google icon removed as per request
        # self.google_label = tk.Label(...)

        # Copy button
        self.copy_button = tk.Label(
            result_row,
            text="📋",
            font=('Segoe UI', 12),
            fg=COLORS['text_secondary'],
            bg=COLORS['result_bg'],
            cursor="hand2"
        )
        self.copy_button.pack(side=tk.RIGHT, padx=5)
        self.copy_button.bind('<Button-1>', lambda e: self.copy_to_clipboard())
        
        # Translated text
        self.translated_label = tk.Label(
            result_row,
            text="",
            font=('Segoe UI', 14),
            fg=COLORS['text'],
            bg=COLORS['result_bg'],
            anchor='w',
            justify='left',
            wraplength=WINDOW_WIDTH - 120,
        )
        self.translated_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Source info
        self.source_info = tk.Label(
            result_content,
            text="",
            font=('Segoe UI', 10),
            fg=COLORS['text_secondary'],
            bg=COLORS['result_bg'],
            anchor='w',
        )
        self.source_info.pack(fill=tk.X, pady=(6, 0))
        
        # Bind keys
        self.root.bind('<Escape>', lambda e: self.hide_window())
        self.root.bind('<FocusOut>', self.on_focus_out)
        self.search_input.bind('<Return>', lambda e: self.perform_translation())
        
        # Get HWND for Windows API calls
        self.root.update_idletasks()
        self.hwnd = windll.user32.GetParent(self.root.winfo_id())
        
        # Apply Windows effects
        apply_acrylic(self.hwnd)
        set_rounded_corners(self.hwnd)
        
        # Start hidden
        self.root.withdraw()
        self.is_visible = False
        
        return self.root
        
    def on_text_changed(self, *args):
        """Handle text input changes with debounce."""
        if self.typing_timer:
            self.root.after_cancel(self.typing_timer)
            
        text = self.search_var.get().strip()
        if text:
            self.typing_timer = self.root.after(400, self.perform_translation)
        else:
            self.result_frame.pack_forget()
            self.adjust_height(False)
            
    def perform_translation(self):
        """Perform the translation."""
        text = self.search_var.get().strip()
        if not text:
            return
            
        def translate():
            result = self.translator.translate(text)
            self.root.after(0, lambda: self.show_result(result))
            
        threading.Thread(target=translate, daemon=True).start()
        
    def show_result(self, result):
        """Show translation result."""
        if result['success']:
            self.translated_label.config(text=result['translated'])
            
            source_name = self.translator.get_language_name(result['source_lang'])
            target_name = self.translator.get_language_name(result['target_lang'])
            self.source_info.config(text=f"{source_name} → {target_name}")
        else:
            self.translated_label.config(text="Çeviri yapılamadı")
            self.source_info.config(text=result.get('error', 'Bilinmeyen hata'))
            
        self.result_frame.pack(fill=tk.X, pady=(10, 0), padx=4)
        self.adjust_height(True)

    def copy_to_clipboard(self):
        """Copy translated text to clipboard."""
        text = self.translated_label.cget("text")
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            # Visual feedback
            orig_color = self.copy_button.cget("fg")
            self.copy_button.config(fg="#ffffff")
            self.root.after(200, lambda: self.copy_button.config(fg=orig_color))

    def adjust_height(self, with_result: bool):
        """Adjust window height based on content."""
        if with_result:
            self.root.update_idletasks()
            # Calculate required height based on content
            # Input area is roughly 60px
            # Result frame height comes from its content
            # Add extra padding (80px) to ensure source info is visible
            required_height = 90 + self.result_frame.winfo_reqheight()
            new_height = max(160, required_height)
        else:
            new_height = WINDOW_HEIGHT
            
        geo = self.root.geometry()
        parts = geo.split('+')
        x, y = parts[1], parts[2]
        self.root.geometry(f"{WINDOW_WIDTH}x{new_height}+{x}+{y}")
        
    def animate_open(self):
        """Fade in animation."""
        alpha = 0.0
        self.root.attributes('-alpha', alpha)
        self.root.deiconify()
        
        def fade():
            nonlocal alpha
            alpha += 0.15
            if alpha >= 0.95:
                self.root.attributes('-alpha', 0.95)
                # Ensure focus after animation
                force_foreground(self.hwnd)
                self.search_input.focus_force()
            else:
                self.root.attributes('-alpha', alpha)
                self.root.after(10, fade)
                
        fade()
        
    def show_window(self):
        """Show the window centered on screen."""
        self.search_var.set("")
        self.result_frame.pack_forget()
        
        # Reset position
        x = (self.screen_width - WINDOW_WIDTH) // 2
        y = self.screen_height // 3
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        
        self.is_visible = True
        self.animate_open()
        
        # Force focus immediately too
        force_foreground(self.hwnd)
        self.search_input.focus_force()
        self.search_input.selection_range(0, tk.END)
        
    def hide_window(self):
        """Hide the window."""
        self.root.withdraw()
        self.is_visible = False
        
    def on_focus_out(self, event):
        """Hide window when focus is lost."""
        self.root.after(100, self.check_focus)
        
    def check_focus(self):
        """Check if window should be hidden."""
        try:
            # Get foreground window to see if it's us
            fg_hwnd = windll.user32.GetForegroundWindow()
            if fg_hwnd != self.hwnd and self.is_visible:
                 self.hide_window()
        except:
            pass
            
    def toggle_window(self):
        """Toggle window visibility."""
        if self.is_visible:
            self.hide_window()
        else:
            self.show_window()
