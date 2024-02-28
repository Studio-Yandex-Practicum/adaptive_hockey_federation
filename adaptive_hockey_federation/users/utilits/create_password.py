import random
import string


def generate_random_password(length: int = 12) -> str:
    """Функция генерации случайного пароля пользователя"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))
