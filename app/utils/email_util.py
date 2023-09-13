"""Email utility class"""
from app.environments import settings

class EmailUtil:
    @classmethod
    def load_as_image_attachments(cls, files: list[str]) -> list[dict]:
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
