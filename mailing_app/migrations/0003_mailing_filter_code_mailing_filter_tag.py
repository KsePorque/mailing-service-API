# Generated by Django 4.1.1 on 2022-09-19 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0002_alter_mailing_ended_at_alter_mailing_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='filter_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mailing',
            name='filter_tag',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
