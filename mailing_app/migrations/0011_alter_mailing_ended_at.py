# Generated by Django 4.1.1 on 2022-09-25 22:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0010_alter_mailing_ended_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='ended_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 26, 1, 31, 53, 490563, tzinfo=datetime.timezone.utc)),
        ),
    ]
