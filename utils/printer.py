"""
This Python script provides a utility class, 'Device,' for interacting with a networked device
to retrieve printer statistics. It allows users to check various statistics such as counters
and serial numbers from a networked printer.
"""

import ipaddress

import requests
from bs4 import BeautifulSoup

from .exceptions import InvalidAddressError, ReportError, CreateReportError


class Device:
    """
    A utility class for interacting with a networked device to retrieve printer statistics.

    Attributes:
        ip_address (str): The IP address of the networked device.

    Methods:
        ip_address_is_valid():
            Check if the provided IP address is valid.

        create_report():
            Fetch the device statistics report from the device's web interface.

        get_counter():
            Get the current counter value from the device statistics report.

        get_serial_number():
            Get the serial number from the device statistics report.
    """
    def __init__(self, ip_address: str):
        """
        Initialize the Device object with the IP address of the networked device.

        Args:
            ip_address (str): The IP address of the networked device.
        """
        self.ip_address = ip_address
        self._report = None

    def __enter__(self):
        """
        Enter the context manager. Validates the IP address and creates the device report.

        Raises:
            InvalidAddressError: If the IP address is invalid.

        Returns:
            Device: The Device object.
        """
        if self.ip_address_is_valid():
            self.create_report()
            return self
        raise InvalidAddressError

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Implemented to use Device class as a context manager"""

    def ip_address_is_valid(self) -> bool:
        """
        Check if the provided IP address is a valid IPv4 address.

        Returns:
            bool: True if the IP address is valid, False otherwise.
        """
        try:
            ipaddress.ip_address(self.ip_address)
            return True
        except ValueError:
            return False

    def create_report(self):
        """
        Fetch the device statistics report from the device's web interface.
        """
        url = f'http://{self.ip_address}/cgi-bin/dynamic/printer/config/reports/devicestatistics.html'
        page = requests.get(url)
        if page.status_code == 200:
            self._report = page.text
            return
        raise CreateReportError

    def get_counter(self) -> str:
        """
        Get the current counter value from the device statistics report.

        Raises:
            ReportError: If the report is not available or the counter cannot be found.

        Returns:
            str: The counter value.
        """
        if self._report:
            soup = BeautifulSoup(self._report, 'html.parser')
            table = soup.find_all('table')[4]
            tr = table.find_all('tr')[-1]
            counter = tr.find_all('p')[-1].text.strip()
            return counter
        raise ReportError

    def get_serial_number(self) -> str:
        """
        Get the serial number from the device statistics report.

        Raises:
            ReportError: If the report is not available or the serial number cannot be found.

        Returns:
            str: The serial number.
        """
        if self._report:
            soup = BeautifulSoup(self._report, 'html.parser')
            table = soup.find_all('table')[10]
            tr = table.find_all('tr')[2]
            serial_number = tr.find_all('p')[-1].text.strip()
            return serial_number
        raise ReportError
