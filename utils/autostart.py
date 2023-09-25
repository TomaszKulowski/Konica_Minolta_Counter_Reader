"""
This script provides utility functions to interact with the Windows Registry
for managing applications in the startup list. It includes functions to add
an application to the startup list and check if an application is in the startup list.
"""

from pathlib import Path
import winreg

from .exceptions import AddAutostartError


def add(app_path: Path):
    """
    Add the application to the Windows Registry startup list.

    Args:
        app_path (Path): The path to the application's file.
    """
    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_WRITE
        )
        winreg.SetValueEx(registry_key, app_path.name, 1, winreg.REG_SZ, f'Python "{app_path}"')
        winreg.CloseKey(registry_key)

    except WindowsError:
        winreg.CloseKey(registry_key)
        raise AddAutostartError


def check(app_name: str) -> bool:
    """
    Check if the application is in the Windows Registry startup list.

    Args:
        app_name (str): The name of the application to check for in the startup list.

    Returns:
        bool: True if the application is in the startup list, False otherwise.
    """
    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        return bool(winreg.QueryValueEx(registry_key, app_name))

    except FileNotFoundError:
        return False
