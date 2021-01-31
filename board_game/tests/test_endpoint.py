import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Match, Game, Project, User, Player
from ..serializers import MatchSerializer, CreateMatchSerializer, RoomSerializer, PlayersSerializerDetail, \
    GameSerializer, UserSerializerGet, UserSerializerPost
from random import choice
from django.shortcuts import get_object_or_404

# initialize the APIClient app
client = Client()


# data to test
names = ['michal', 'artur', 'marek', 'wiktoria']
numbers = [str(i) for i in list(range(1000))]


# endpoint : '/games'
class GetAllGames(TestCase):
    def setUp(self) -> None:
        self.category = Project.objects.create(projectName='planszufki')
        self.game = Game.objects.create(games=self.category,
                            name='kolko i krzyzyk',
                            imgUrl='https://stackoverflow.com/questions/52827996/how-do-i-test-the-foreign-key-object-on-django-model/52828084')
        Game.objects.create(games=self.category,
                            name='szachy',
                            imgUrl='https://stackoverflow.com/questions/52827996/how-do-i-test-the-foreign-key-object-on-django-model/52828084')
        Match.objects.create(game=self.game, maxPlayers=2)


    def test_get_all_type_of_games(self):
        response = client.get(reverse('game-list'))
        games = Game.objects.all()
        serializer = GameSerializer(games,many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# endpoint : '/creatematch'
class CreateMatchesTest(TestCase):

    def setUp(self) -> None:
        self.category = Project.objects.create(projectName='planszufki')
        self.game = Game.objects.create(games=self.category,
                                        name='szachy',
                                        imgUrl='https://stackoverflow.com/questions/52827996/how-do-i-test-the-foreign-key-object-on-django-model/52828084')
        Match.objects.create(game=self.game, maxPlayers=choice(numbers))
        Match.objects.create(game=self.game, maxPlayers=choice(numbers))
        Match.objects.create(game=self.game, maxPlayers=choice(numbers))

    def test_get_all_matches(self):
        # get API response
        response = client.get(reverse('creatematch'))
        matches = Match.objects.all()
        serializer = CreateMatchSerializer(matches, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# endpoint : '/creatematch'
class CreateMatchesByPostTest(TestCase):
    def setUp(self) -> None:
        self.category = Project.objects.create(projectName='planszufki')
        self.game = Game.objects.create(games=self.category,
                                        name='szachy',
                                        imgUrl='https://image.freepik.com/darmowe-wektory/gra-tic-tac-toe_97886-854.jpg')
        # print(self.game,self.game.id)
        self.valid_payload = {
            'game': self.game.id,
            'maxPlayers': 2,
        }
        self.invalid_payload = {
            'game': self.game.id,
            'maxPlayers': '',
        }

    def test_create_valid_match(self):
        response = client.post(reverse('creatematch'),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_match(self):
        response = client.post(reverse('creatematch'),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ActionsOnMatchesObjects(TestCase):
    def setUp(self) -> None:
        self.category = Project.objects.create(projectName='planszufki')
        self.game = Game.objects.create(games=self.category,
                                        name='kółko i krzyżyk',
                                        imgUrl='https://image.freepik.com/darmowe-wektory/gra-tic-tac-toe_97886-854.jpg')
        self.match = Match.objects.create(game=self.game,
                                          maxPlayers=2)
        self.user1 = User.objects.create(username=choice(names) + choice(numbers))
        self.user2 = User.objects.create(username=choice(names) + choice(numbers))
        self.player1 = Player.objects.create(match=self.match,
                                             playerName=self.user1)
        self.player2 = Player.objects.create(match=self.match,
                                             playerName=self.user2)
        self.randomPlayerList = [self.player1, self.player2]

    # endpoint : '/allmatches'
    def test_get_all_matches(self):
        response = client.get(reverse('allmatches'))
        matches = Game.objects.all()
        serializer = RoomSerializer(matches, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # endpoint : '/leave-match/<int:pk>'
    def test_delete_valid_player(self):
        player = choice(self.randomPlayerList)
        response = client.delete((
            reverse('leave-match', kwargs={'pk': player.pk})
        ))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_player(self):
        response = client.delete(
            reverse('leave-match', kwargs={'pk': 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_valid_player(self):
        player = choice(self.randomPlayerList)
        response = client.get(
            reverse('leave-match', kwargs={'pk': player.pk})
        )
        playerData = get_object_or_404(Player, pk=player.pk)
        serializer = PlayersSerializerDetail(playerData)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_player(self):
        player = choice(self.randomPlayerList)
        response = client.get(
            reverse('leave-match', kwargs={'pk': 30})
        )
        playerData = get_object_or_404(Player, pk=player.pk)
        serializer = PlayersSerializerDetail(playerData)
        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # endpoint : '/roomdetail/<int:pk>'
    def test_get_valid_one_match(self):
        response = client.get(
            reverse('roomdetail', kwargs={'pk': self.match.pk})
        )
        match = get_object_or_404(Match, pk=self.match.pk)
        serializer = MatchSerializer(match)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_one_match(self):
        response = client.get(
            reverse('roomdetail', kwargs={'pk': 300})
        )
        serializer = MatchSerializer(self.match)
        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # endpoint : '/matches/<int:pk>'
    def test_get_valid_game_with_type(self):
        response = client.get(
            reverse('matches', kwargs={'pk': self.game.pk})
        )
        game = get_object_or_404(Game, pk=self.game.pk)
        serializer = RoomSerializer(game)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


# endpoint : '/register
class RegisterUserInPost(TestCase):
    def setUp(self) -> None:
        self.valid_user = {
            "username": choice(names)+choice(numbers)
        }
        self.invalid_user = {
            "username": 2
        }
        self.valid = User.objects.create(username=choice(names)+choice(numbers))

    def test_register_valid_user(self):
        response = client.post(reverse('register'),
                               data=json.dumps(self.valid_user),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_register_invalid_user(self):
        response = client.post(reverse('register'),
                               data=json.dumps(self.invalid_user),
                               content_type='application/json')
        user = get_object_or_404(User, pk=self.valid.pk)
        serializer = UserSerializerGet(user)
        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # endpoint : '/users'
    def test_get_all_users(self):
        response = client.get(reverse('register'))
        users = User.objects.all()
        serializer = UserSerializerGet(users,many=True)
        self.assertEqual(response.data, serializer.data)

# endpoint : '/join-match'
class JoinMatchByPost(TestCase):
    def setUp(self) -> None:
        self.category = Project.objects.create(projectName='planszufki')
        self.game = Game.objects.create(games=self.category, name='kółko i krzyżyk',
                                        imgUrl='https://image.freepik.com/darmowe-wektory/gra-tic-tac-toe_97886-854.jpg')
        self.match = Match.objects.create(game=self.game, maxPlayers=2)
        self.user1 = User.objects.create(username=choice(names) + choice(numbers))
        self.user2 = User.objects.create(username=choice(names) + choice(numbers))

        self.valid_payload = {
            "match": self.match.pk,
            "playerName": self.user1.pk
        }
        self.invalid_payload = {
            "match": 10000000000,
            "playerName": self.user2.pk
        }

    def test_create_valid_player(self):
        response = client.post(
            reverse('join-match'),
            data=json.dumps(self.valid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_player(self):
        response = client.post(
            reverse('join-match'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)