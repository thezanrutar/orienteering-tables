# Troubleshooting Guide

## Application Not Working?

If you encounter issues running the application, follow these steps:

### 1. Check Python Version

```bash
python3 --version
```

Required: Python 3.8 or higher

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or directly:

```bash
pip install PySide6
```

### 3. Install System Libraries (Linux only)

On Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y libegl1 libgl1 libxkbcommon0 libxcb-icccm4 libxcb-image0 \
    libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 \
    libxcb-xinerama0 libxcb-xfixes0 libxcb-cursor0
```

### 4. Run the Application

```bash
cd src
python3 main.py
```

Or from the project root:

```bash
python3 src/main.py
```

## Common Issues

### ModuleNotFoundError: No module named 'PySide6'

**Solution:** Install PySide6:
```bash
pip install PySide6
```

### ImportError: libEGL.so.1: cannot open shared object file

**Solution:** Install system libraries (Linux):
```bash
sudo apt-get install -y libegl1 libgl1
```

### Application Window Not Showing

**Possible causes:**
1. Running in a headless environment (no display server)
2. Display server not accessible

**Solution:** Ensure you have a working display server (X11, Wayland) or use a virtual display.

### Database Errors

The database file (`orienteering.db`) is created automatically in the project root directory. If you encounter database errors:

1. Delete the database file: `rm orienteering.db`
2. Restart the application (it will recreate the database)

## Verification

To verify the application is working correctly, run:

```bash
python3 src/main.py
```

You should see:
- "Database initialized successfully" message
- Application window opens with dark theme
- Competition grid is visible
- You can click "+" to create a new competition

## Still Having Issues?

If the problem persists:

1. Check that all dependencies are installed: `pip list | grep PySide6`
2. Verify Python version: `python3 --version` (must be 3.8+)
3. Try running in verbose mode to see error messages
4. Check the console output for any error messages

## Test the Application

You can verify the application works by running a test:

```python
# test_app.py
import sys
import os
sys.path.insert(0, 'src')
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PySide6 import QtWidgets
import database

# Test database
database.init_db()
comp_id = database.insert_competition('2025-07-19', 'Oslo, Norway', ['A', 'B'], {'A': 45, 'B': 60})
print(f"✓ Competition created with ID: {comp_id}")

# Test GUI
app = QtWidgets.QApplication([])
from main_window import MainWindow
window = MainWindow()
print("✓ Application working correctly!")
```

Run with:
```bash
python3 test_app.py
```
