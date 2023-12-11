
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Описание команды"

    def handle(self, *args, **options):
        return 'Я заготовка'
