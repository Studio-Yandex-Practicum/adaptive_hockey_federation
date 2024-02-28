def pluralize_days(days):
    """
    Вспомогательная функция для коректного отображения дней.
    """
    if days % 10 == 1 and days % 100 != 11:
        return f"{days} день"
    elif (
        days % 10 >= 2
        and days % 10 <= 4
        and (days % 100 < 10 or days % 100 >= 20)
    ):
        return f"{days} дня"
    else:
        return f"{days} дней"
