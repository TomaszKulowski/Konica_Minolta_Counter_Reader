"""
The collections of the tests for the 'utils.autostart.py' module.
"""

from pathlib import Path
from unittest.mock import patch

import pytest

from utils import autostart
from utils.exceptions import AddAutostartError


@patch('winreg.OpenKey')
@patch('winreg.SetValueEx')
@patch('winreg.CloseKey')
def test_add_successful(mock_open_key: patch, mock_set_value_ex: patch, mock_close_key: patch):
    """
    Test the successful addition of an Autostart entry.

    Args:
        mock_open_key (patch): A mock object for winreg.OpenKey.
        mock_set_value_ex (patch): A mock object for winreg.SetValueEx.
        mock_close_key (patch): A mock object for winreg.CloseKey.

    Raises:
        AssertionError: If any of the expected function calls are not made.
    """
    autostart.add(Path('main.py'))

    mock_open_key.assert_called_once()
    mock_set_value_ex.assert_called_once()
    mock_close_key.assert_called_once()


@patch('winreg.OpenKey')
@patch('winreg.SetValueEx', side_effect=WindowsError)
@patch('winreg.CloseKey')
def test_add_unsuccessful(mock_open_key: patch, mock_set_value_ex: patch, mock_close_key: patch):
    """
    Test the unsuccessful addition of an Autostart entry.

    Args:
        mock_open_key (patch): A mock object for winreg.OpenKey.
        mock_set_value_ex (patch): A mock object for winreg.SetValueEx.
        mock_close_key (patch): A mock object for winreg.CloseKey.

    Raises:
        AssertionError: If any of the expected function calls are not made,
            or if the wrong exception is raised.
    """
    with pytest.raises(AddAutostartError) as error:
        autostart.add(Path('main.py'))

    assert error.type == AddAutostartError
    mock_open_key.assert_called_once()
    mock_set_value_ex.assert_called_once()
    mock_close_key.assert_called_once()
