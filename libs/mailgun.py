import os
from requests import Response, post
from typing import List

FAILED_LOAD_API_KEY = "Failed to load Mailgun API KEY"
FAILED_LOAD_DOMAIN = "Failed to load Mailgun Domain"
ERROR_SENDING_CONFIRMATION_EMAIL = "Error in sending confirmation email, user registration failed"


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:

    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")

    FROM_TITLE = "API REST STORES"
    FROM_EMAIL = "postmaster@sandboxd592c21b1f714fabbcf29f19c7322c18.mailgun.org"

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:

        if cls.MAILGUN_API_KEY is None:
            raise MailGunException(FAILED_LOAD_API_KEY)

        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException(FAILED_LOAD_DOMAIN)

        response = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )

        print("****** STATUS CODE *******")
        print(response.status_code)

        if response.status_code != 200:
            raise MailGunException(ERROR_SENDING_CONFIRMATION_EMAIL)

        return response
