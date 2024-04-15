from core.constants import DISCIPLINE_LEVELS
from django.db import migrations


def set_default_disciplines(apps, schema_editor):
    DisciplineName = apps.get_model("main", "DisciplineName")
    DisciplineName.objects.bulk_create(
        [DisciplineName(name=name) for name in set(DISCIPLINE_LEVELS.keys())]
    )


def set_discipline_levels_to_discipline_name(apps, schema_editor):
    DisciplineName = apps.get_model("main", "DisciplineName")
    DisciplineLevel = apps.get_model("main", "DisciplineLevel")
    for discipline_name in DisciplineName.objects.all():
        for discipline_level in DISCIPLINE_LEVELS[discipline_name.name]:
            new_discipline_level = DisciplineLevel(
                name=discipline_level,
                discipline_name=discipline_name,
            )
            new_discipline_level.save()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0025_disciplinelevel_discipline_name"),
    ]

    operations = [
        migrations.RunPython(
            set_default_disciplines,
        ),
        migrations.RunPython(
            set_discipline_levels_to_discipline_name,
        ),
    ]
