from channels.generic.websocket import WebsocketConsumer
from django.test import TestCase
from ..game_logic.tictactoe import TicTacToe, State
import json

states = json.load(open('board_game/tests/states_to_test.json'))


class CheckRows(TestCase):
    def setUp(self) -> None:
        self.winingRows = states['rows']['win']
        self.notWinningRows = states['rows']['lose']

    def test_is_winner_in_row(self):
        for test in self.winingRows:
            isWinner = TicTacToe(test).check_rows()
            self.assertEqual(type(isWinner), str)

    def test_is_not_winner_in_row(self):
        for test in self.notWinningRows:
            isNotWinner = TicTacToe(test).check_rows()
            self.assertEqual(isNotWinner, False)


class CheckColumns(TestCase):
    def setUp(self) -> None:
        self.winingColumn = states['columns']['win']
        self.notWinningColumn = states['columns']['lose']

    def test_is_winner_in_column(self):
        for test in self.winingColumn:
            isWinner = TicTacToe(test).check_columns()
            self.assertEqual(type(isWinner), str)

    def test_is_not_winner_in_column(self):
        for test in self.notWinningColumn:
            isNotWinner = TicTacToe(test).check_columns()
            self.assertEqual(isNotWinner, False)


class CheckDiag(TestCase):
    def setUp(self) -> None:
        self.winingColumn = states['diagonal']['win']
        self.notWinningColumn = states['diagonal']['lose']

    def test_is_winner_in_diag(self):
        for test in self.winingColumn:
            isWinner = TicTacToe(test).check_diag()
            self.assertEqual(type(isWinner), str)

    def test_is_not_winner_in_diag(self):
        for test in self.notWinningColumn:
            isNotWinner = TicTacToe(test).check_diag()
            self.assertEqual(isNotWinner, False)


class CheckWinner(TestCase):
    def setUp(self) -> None:
        state = states['winerIsKnow']
        for key, value in state.items():
            winner = TicTacToe(key).run()
            self.assertEqual(winner, value)


class SimpleStateTest(TestCase):
    def setUp(self) -> None:
        oldState = "XXX-O-X--"
        newState = "XXX-O-X-O"
        self.checkState = State(oldState, newState)

    def test_there_was_one_move(self):
        oneMove = self.checkState.check_move()
        self.assertEqual(oneMove, True)
