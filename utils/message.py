"""
This Python script provides a utility class for sending emails using SMTP with optional SSL or TLS encryption.
It includes an 'Email' class with methods for creating and sending emails.
"""

from email.message import EmailMessage
from smtplib import SMTP, SMTP_SSL


class Email:
    """
    A utility class for sending emails using SMTP with optional SSL or TLS encryption.

    Attributes:
        smtp_server (str): The SMTP server for sending emails.
        login (str): The login username for the email account.
        password (str): The password for the email account.
        port (int): The SMTP port for email sending.
        receiver (str): The recipient email address.
        encryption (str): The encryption method for the email ('SSL', 'TLS', or 'None').

    Methods:
        _create_message(message_title: str, message_body: str):
            Create an EmailMessage object with the specified title, body, and sender/receiver information.

        send(title: str, message: str):
            Send an email with the given title and message content to the specified recipient.
    """
    def __init__(self, smtp_server: str, login: str, password: str, port: int, receiver: str, encryption: str):
        """
        Initialize the Email object with the necessary email parameters.

        Args:
            smtp_server (str): The SMTP server for sending emails.
            login (str): The login username for the email account.
            password (str): The password for the email account.
            port (int): The SMTP port for email sending.
            receiver (str): The recipient email address.
            encryption (str): The encryption method for the email ('SSL', 'TLS', or 'None').
        """
        self.smtp_server = smtp_server
        self.login = login
        self.password = password
        self.port = port
        self.receiver = receiver
        self.encryption = encryption

    def _create_message(self, message_title: str, message_body: str) -> EmailMessage:
        """
        Create an EmailMessage object with the specified title, body, and sender/receiver information.

        Args:
            message_title (str): The title or subject of the email.
            message_body (str): The body or content of the email.

        Returns:
            EmailMessage: An EmailMessage object representing the email to be sent.
        """
        message = EmailMessage()
        message['Subject'] = message_title
        message['From'] = self.login
        message['To'] = self.receiver
        message.set_content(message_body)
        return message

    def send(self, title, message):
        """
        Send an email with the given title and message content to the specified recipient.

        Args:
            title (str): The title or subject of the email.
            message (str): The body or content of the email.
        """
        if self.encryption.upper() == 'SSL':
            with SMTP_SSL(self.smtp_server, self.port) as server:
                server.login(self.login, self.password)
                server.send_message(self._create_message(title, message))
        else:
            with SMTP(self.smtp_server, self.port) as server:
                if self.encryption.upper() == 'TLS':
                    server.starttls()
                server.login(self.login, self.password)
                server.send_message(self._create_message(title, message))
