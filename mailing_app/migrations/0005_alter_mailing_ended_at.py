# Generated by Django 4.1.1 on 2022-09-20 05:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0004_alter_message_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='ended_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 9, 20, 8, 28, 8, 380479), null=True),
        ),
    ]
