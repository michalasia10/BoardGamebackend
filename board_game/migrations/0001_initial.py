# Generated by Django 3.0.9 on 2020-09-27 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=144)),
                ('imgUrl', models.URLField(max_length=400)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectName', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('projectName',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=144, unique=True)),
            ],
            options={
                'ordering': ('username',),
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playersNumber', models.IntegerField(default=2)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='board_game.Game')),
            ],
            options={
                'ordering': ('game',),
            },
        ),
        migrations.AddField(
            model_name='game',
            name='games',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='board_game.Project'),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('playerName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='board_game.User')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board_game.Match')),
            ],
            options={
                'ordering': ('playerName',),
            },
        ),
    ]
