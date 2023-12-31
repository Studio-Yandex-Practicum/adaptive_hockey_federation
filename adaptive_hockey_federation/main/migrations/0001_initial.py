# Generated by Django 4.2.8 on 2023-12-16 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование', max_length=256, unique=True, verbose_name='Наименование')),
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
                ('name', models.CharField(help_text='Наименование', max_length=256, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Диагноз',
                'verbose_name_plural': 'Диагнозы',
            },
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Дисциплина',
                'verbose_name_plural': 'Дисциплины',
            },
        ),
        migrations.CreateModel(
            name='DisciplineLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование', max_length=256, unique=True, verbose_name='Наименование')),
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
                ('name', models.CharField(help_text='Наименование', max_length=256, unique=True, verbose_name='Наименование')),
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
                ('name', models.CharField(help_text='Наименование', max_length=256, unique=True, verbose_name='Наименование')),
                ('file', models.FileField(max_length=256, upload_to='documents')),
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
                ('name', models.CharField(help_text='Наименование', max_length=256, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Нозология',
                'verbose_name_plural': 'Нозология',
            },
        ),
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(default='', help_text='Фамилия', max_length=256, verbose_name='Фамилия')),
                ('name', models.CharField(default='', help_text='Имя', max_length=256, verbose_name='Имя')),
                ('patronymic', models.CharField(blank=True, default='', help_text='Отчество', max_length=256, verbose_name='Отчество')),
                ('phone', models.CharField(blank=True, default='', help_text='Номер телефона', max_length=256, verbose_name='Номер телефона')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='StaffTeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_position', models.CharField(choices=[('trainer', 'тренер'), ('other', 'другой')], default='', help_text='Статус сотрудника', max_length=256, verbose_name='Статус сотрудника')),
                ('qualification', models.CharField(blank=True, default='', help_text='Квалификация', max_length=256, verbose_name='Квалификация')),
                ('notes', models.TextField(blank=True, default='', help_text='Описание', verbose_name='Описание')),
                ('staff_member', models.ForeignKey(default='', help_text='Сотрудник', on_delete=django.db.models.deletion.SET_DEFAULT, to='main.staffmember', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Сотрудник команды',
                'verbose_name_plural': 'Сотрудники команды',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование', max_length=256, unique=True, verbose_name='Наименование')),
                ('city', models.ForeignKey(default='', help_text='Город откуда команда', on_delete=django.db.models.deletion.SET_DEFAULT, to='main.city', verbose_name='Город откуда команда')),
                ('discipline_name', models.ForeignKey(default='', help_text='Дисциплина команды', on_delete=django.db.models.deletion.SET_DEFAULT, to='main.disciplinename', verbose_name='Дисциплина команды')),
                ('staff_team_member', models.ForeignKey(default='', help_text='Сотрудник команды', on_delete=django.db.models.deletion.SET_DEFAULT, to='main.staffteammember', verbose_name='Сотрудник команды')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
                'default_related_name': 'teams',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(default='', help_text='Фамилия', max_length=256, verbose_name='Фамилия')),
                ('name', models.CharField(default='', help_text='Имя', max_length=256, verbose_name='Имя')),
                ('patronymic', models.CharField(blank=True, default='', help_text='Отчество', max_length=256, verbose_name='Отчество')),
                ('birthday', models.DateField(help_text='Дата рождения', verbose_name='Дата рождения')),
                ('gender', models.CharField(choices=[('male', 'Мужской'), ('female', 'Женский')], default='', help_text='Пол', max_length=256, verbose_name='Пол')),
                ('level_revision', models.TextField(blank=True, default='', help_text='Уровень ревизии', verbose_name='Уровень ревизии')),
                ('position', models.CharField(choices=[('striker', 'Нападающий'), ('bobber', 'Поплавок'), ('goalkeeper', 'Вратарь'), ('defender', 'Защитник')], default='', help_text='Игровая позиция', max_length=256, verbose_name='Игровая позиция')),
                ('number', models.IntegerField(default=0, help_text='Номер игрока', verbose_name='Номер игрока')),
                ('is_captain', models.BooleanField(default=False, help_text='Капитан', verbose_name='Капитан')),
                ('is_assistent', models.BooleanField(default=False, help_text='Ассистент', verbose_name='Ассистент')),
                ('identity_document', models.TextField(blank=True, default='', help_text='Удостоверение личности', verbose_name='Удостоверение личности')),
                ('diagnosis', models.ForeignKey(default=0, help_text='Диагноз', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_diagnosis', to='main.diagnosis', verbose_name='Диагноз')),
                ('discipline', models.ForeignKey(default='', help_text='Дисциплина', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_disciplines', to='main.discipline', verbose_name='Дисциплина')),
                ('document', models.ForeignKey(blank=True, default='', help_text='Документ', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_documemts', to='main.document', verbose_name='Документ')),
                ('team', models.ManyToManyField(help_text='Команда', related_name='team_players', to='main.team', verbose_name='Команда')),
            ],
            options={
                'verbose_name': 'Игрок',
                'verbose_name_plural': 'Игроки',
                'ordering': ('surname', 'name', 'patronymic'),
                'abstract': False,
                'default_related_name': 'players',
            },
        ),
        migrations.AddField(
            model_name='discipline',
            name='discipline_level',
            field=models.ForeignKey(help_text='Класс/статус', max_length=10, on_delete=django.db.models.deletion.CASCADE, related_name='disciplines', to='main.disciplinelevel', verbose_name='Класс/статус'),
        ),
        migrations.AddField(
            model_name='discipline',
            name='discipline_name',
            field=models.ForeignKey(help_text='Название дисциплины', max_length=10, on_delete=django.db.models.deletion.CASCADE, related_name='disciplines', to='main.disciplinename', verbose_name='Название дисциплины'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='nosology',
            field=models.ForeignKey(help_text='Нозология', max_length=10, on_delete=django.db.models.deletion.CASCADE, related_name='diagnosis', to='main.nosology', verbose_name='Нозология'),
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('name', 'city', 'discipline_name'), name='team_city_unique'),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.UniqueConstraint(fields=('name', 'surname', 'patronymic', 'birthday'), name='player_unique'),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.UniqueConstraint(fields=('position', 'number'), name='player_position_number_unique'),
        ),
        migrations.AddConstraint(
            model_name='discipline',
            constraint=models.UniqueConstraint(fields=('discipline_name', 'discipline_level'), name='discipline_name_level_unique'),
        ),
    ]
