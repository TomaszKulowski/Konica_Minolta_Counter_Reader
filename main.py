"""
This script automates sending periodic emails with printer statistics. It reads configuration
from environment variables or a .env file, schedules email sending based on specified intervals,
and sends printer statistics via email.

It uses the following environment variables:
- SEND_INTERVAL: Interval between email sends in hours.
- NEXT_SEND: The next scheduled email send time.
- SEND_EVERY: The time unit for scheduling (e.g., 'days', 'hours', 'minutes').
- PRINTER_IP: The IP address of the printer to retrieve statistics from.
- SMTP_SERVER: The SMTP server for sending emails.
- EMAIL_LOGIN: The login username for the email account.
- EMAIL_PASSWORD: The password for the email account.
- SMTP_PORT: The SMTP port for email sending.
- EMAIL_RECEIVER: The recipient email address.
- ENCRYPTION: The encryption method for the email (e.g., 'TLS', 'SSL').

The script utilizes external modules and utilities such as 'autostart', 'message', 'printer',
'schedule', and 'template' for its functionality.

Usage:
    To use this script, configure the required environment variables and run it. It will
    periodically send printer statistics via email based on the specified interval.
"""

from os import getenv, environ
from pathlib import Path
from time import sleep

from dotenv import load_dotenv

from utils import autostart
from utils.message import Email
from utils.printer import Device
from utils.schedule import Schedule
from utils.template import message_body, message_title


def change_next_send_date(next_send: str):
    """
    Change the value of the 'NEXT_SEND' environment variable or update the '.env' file
    with the provided 'next_send' value.

    Args:
        next_send (str): The new value for the 'NEXT_SEND' environment variable.
    """
    if Path('.env').exists():
        content = ''
        with open('.env', 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if 'NEXT_SEND' not in line:
                    content += line
            content += f'NEXT_SEND = {next_send}'
        with open('.env', 'w') as file:
            file.write(content)
    else:
        environ['NEXT_SEND'] = next_send


def main():
    """
    Main function to automate sending periodic emails with printer statistics.

    It checks if the script should run automatically at startup, schedules email sending
    based on the specified interval, retrieves printer statistics, sends the statistics
    via email, and updates the 'NEXT_SEND' value.
    """
    if not autostart.check(__file__):
        autostart.add(__file__)

    while True:
        schedule = Schedule(int(getenv('SEND_INTERVAL')), getenv('NEXT_SEND'))
        schedule.call_every(getenv('SEND_EVERY').lower())
        if schedule.check_time():
            with Device(getenv('PRINTER_IP')) as device:
                serial_number = device.get_serial_number()
                counter = device.get_counter()

            message = Email(
                smtp_server=getenv('SMTP_SERVER'),
                login=getenv('EMAIL_LOGIN'),
                password=getenv('EMAIL_PASSWORD'),
                port=int(getenv('SMTP_PORT')),
                receiver=getenv('EMAIL_RECEIVER'),
                encryption=getenv('ENCRYPTION'),
            )

            message.send(message_title(), message_body(counter, serial_number))
            change_next_send_date(schedule.next_call)

        sleep(60*60)


if __name__ == '__main__':
    load_dotenv()
    main()
