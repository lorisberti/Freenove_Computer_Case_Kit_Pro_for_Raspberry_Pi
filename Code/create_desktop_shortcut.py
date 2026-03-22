#!/usr/bin/env python3

import os
import sys

def update_desktop_file():
    """
    Directly create desktop shortcut file on user desktop and autostart.
    """
    try:
        # Get the directory where the current script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Current directory: {current_dir}")
        
        # Build new execution path - run the shell script
        run_script_path = os.path.join(current_dir, "run_app.sh")
        if not os.path.exists(run_script_path):
            raise FileNotFoundError(f"Script file {run_script_path} does not exist")

        icon_path = os.path.join(current_dir, "Freenove_Logo.xpm")
        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"Icon file {icon_path} does not exist")
        
        # Get home directory path and build target paths
        try:
            username = os.getlogin()
            home_dir = os.path.expanduser(f"~{username}")
        except Exception:
            # If getting username fails, use default pi user
            home_dir = "/home/pi"
            print("Warning: Unable to get current username, using default path /home/pi")
        
        desktop_dir = os.path.join(home_dir, "Desktop")
        autostart_dir = os.path.join(home_dir, ".config", "autostart")
        
        # Ensure desktop directory exists
        if not os.path.exists(desktop_dir):
            try:
                os.makedirs(desktop_dir, mode=0o755, exist_ok=True)
                print(f"Created desktop directory: {desktop_dir}")
            except Exception as e:
                raise Exception(f"Failed to create desktop directory: {e}")
        
        # Ensure autostart directory exists
        if not os.path.exists(autostart_dir):
            try:
                os.makedirs(autostart_dir, mode=0o755, exist_ok=True)
                print(f"Created autostart directory: {autostart_dir}")
            except Exception as e:
                raise Exception(f"Failed to create autostart directory: {e}")
        
        # Check if desktop directory is valid and writable
        if not os.path.isdir(desktop_dir):
            raise Exception(f"Desktop directory {desktop_dir} is not a valid directory")
        
        if not os.access(desktop_dir, os.W_OK):
            raise Exception(f"Desktop directory {desktop_dir} does not have write permission")
        
        # Check if autostart directory is valid and writable
        if not os.path.isdir(autostart_dir):
            raise Exception(f"Autostart directory {autostart_dir} is not a valid directory")
        
        if not os.access(autostart_dir, os.W_OK):
            raise Exception(f"Autostart directory {autostart_dir} does not have write permission")
        
        # Build destination file paths
        desktop_path = os.path.join(desktop_dir, "My_Raspi.desktop")
        autostart_path = os.path.join(autostart_dir, "My_Raspi.desktop")
        
        # If desktop file exists, delete it
        if os.path.exists(desktop_path):
            try:
                os.remove(desktop_path)
                print(f"Deleted existing desktop file: {desktop_path}")
            except Exception as e:
                raise Exception(f"Failed to delete existing desktop file: {e}")
        
        # If autostart file exists, delete it
        if os.path.exists(autostart_path):
            try:
                os.remove(autostart_path)
                print(f"Deleted existing autostart file: {autostart_path}")
            except Exception as e:
                raise Exception(f"Failed to delete existing autostart file: {e}")

        # Create desktop file content for desktop
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=My_Raspi
Comment=My_Raspi Case Kit for Raspberry Pi
Exec=bash {run_script_path}
Icon={icon_path}
Terminal=false
Categories=Application;Development;
"""
        
        # Create desktop file content for autostart
        autostart_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=My_Raspi autostart
Comment=My_Raspi Case Kit for Raspberry Pi
Exec=bash {run_script_path}
Icon={icon_path}
Terminal=false
Categories=Application;Development;
X-GNOME-Autostart-enabled=true
"""
        
        # Write desktop file to desktop
        try:
            with open(desktop_path, 'w', encoding='utf-8') as f:
                f.write(desktop_content)
            print("Created new desktop file in ~/Desktop")
        except Exception as e:
            raise Exception(f"Error creating desktop file: {e}")
        
        # Write desktop file to autostart
        try:
            with open(autostart_path, 'w', encoding='utf-8') as f:
                f.write(autostart_content)
            print("Created new autostart file in ~/.config/autostart")
        except Exception as e:
            raise Exception(f"Error creating autostart file: {e}")
        
        # Set files as executable
        try:
            os.chmod(desktop_path, 0o755)
            os.chmod(autostart_path, 0o755)
            # Also make the run_app.sh script executable
            os.chmod(run_script_path, 0o755)
            print("Desktop and autostart files set as executable")
        except Exception as e:
            raise Exception(f"Error setting file permissions: {e}")
        
        # Remove __pycache__ folder if it exists
        pycache_path = os.path.join(current_dir, "__pycache__")
        if os.path.exists(pycache_path) and os.path.isdir(pycache_path):
            try:
                # Recursively remove __pycache__ directory and its contents using os module
                for root, dirs, files in os.walk(pycache_path, topdown=False):
                    for file in files:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        os.rmdir(dir_path)
                os.rmdir(pycache_path)
            except Exception as e:
                print(f"Warning: Failed to remove __pycache__ folder: {e}")
                
        return True
            
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        return False
    except PermissionError as e:
        print(f"Permission error: {e}")
        return False
    except Exception as e:
        print(f"Operation failed: {e}")
        return False

if __name__ == "__main__":
    success = update_desktop_file()
    if success:
        print("Desktop and autostart shortcuts created successfully!")
        sys.exit(0)
    else:
        print("Shortcut creation failed!")
        sys.exit(1)