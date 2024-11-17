from tri_api.core.logger import logger
from tri_api.support.enums import MailEnum
from tri_api.support.config import CONFIGURATION
from fastapi_mail import (
    FastMail,
    MessageSchema,
    MessageType,
    ConnectionConfig,
)


mail_conf = ConnectionConfig(
    MAIL_USERNAME=CONFIGURATION.mail_username,
    MAIL_PASSWORD=CONFIGURATION.mail_password,
    MAIL_FROM=CONFIGURATION.mail_sender,
    MAIL_PORT=CONFIGURATION.mail_port,
    MAIL_SERVER=CONFIGURATION.mail_server,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
)

mail = FastMail(mail_conf)


async def send_verification_email(email: str, token: str) -> None:
    """Send user verification email."""

    url = CONFIGURATION.root_url + MailEnum.verify_endpoint.value + token
    if CONFIGURATION.mail_console:
        logger.info("POST to " + url)
    else:
        message = MessageSchema(
            recipients=[email],
            subject=MailEnum.verify_subject.value,
            body=MailEnum.verify_body.value.format(url),
            subtype=MessageType.plain,
        )
        await mail.send_message(message)


async def send_password_reset_email(email: str, token: str) -> None:
    """Send password reset email."""
    # Change this later to public endpoint
    url = CONFIGURATION.root_url + MailEnum.reset_endpoint.value + token
    if CONFIGURATION.mail_console:
        logger.info("POST to " + url)
    else:
        message = MessageSchema(
            recipients=[email],
            subject=MailEnum.reset_subject.value,
            body=MailEnum.reset_body.value.format(url),
            subtype=MessageType.plain,
        )
        await mail.send_message(message)
