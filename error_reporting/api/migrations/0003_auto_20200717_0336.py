# Generated by Django 3.0.8 on 2020-07-17 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200714_0417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventuser',
            name='custom_data',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='eventuser',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
