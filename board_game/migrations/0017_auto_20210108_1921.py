# Generated by Django 3.0.4 on 2021-01-08 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_game', '0016_auto_20210108_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='currentPlayer',
            field=models.IntegerField(blank=True, default=None,null=True),
        ),
    ]