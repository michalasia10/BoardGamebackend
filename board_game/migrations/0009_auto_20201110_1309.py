# Generated by Django 3.0.4 on 2020-11-10 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_game', '0008_auto_20201110_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='projectName',
            field=models.CharField(help_text='Category of games', max_length=100, verbose_name='game category'),
        ),
    ]
