import os
from datetime import datetime

TIME_FORMAT = '%H-%M-%S'


def generate_file_name(filename: str, prefix: str, suffix) -> str:
    filename, file_extension = os.path.splitext(filename)
    return (f'{prefix}-{datetime.now().strftime(TIME_FORMAT)}-'
            f'{suffix}{file_extension}')
