import asyncio
import logging
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from settings import settings


logger = logging.getLogger(__name__)


async def send_email(
    recipient_email: str,
    subject: str,
    body: str
):
    """
    Send email asynchronously.

    SMTP is blocking, so the actual SMTP operation
    is moved to a background thread.
    """

    try:

        await asyncio.to_thread(
            send_email_sync,
            recipient_email,
            subject,
            body
        )

        logger.info(
            "Email sent successfully to %s",
            recipient_email
        )

    except Exception as e:

        # Email failure should NOT break
        # the comment/like API request.
        logger.error(
            "Email sending failed: %s",
            str(e)
        )


def send_email_sync(
    recipient_email: str,
    subject: str,
    body: str
):

    message = MIMEMultipart()

    message["From"] = (
        f"{settings.MAIL_FROM_NAME} "
        f"<{settings.MAIL_FROM}>"
    )

    message["To"] = recipient_email

    message["Subject"] = subject

    message.attach(
        MIMEText(
            body,
            "plain"
        )
    )

    with smtplib.SMTP(
        settings.MAIL_HOST,
        settings.MAIL_PORT
    ) as server:

        server.starttls()

        server.login(
            settings.MAIL_USERNAME,
            settings.MAIL_PASSWORD
        )

        server.sendmail(
            settings.MAIL_FROM,
            recipient_email,
            message.as_string()
        )