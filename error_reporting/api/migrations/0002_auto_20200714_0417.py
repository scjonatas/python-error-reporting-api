# Generated by Django 3.0.8 on 2020-07-14 04:17

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='EventUser',
        ),
        migrations.RenameField(
            model_name='agent',
            old_name='user',
            new_name='event_user',
        ),
    ]
