# Generated by Django 4.1.1 on 2022-09-25 22:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0013_alter_mailing_ended_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='ended_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 26, 1, 34, 23, 647461, tzinfo=datetime.timezone.utc)),
        ),
    ]