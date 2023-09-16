"""
This Python module, 'templates.py,' contains functions for generating email message content.
It provides functions to generate email titles and bodies with printer statistics.
"""

from datetime import datetime


def message_title() -> str:
    """
    Generate the title for an email message.

    Returns:
        str: The title for the email message.
    """
    return 'Counter List'


def message_body(counter: str, serial_number: str) -> str:
    """
    Generate the body for an email message containing printer statistics.

    Args:
        counter (str): The printer counter value as a string.
        serial_number (str): The printer's serial number as a string.

    Returns:
        str: The body of the email message containing printer statistics.
    """
    return f"""Time: {datetime.now().strftime('%d-%m-%Y %H:%M')}
Printer serial number: {serial_number}
Printer counter: {counter} copies
"""
