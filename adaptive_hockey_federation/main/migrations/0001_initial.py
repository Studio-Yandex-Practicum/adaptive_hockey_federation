# Generated by Django 4.2.13 on 2024-06-03 19:22

import core.constants
import core.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import phonenumber_field.validators
import users.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Диагноз',
                'verbose_name_plural': 'Диагнозы',
            },
        ),
        migrations.CreateModel(
            name='DisciplineLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Классификация/статус дисциплины',
                'verbose_name_plural': 'Классификация/статусы дисциплин',
            },
        ),
        migrations.CreateModel(
            name='DisciplineName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Название дисциплины',
                'verbose_name_plural': 'Названия дисциплин',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], verbose_name='Наименование')),
                ('file', models.FileField(max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], unique=True, upload_to='players_documents')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
        migrations.CreateModel(
            name='Nosology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Нозология',
                'verbose_name_plural': 'Нозология',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Фамилия', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], validators=[django.core.validators.RegexValidator('^[А-Яа-яё -]+$', 'Строка должны состоять из кирилических символов. Возможно использование дефиса.')], verbose_name='Фамилия')),
                ('name', models.CharField(default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Имя', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], validators=[django.core.validators.RegexValidator('^[А-Яа-яё -]+$', 'Строка должны состоять из кирилических символов. Возможно использование дефиса.')], verbose_name='Имя')),
                ('patronymic', models.CharField(blank=True, default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Отчество', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], validators=[django.core.validators.RegexValidator('^[А-Яа-яё -]+$', 'Строка должны состоять из кирилических символов. Возможно использование дефиса.')], verbose_name='Отчество')),
                ('birthday', models.DateField(help_text='Дата рождения', validators=[core.validators.validate_date_birth], verbose_name='Дата рождения')),
                ('addition_date', models.DateField(default=django.utils.timezone.now, help_text='Дата добавления в базу данных', verbose_name='Дата добавления')),
                ('gender', models.CharField(choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')], default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Пол', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], verbose_name='Пол')),
                ('level_revision', models.TextField(blank=True, default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Игровая классификация', verbose_name='Игровая классификация')),
                ('position', models.CharField(choices=[('Нападающий', 'Нападающий'), ('Поплавок', 'Поплавок'), ('Вратарь', 'Вратарь'), ('Защитник', 'Защитник')], default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Игровая позиция', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], verbose_name='Игровая позиция')),
                ('number', models.IntegerField(default=core.constants.MainConstantsInt['DEFAULT_VALUE'], help_text='Номер игрока', verbose_name='Номер игрока')),
                ('is_captain', models.BooleanField(default=False, verbose_name='Капитан')),
                ('is_assistent', models.BooleanField(default=False, verbose_name='Ассистент')),
                ('identity_document', models.TextField(blank=True, default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Удостоверение личности', verbose_name='Удостоверение личности')),
            ],
            options={
                'verbose_name': 'Игрок',
                'verbose_name_plural': 'Игроки',
                'ordering': ('surname', 'name', 'patronymic'),
                'permissions': [('list_view_player', 'Can view list of Игрок')],
                'abstract': False,
                'default_related_name': 'players',
            },
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Фамилия', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], validators=[django.core.validators.RegexValidator('^[А-Яа-яё -]+$', 'Строка должны состоять из кирилических символов. Возможно использование дефиса.')], verbose_name='Фамилия')),
                ('name', models.CharField(default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Имя', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], validators=[django.core.validators.RegexValidator('^[А-Яа-яё -]+$', 'Строка должны состоять из кирилических символов. Возможно использование дефиса.')], verbose_name='Имя')),
                ('patronymic', models.CharField(blank=True, default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Отчество', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], validators=[django.core.validators.RegexValidator('^[А-Яа-яё -]+$', 'Строка должны состоять из кирилических символов. Возможно использование дефиса.')], verbose_name='Отчество')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Номер телефона, допустимый формат - +7 ХХХ ХХХ ХХ ХХ', max_length=128, region=None, validators=[phonenumber_field.validators.validate_international_phonenumber, users.validators.zone_code_without_seven_hundred], verbose_name='Актуальный номер телефона')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], unique=True, verbose_name='Наименование')),
                ('city', models.ForeignKey(help_text='Город откуда команда', on_delete=django.db.models.deletion.CASCADE, to='main.city', verbose_name='Город откуда команда')),
                ('curator', models.ForeignKey(help_text='Куратор команды', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team', to=settings.AUTH_USER_MODEL, verbose_name='Куратор команды')),
                ('discipline_name', models.ForeignKey(help_text='Дисциплина команды', on_delete=django.db.models.deletion.CASCADE, to='main.disciplinename', verbose_name='Дисциплина команды')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
                'permissions': [('list_view_team', 'Can view list of Команда')],
                'default_related_name': 'teams',
            },
        ),
        migrations.CreateModel(
            name='StaffTeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_position', models.CharField(choices=[('тренер', 'тренер'), ('пушер-тьютор', 'пушер-тьютор')], default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Статус сотрудника', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], verbose_name='Статус сотрудника')),
                ('qualification', models.CharField(blank=True, default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Квалификация', max_length=core.constants.MainConstantsInt['CHAR_FIELD_LENGTH'], verbose_name='Квалификация')),
                ('notes', models.TextField(blank=True, default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Описание', verbose_name='Описание')),
                ('staff_member', models.ForeignKey(help_text='Сотрудник', on_delete=django.db.models.deletion.CASCADE, to='main.staffmember', verbose_name='Сотрудник')),
                ('team', models.ManyToManyField(blank=True, default='Свободный агент', help_text='Команда', related_name='team_members', to='main.team', verbose_name='Команда')),
            ],
            options={
                'verbose_name': 'Сотрудник команды',
                'verbose_name_plural': 'Сотрудники команды',
                'permissions': [('list_view_staff', 'Can view list of Персонала команды')],
            },
        ),
        migrations.AddConstraint(
            model_name='staffmember',
            constraint=models.UniqueConstraint(fields=('name', 'surname', 'patronymic'), name='staff_member_unique'),
        ),
        migrations.AddField(
            model_name='player',
            name='diagnosis',
            field=models.ForeignKey(help_text='Диагноз', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_diagnosis', to='main.diagnosis', verbose_name='Диагноз'),
        ),
        migrations.AddField(
            model_name='player',
            name='discipline_level',
            field=models.ForeignKey(help_text='Числовой статус', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_disciplines_levels', to='main.disciplinelevel', verbose_name='Числовой статус'),
        ),
        migrations.AddField(
            model_name='player',
            name='discipline_name',
            field=models.ForeignKey(help_text='Дисциплина', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_disciplines_names', to='main.disciplinename', verbose_name='Дисциплина'),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ManyToManyField(help_text='Команда', related_name='team_players', to='main.team', verbose_name='Команда'),
        ),
        migrations.AddField(
            model_name='document',
            name='player',
            field=models.ForeignKey(blank=True, default=core.constants.MainConstantsStr['EMPTY_VALUE_DISPLAY'], help_text='Игрок', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_documemts', to='main.player', verbose_name='Игрок'),
        ),
        migrations.AddField(
            model_name='disciplinelevel',
            name='discipline_name',
            field=models.ForeignKey(help_text='Дисциплина', on_delete=django.db.models.deletion.CASCADE, related_name='levels', to='main.disciplinename', verbose_name='Дисциплина'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='nosology',
            field=models.ForeignKey(help_text='Нозология', max_length=core.constants.MainConstantsInt['CLASS_FIELD_LENGTH'], on_delete=django.db.models.deletion.CASCADE, related_name='diagnosis', to='main.nosology', verbose_name='Нозология'),
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('name', 'city', 'discipline_name'), name='team_city_unique'),
        ),
        migrations.AddConstraint(
            model_name='staffteammember',
            constraint=models.UniqueConstraint(fields=('staff_member', 'staff_position'), name='staff_member_position_unique'),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.UniqueConstraint(fields=('name', 'surname', 'patronymic', 'birthday'), name='player_unique'),
        ),
        migrations.AddConstraint(
            model_name='document',
            constraint=models.UniqueConstraint(fields=('file', 'player'), name='player_docume_unique'),
        ),
    ]
