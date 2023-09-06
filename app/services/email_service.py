"""Service responsible for everything to do with emails"""
from typing import Coroutine, Callable

from fastapi import BackgroundTasks

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from jinja2 import Environment, Template

from app.environments import settings
from app.schemas.libs import Email
from app import templates_environment


class EmailService:
    _fast_mail: FastMail
    _config: ConnectionConfig
    _templates: Environment

    def __init__(self):
        self._config = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
            USE_CREDENTIALS=settings.MAIL_USE_CREDENTIALS,
            VALIDATE_CERTS=settings.MAIL_VALIDATE_CERTS,
            TEMPLATE_FOLDER=settings.MAIL_TEMPLATE_PATH
        )
        self._templates = templates_environment
        self._fast_mail = FastMail(config=self._config)

    @classmethod
    def _create_mail(
            cls,
            title: str,
            recipients: list[Email],
            template: str,
            template_type: MessageType,
            attachments: list[dict] = None
    ) -> MessageSchema:
        return MessageSchema(
            subject=title,
            recipients=recipients,
            body=template,
            subtype=template_type,
            attachments=attachments
        )

    def create_email_verification_mail(self, recipients: list[Email], verification_code: str, username: str) -> MessageSchema:
        email_verification_template: Template = self._templates.get_template('email-verification-template.html.jinja')
        email_verification_html: str = email_verification_template.render({
            'verification_url': f'http://{settings.HOST_NAME}/verify-email/{verification_code}',
            'username': username
        })
        return self._create_mail(
            title='Please verify your email address',
            recipients=recipients,
            template=email_verification_html,
            template_type=MessageType.html,
            attachments=EmailService._load_as_image_attachments([
                'facebook_logo.png',
                'instagram_logo.png',
                'linkedin_logo.png',
                'rats-nest_logo.jpg'
            ])
        )

    # TODO: Use (uvicorn main:app --workers 4)
    def send(self, background_task: BackgroundTasks, message: MessageSchema) -> None:
        send_task: Callable[[MessageSchema], Coroutine] = self._fast_mail.send_message
        background_task.add_task(send_task, message=message)

    @classmethod
    def _load_as_image_attachments(cls, files: list[str]) -> list[dict]:
        return [cls._file_to_image_attachment(file) for file in files]

    @classmethod
    def _file_to_image_attachment(cls, file: str) -> dict:
        file_name: str = file.split('.')[0].lower()
        file_prefix: str = file_name.split('.')[-1].lower()
        return {
            'file': f'{settings.MAIL_IMAGE_PATH}/{file}',
            'headers': {
                'Content-ID': f'<{file_name}@fastapi-mail>'
            },
            'mime_type': 'image',
            'mime_subtype': file_prefix
        }

emailService: EmailService = EmailService()
