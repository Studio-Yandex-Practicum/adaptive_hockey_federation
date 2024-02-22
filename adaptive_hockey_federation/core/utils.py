import os
from datetime import datetime

from core.constants import TIME_FORMAT


def generate_file_name(filename: str, prefix: str, suffix) -> str:
    filename, file_extension = os.path.splitext(filename)
    return (
        f"{prefix}-{datetime.now().strftime(TIME_FORMAT)}-"
        f"{suffix}{file_extension}"
    )
