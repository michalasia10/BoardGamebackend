# Generated by Django 3.0.4 on 2020-11-10 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board_game', '0009_auto_20201110_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='games',
            field=models.ForeignKey(help_text='Category of game which belong to', on_delete=django.db.models.deletion.CASCADE, related_name='games', to='board_game.Project', verbose_name='game category'),
        ),
        migrations.AlterField(
            model_name='game',
            name='imgUrl',
            field=models.URLField(help_text='URL to game image for logo', max_length=400, verbose_name="game's logo url"),
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(help_text='Game name', max_length=144, verbose_name='game name'),
        ),
        migrations.AlterField(
            model_name='match',
            name='game',
            field=models.ForeignKey(help_text='Type of game which match belong to', on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='board_game.Game', verbose_name='type of game'),
        ),
        migrations.AlterField(
            model_name='match',
            name='maxPlayers',
            field=models.IntegerField(default=2, help_text='Number of max players in each game', verbose_name='max players in game'),
        ),
        migrations.AlterField(
            model_name='match',
            name='state',
            field=models.CharField(default='---------', help_text='State of board', max_length=144, verbose_name='state of board'),
        ),
        migrations.AlterField(
            model_name='player',
            name='match',
            field=models.ForeignKey(help_text='choose match/room u want to join', on_delete=django.db.models.deletion.CASCADE, related_name='players', to='board_game.Match', verbose_name='match/room'),
        ),
        migrations.AlterField(
            model_name='player',
            name='playerName',
            field=models.OneToOneField(help_text='user will be a player ', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='board_game.User', verbose_name='player'),
        ),
    ]
