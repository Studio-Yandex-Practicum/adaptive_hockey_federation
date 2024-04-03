def get_split_discipline(discipline):
    """Разделяет дисциплину на название и числовой статус."""
    discipline_str = str(discipline)
    parts = discipline_str.split("(")
    if len(parts) == 2:
        discipline_name = parts[0].strip()
        status = parts[1].replace(")", "").strip()
        return (discipline_name, status)
    else:
        return ("Ошибка: Неверный формат строки", "Неверный формат строки")
