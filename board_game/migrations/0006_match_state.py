# Generated by Django 3.0.4 on 2020-11-03 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_game', '0005_auto_20201003_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='state',
            field=models.CharField(default='---------', max_length=144),
        ),
    ]