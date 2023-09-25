"""
The collections of the tests for the 'utils.autostart.py' module.
"""
import winreg
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


@pytest.mark.parametrize('expected_result', (True, False))
@patch('winreg.QueryValueEx')
@patch('winreg.OpenKey')
def test_app_exists_in_autostart(mock_open_key: patch, mock_query_value_ex: patch, expected_result: bool):
    """
    Test if an application exists in the Windows Autostart configuration.

    Args:
        mock_open_key (patch): A mock object for winreg.OpenKey.
        mock_query_value_ex (patch): A mock object for winreg.QueryValueEx.
        expected_result (bool): The expected result of the check, True if the
            application exists, False if it does not.
    """
    mock_query_value_ex.return_value = expected_result
    result = autostart.check('app_name.py')

    assert result == expected_result


@patch('winreg.OpenKey', side_effect=FileNotFoundError)
def test_winreg_raise_error(mock_open_key: patch):
    """
    Test handling of an error when accessing the Windows Registry.

    Args:
        mock_open_key (patch): A mock object for winreg.OpenKey.
    """
    result = autostart.check('app_name.py')

    assert result is False
