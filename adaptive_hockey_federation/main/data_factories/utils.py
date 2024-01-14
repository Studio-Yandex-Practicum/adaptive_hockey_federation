import random


def check_len(field, max, min):
    """
    Функция проверяет количество созданны фабрикой слов,
    и при необходимости коректирует их число до требуемого.
    """
    words = field.split()
    count = min - len(words)
    if len(words) < min:
        add_words = words[:count]
        words.append(' '.join(add_words))
    if len(words) > max:
        del words[max:]
    field = ' '.join(words)
    return field


def get_random_objects(model):
    """Функция получает рандомные записи, из представленой модели данных."""
    queryset = model.objects.distinct()
    return random.choice(queryset)
