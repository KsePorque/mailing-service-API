# Generated by Django 4.1.1 on 2022-09-20 06:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0007_alter_mailing_ended_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='ended_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 20, 10, 2, 3, 656407, tzinfo=datetime.timezone.utc)),
        ),
    ]
