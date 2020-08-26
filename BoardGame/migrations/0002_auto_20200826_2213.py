# Generated by Django 3.0.9 on 2020-08-26 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BoardGame', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='BoardGame.Game'),
        ),
        migrations.AlterField(
            model_name='match',
            name='roomName',
            field=models.CharField(default='room', max_length=140, unique=True),
        ),
    ]
