"""
The collections of the tests for the 'utils.printer.py' module.
"""
from unittest.mock import patch

import pytest
import requests
from pytest import fixture, MonkeyPatch

from utils.exceptions import InvalidAddressError, CreateReportError, ReportError

from utils.printer import Device


class RequestsMock:
    """
    A mock class for simulating HTTP requests with customizable response status code and content.

    Attributes:
        status_code (int): The HTTP response status code.
        text (str): The content of the HTTP response.
    """
    def __init__(self):
        """
        Initialize the necessary attributes.
        """
        self.status_code = None
        self.text = None

    def set_status_code(self, code: int):
        """
        Set the HTTP response status code.

        Args:
            code (int): The HTTP status code to set.
          """
        self.status_code = code

    def get(self, *args, **kwargs):
        """
        Simulate an HTTP GET request.

        Returns:
            RequestsMock: An instance of RequestsMock with the specified status code and content.
        """
        if not self.status_code:
            self.status_code = 200

        with open('tests/example_report.html') as file:
            self.text = file.read()

        return self


@pytest.fixture(autouse=True)
def no_requests(monkeypatch: MonkeyPatch):
    """
    A Pytest fixture that monkeypatches the requests.get method to use the RequestsMock class.

    Args:
        monkeypatch: The Pytest monkeypatch fixture.
    """
    monkeypatch.setattr(requests, 'get', RequestsMock().get)


def test_use_device_as_context_manager(no_requests: fixture):
    """
    Test using the Device class as a context manager.

    Args:
        no_requests (fixture): Pytest fixture that mocks HTTP requests.
    """
    with Device('192.168.0.1') as device:
        pass
    assert isinstance(device, Device)
    assert device.ip_address == '192.168.0.1'


def test_context_manager_invalid_ip_address():
    """
    Test using the Device class as a context manager with an invalid IP address.

    Raises:
        InvalidAddressError: When an invalid IP address is used.
    """
    with pytest.raises(InvalidAddressError) as error, \
            Device('invalid_ip_address'):
        pass

    assert error.type == InvalidAddressError


@patch('utils.printer.Device.ip_address_is_valid', return_value=True)
@patch('utils.printer.Device.create_report')
def test_context_manager_valid_ip_address(mock_create_report: patch, mock_ip_valid: patch):
    """
    Test using the Device class as a context manager with a valid IP address.

    Args:
        mock_create_report (patch): Pytest mock for the create_report method.
        mock_ip_valid (patch): Pytest mock for the ip_address_is_valid method.
    """
    with Device('192.168.0.1'):
        pass

    mock_create_report.assert_called_once()
    mock_ip_valid.assert_called_once_with()


@pytest.mark.parametrize(
    'ip, expected_result', (
            ('192.168.0.1', True),
            ('1.1.1.1', True),
            ('192.168.0.1a', False),
            ('invalid', False),
    )
)
def test_ip_address_validator(ip: str, expected_result: bool):
    """
    Test the IP address validator function.

    Args:
        ip (str): The IP address to validate.
        expected_result (bool): The expected validation result.
    """
    result = Device(ip).ip_address_is_valid()

    assert result is expected_result


def test_successfully_create_report():
    """
    Test the successful creation of a report.
    """
    with open('tests/example_report.html') as file:
        expected_result = file.read()

    device = Device('127.0.0.1')

    assert device._report is None

    device.create_report()

    assert device._report == expected_result


def test_unsuccessfully_create_report(monkeypatch: MonkeyPatch):
    """
    Test the unsuccessful creation of a report.

    It simulates a failed HTTP request and expects a CreateReportError to be raised.

    Args:
        monkeypatch: The Pytest monkeypatch fixture.
    """
    mock_requests = RequestsMock()
    mock_requests.set_status_code(403)
    monkeypatch.setattr(requests, 'get', mock_requests.get)

    with pytest.raises(CreateReportError) as error:
        Device('127.0.0.1').create_report()

    assert error.type == CreateReportError


def test_successfully_get_counter():
    """
    Test successfully getting the counter value from a Device.
    """
    with Device('10.0.0.1') as device:
        printer_counter = device.get_counter()

    assert printer_counter == '113013'


def test_successfully_get_serial_number():
    """
    Test successfully getting the serial number from a Device.
    """
    with Device('10.0.0.1') as device:
        printer_serial_number = device.get_serial_number()

    assert printer_serial_number == '701545HH0NLT2'


def test_unsuccessfully_get_counter():
    """
    Test unsuccessfully getting the counter value from a Device.
    """
    device = Device('127.2.2.2')

    with pytest.raises(ReportError) as error:
        device.get_counter()

    assert error.type == ReportError


def test_unsuccessfully_get_serial_number():
    """
    Test unsuccessfully getting the serial number from a Device.
    """
    device = Device('0.0.0.0')

    with pytest.raises(ReportError) as error:
        device.get_serial_number()

    assert error.type == ReportError
