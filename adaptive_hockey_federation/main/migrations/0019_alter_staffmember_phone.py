# Generated by Django 4.2.10 on 2024-03-23 20:12

import phonenumber_field.modelfields
import phonenumber_field.validators
import users.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0018_alter_player_birthday_alter_player_gender_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staffmember",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                help_text="Номер телефона, допустимый формат - +7 ХХХ ХХХ ХХ ХХ",
                max_length=128,
                region=None,
                validators=[
                    phonenumber_field.validators.validate_international_phonenumber,
                    users.validators.zone_code_without_seven_hundred,
                ],
                verbose_name="Актуальный номер телефона",
            ),
        ),
    ]
