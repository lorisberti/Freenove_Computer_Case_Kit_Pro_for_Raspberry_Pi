#!/usr/bin/env python3
import os
import sys
import stat
import shutil

def on_rm_error(func, path, exc_info):
    """Error handler for directory removal"""
    try:
        os.chmod(path, stat.S_IWUSR | stat.S_IRUSR)
        func(path)
    except Exception:
        pass

def create_shortcut():
    """Create desktop shortcut"""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    os.makedirs(desktop_dir, exist_ok=True)

    dest_file = os.path.join(desktop_dir, "MyRaspi.desktop")
    script_file = os.path.join(base_dir, "app_ui.py")
    python_exec = sys.executable or "/usr/bin/python3"

    if not os.path.exists(script_file):
        print(f"Error: target script not found: {script_file}")
        return 1

    # Build exec command with absolute paths
    exec_line = f'{python_exec} "{script_file}"'
    icon_path = os.path.join(base_dir, "icon.png")
    if not os.path.exists(icon_path):
        icon_path = ""

    # Create desktop entry content
    desktop_entry = [
        "[Desktop Entry]",
        "Type=Application",
        "Name=MyRaspi",
        "Comment= Case Controller for Raspberry Pi",
        f'Exec={exec_line}',
        f'Path={base_dir}',
        f'Icon={icon_path}' if icon_path else "Icon=",
        "Terminal=false",
        "Categories=Utility;",
        "StartupNotify=false",
    ]

    # Remove old desktop file if exists
    try:
        if os.path.exists(dest_file):
            os.remove(dest_file)
            print(f"Deleted existing desktop file: {dest_file}")
    except Exception as e:
        print(f"Warning: Could not delete existing file: {e}")

    # Write new .desktop file
    try:
        with open(dest_file, "w", encoding="utf-8") as f:
            f.write("\n".join(desktop_entry) + "\n")
        os.chmod(dest_file, 0o755)
        print("Created new desktop file on Desktop")
    except Exception as e:
        print(f"Error writing desktop file: {e}")
        return 1

    # Clean up __pycache__
    try:
        cache_dir = os.path.join(base_dir, "__pycache__")
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir, onerror=on_rm_error)
            print(f"Removed __pycache__ directory")
    except Exception as e:
        print(f"Warning: Could not remove __pycache__: {e}")

    return 0

if __name__ == "__main__":
    rc = create_shortcut()
    if rc == 0:
        print("Desktop shortcut created successfully!")
    sys.exit(rc)