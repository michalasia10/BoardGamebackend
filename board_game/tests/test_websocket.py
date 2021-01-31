from channels.testing import  WebsocketCommunicator
from channels.sessions import SessionMiddlewareStack
import pytest
from configuration.routing import application
from channels.db import database_sync_to_async
from board_game.models import Game,Project,User,Player,Match
from random import choice


TEST_CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

names = ['michal', 'artur', 'marek', 'wiktoria']
numbers = [str(i) for i in list(range(1000))]




@database_sync_to_async
def make_match_with_one_player():
    category = Project.objects.create(projectName='planszufki')
    game = Game.objects.create(games=category, name='kółko i krzyżyk',
                               imgUrl='https://image.freepik.com/darmowe-wektory/gra-tic-tac-toe_97886-854.jpg')
    match = Match.objects.create(game=game, maxPlayers=2)
    user = User.objects.create(username=choice(names) + choice(numbers))
    player = Player.objects.create(match=match,
                                    playerName=user)
    return match, player

@database_sync_to_async
def add_second_player_to_match(match):
    userSecond = User.objects.create(username=choice(names) + choice(numbers))
    playerSecond = Player.objects.create(match=match,
                                    playerName=userSecond)
    return playerSecond

@pytest.mark.django_db
@pytest.mark.asyncio
class TestWebSocket:
    async def test_websocket_can_connect(self,settings):

        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        app = SessionMiddlewareStack(application)
        # Create to communicators
        match,playerFirst = await make_match_with_one_player()
        communicator = WebsocketCommunicator(app, f'ws/match/{match.pk}')
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()




