# Generated by Django 3.0.8 on 2020-07-17 04:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200717_0336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='custom_data',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='eventuser',
            name='custom_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, validators=[django.core.validators.EmailValidator]),
        ),
        migrations.AlterField(
            model_name='eventuser',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='eventuser',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
