# Quick Translator 🌐

![Quick Translator Interface](screenshots/1.png)

Fast, lightweight, and modern Windows translation app. macOS Spotlight-style interface that integrates seamlessly with your system.


## Features ✨

- 🚀 **Quick Access**: Open instantly with `CTRL+SPACE` (Customizable)
- 🧠 **Smart Translation**: 
  - If you type in your **Primary Language** (e.g. Turkish) → Translates to English
  - If you type in English (or other) → Translates to your Primary Language
- 🎨 **Modern Interface**: Windows 11 Acrylic Blur effect and rounded corners
- ⌨️ **Keyboard Friendly**: No mouse needed, just type and translate
- 🌗 **Dark Mode**: Stylish dark theme that's easy on the eyes
- 📌 **System Tray**: Runs quietly in the background, minimal resource usage

## Download & Install 📦

**[Download Latest Version (Releases)](https://github.com/bugraskl/win-quick-translator/releases)**

1. Download `QuickTranslatorSetup.exe`.
2. Complete the installation.
3. Select your **Primary Language** and **Hotkey** on first launch.

## Development & Building 🛠️

To develop the project on your own machine:

1. Clone the repository:
```bash
git clone https://github.com/bugraskl/win-quick-translator.git
cd win-quick-translator
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

### Building Exe & Installer

To create a single `.exe` file and installer:

1. Run `build.bat` (creates exe using PyInstaller).
2. Right-click `installer.iss` and select **Compile** (requires Inno Setup).
3. Output will be in the `installer_output/` folder.

## License 📄

MIT License
