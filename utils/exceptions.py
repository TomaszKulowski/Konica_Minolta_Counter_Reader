class InvalidAddressError(Exception):
    """
    Exception raised when an invalid address or address format is encountered.
    """


class ReportError(Exception):
    """
    Exception raised when an error occurs while generating or processing a report.
    """


class AddAutostartError(Exception):
    """
    Exception raised when an error occurs while adding an entry to the autostart.
    """
