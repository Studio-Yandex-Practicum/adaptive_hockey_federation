import os
import random
from typing import Tuple

import factory
from competitions.models import Competition
from django.db.models import QuerySet
from main.models import Player, Team
from unloads.models import Unload
from unloads.utils import export_excel
from users.factories import UserFactory


class UnloadFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания тестовых Выгрузок."""

    class Meta:
        model = Unload

    unload_name = factory.Sequence(lambda n: f"Выгрузка{n}")
    date = factory.Faker("date_object")
    user = factory.SubFactory(UserFactory)
    unload_file_slug = factory.LazyAttribute(lambda o: "")

    @factory.post_generation
    def create_excel_file(obj, create, extracted, **kwargs):
        if not create:
            return

        queryset_with_titles = get_queryset_for_unload(obj)

        if queryset_with_titles:
            title = queryset_with_titles[1]
            queryset = queryset_with_titles[0]
            filename = f"{title}_{obj.unload_name}.xlsx"
            export_excel(queryset, filename, title)
            file_path = os.path.join("data", filename)
            obj.unload_file_slug = file_path
            obj.save()


def get_queryset_for_unload(unload_instance) -> Tuple[QuerySet, str]:
    choices = [
        (Competition.objects.all(), "Выгрузка соревнований"),
        (Player.objects.all(), "Выгрузка игроков"),
        (Team.objects.all(), "Выгрузка команд"),
    ]
    selected_choice = random.choice(choices)
    return selected_choice
