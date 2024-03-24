import os
from datetime import datetime

from core.config.base_settings import FILE_RESOLUTION, MAX_UPLOAD_SIZE
from core.constants import TIME_FORMAT
from django.core.files.uploadedfile import InMemoryUploadedFile


def generate_file_name(filename: str, prefix: str) -> str:
    filename, file_extension = os.path.splitext(filename)
    return (
        f"{prefix}-{datetime.now().strftime(TIME_FORMAT)}" f"{file_extension}"
    )


def is_uploaded_file_valid(file: InMemoryUploadedFile) -> bool:
    if (
        file.content_type
        and file.size
        and file.content_type.split("/")[1] in FILE_RESOLUTION
        and file.size <= MAX_UPLOAD_SIZE
    ):
        return True
    return False
