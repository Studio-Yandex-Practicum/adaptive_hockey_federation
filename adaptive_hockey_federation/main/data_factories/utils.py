import random

from main.models import DisciplineLevel, DisciplineName, Player, Team


def check_len(field, max, min):
    """
    Функция проверяет количество созданны фабрикой слов,
    и при необходимости коректирует их число до требуемого.
    """
    words = field.split()
    count = min - len(words)
    if len(words) < min:
        add_words = words[:count]
        words.append(" ".join(add_words))
    if len(words) > max:
        del words[max:]
    field = " ".join(words)
    return field


def get_random_objects(model):
    """Функция получает рандомные записи, из представленой модели данных."""
    queryset = model.objects.distinct()
    return random.choice(queryset)


def updates_for_players():
    """
    Обновления записей игроков в базе данных. Функция проходит по всем
    существующим командам, присваивает должности капитанов и помощников,
    в каждой команде по одному капитану и помощнику. Затем к каждому игроку
    в команде присваевается дисциплина которая соответствует его команде.
    """
    teams = Team.objects.all()
    for team in teams:
        player_in_team = Player.objects.filter(team__id=team.id)
        disciplines_names = DisciplineName.objects.filter(
            id=team.discipline_name.id
        )
        discipline_name = random.choice(disciplines_names)
        discipline_levels = DisciplineLevel.objects.filter(
            discipline_name=discipline_name,
        )
        discipline_level = random.choice(discipline_levels)
        captain = random.choice(player_in_team)
        assistent = random.choice(player_in_team)
        captain.is_captain = True
        assistent.is_assistent = True
        captain.save()
        assistent.save()
        player_in_team.update(
            discipline_name=discipline_name, discipline_level=discipline_level
        )
