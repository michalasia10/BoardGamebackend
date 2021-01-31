import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Match, Game, Project, User, Player
from random import choice



# initialize the APIClient app
client = Client()

# data to test
names = ['michal', 'artur', 'marek', 'wiktoria']
numbers = [str(i) for i in list(range(1000))]


class JoinPlayer(TestCase):
    def setUp(self) -> None:
        self.category = Project.objects.create(projectName='planszufki')
        self.game = Game.objects.create(games=self.category,
                                        name='kółko i krzyżyk',
                                        imgUrl='https://image.freepik.com/darmowe-wektory/gra-tic-tac-toe_97886-854.jpg')
        self.matchFirst = Match.objects.create(game=self.game,
                                               maxPlayers=2)
        self.matchSecond = Match.objects.create(game=self.game,
                                                maxPlayers=2)

        self.userFirst = User.objects.create(username=choice(names) + choice(numbers))
        self.userSecond = User.objects.create(username=choice(names) + choice(numbers))

        self.playerFirst = Player.objects.create(match=self.matchFirst,
                                                 playerName=self.userFirst)
        self.playerSecond = Player.objects.create(match=self.matchFirst,
                                                  playerName=self.userSecond)

        self.invalid_payload = {
            "match": self.matchSecond.pk,
            "playerName": self.userFirst.pk
        }

    def test_join_player_to_game_being_the_same_time_in_other(self):
        response = client.post(
            reverse('join-match'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        message = {'message': 'YOU ARE IN ANOTHER GAME'}
        self.assertEqual(response.data,message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


