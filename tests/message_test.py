"""
Unit Tests for the 'utils.message.py' module.
"""
from email.message import EmailMessage
from unittest.mock import patch

import pytest

from utils.message import Email


@pytest.fixture
def email_fixture():
    """
    Fixture for creating an Email instance with predefined settings for testing.

    Returns:
        Email: An Email instance configured for testing.
    """
    return Email(
        smtp_server='smtp.gmail.com',
        login='sender_email@gmail.com',
        password='password',
        port=123,
        receiver='receiver_email@gmail.com',
        encryption='No',
    )


def test_create_message(email_fixture: Email):
    """
    Test the creation of an EmailMessage object with the specified content.

    Args:
        email_fixture (Email): An Email instance configured for testing.

    Raises:
        AssertionError: If the created EmailMessage object does not have the
        expected properties and content.
    """
    message = email_fixture._create_message('message title', 'message content')

    assert isinstance(message, EmailMessage)
    assert message['Subject'] == 'message title'
    assert message['From'] == 'sender_email@gmail.com'
    assert message['To'] == 'receiver_email@gmail.com'
    assert message.get_content() == 'message content\n'


@pytest.mark.parametrize('encryption', ('No', 'TLS'))
@patch('smtplib.SMTP')
@patch('utils.message.Email._create_message', return_value='message_body')
def test_send_email(mock_message: patch, mock_smtp: patch, encryption: str, email_fixture: Email):
    """
    Test the sending of an email using SMTP with optional TLS encryption.

    Args:
        mock_message (patch): A mock for the _create_message method.
        mock_smtp (patch): A mock for the SMTP class.
        encryption (str): The encryption type ('No' or 'TLS').
        email_fixture (Email): An Email instance configured for testing.

    Raises:
        AssertionError: If the email sending process does not behave as expected.
    """
    email_fixture.encryption = encryption

    email_fixture.send('message title', 'message content')

    mock_smtp.assert_called_once_with(email_fixture.smtp_server, email_fixture.port)
    context = mock_smtp.return_value.__enter__.return_value
    context.login.assert_called_once_with(email_fixture.login, email_fixture.password)
    context.send_message.assert_called_once_with('message_body')
    mock_message.assert_called_once()

    if encryption == 'TLS':
        mock_smtp.return_value.__enter__.return_value.starttls.assert_called()


@patch('smtplib.SMTP_SSL')
@patch('utils.message.Email._create_message', return_value='message_body')
def test_send_email_using_ssl(mock_message: patch, mock_smtp_ssl: patch, email_fixture: Email):
    """
    Test the sending of an email using SMTP with SSL encryption.

    Args:
        mock_message (patch): A mock for the _create_message method.
        mock_smtp_ssl (patch): A mock for the SMTP_SSL class.
        email_fixture (Email): An Email instance configured for testing.

    Raises:
        AssertionError: If the email sending process does not behave as expected.
    """
    email_fixture.encryption = 'SSL'

    email_fixture.send('message title', 'message content')

    mock_smtp_ssl.assert_called_once_with(email_fixture.smtp_server, email_fixture.port)
    context = mock_smtp_ssl.return_value.__enter__.return_value
    context.login.assert_called_once_with(email_fixture.login, email_fixture.password)
    context.send_message.assert_called_once_with('message_body')
    mock_message.assert_called_once()
