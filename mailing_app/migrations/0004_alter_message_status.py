# Generated by Django 4.1.1 on 2022-09-19 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0003_mailing_filter_code_mailing_filter_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.IntegerField(choices=[(1, 'is_sent'), (0, 'not_sent'), (2, 'is_pending')], default=0),
        ),
    ]
