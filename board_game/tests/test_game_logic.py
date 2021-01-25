from django.test import TestCase
from ..game_logic.tictactoe import TicTacToe, State
import json

# data with states to test
states = json.load(open('board_game/tests/states_to_test.json'))


class CheckRows(TestCase):
    def setUp(self) -> None:
        self.winingRows = states['rows']['win']
        self.notWinningRows = states['rows']['notWin']

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
        self.notWinningColumn = states['columns']['notWin']

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
        self.notWinningColumn = states['diagonal']['notWin']

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
        self.state = states['winerIsKnow']

    def test_value_from_game_equal_to_state_winner(self):
        for key, value in self.state.items():
            winner = TicTacToe(key).run()
            self.assertEqual(winner, value)


class StateOneMoveTests(TestCase):
    def setUp(self) -> None:
        state = states['checkState']
        self.oldStateOneMove = state['oneMove']['oldState']
        self.oldStateNotOneMove = state['notOneMove']['oldState']
        self.newStateOneMove = state['oneMove']['newState']
        self.newStateNotOneMove = state['notOneMove']['newState']

    def test_there_was_one_move(self):
        for old,new in zip(self.oldStateOneMove,self.newStateOneMove):
            oneMove = State(old,new).check_move()
            self.assertEqual(oneMove, True)

    def test_there_wasnt_one_move(self):
        for old,new in zip(self.oldStateNotOneMove,self.newStateNotOneMove):
            oneMove = State(old,new).check_move()
            self.assertEqual(oneMove, False)

class StateFinishedGameTests(TestCase):
    def setUp(self) -> None:
        state = states['checkState']
        self.oldStateFinished = state['finished']['oldState']
        self.oldStateNotFinished = state['notFinished']['oldState']
        self.newStateFinished = state['finished']['newState']
        self.newStateNotFinished = state['notFinished']['newState']

    def test_game_is_finished(self):
        for old,new in zip(self.oldStateFinished,self.newStateFinished):
            finished = State(old,new).check_finished()
            self.assertEqual(finished,True)

    def test_game_is_not_finished(self):
        for old,new in zip(self.oldStateNotFinished,self.newStateNotFinished):
            finished = State(old,new).check_finished()
            self.assertEqual(finished,False)


class StateFieldChangedTest(TestCase):
    def setUp(self) -> None:
        state = states['checkState']
        self.oldStateChangeField = state['changedField']['oldState']
        self.oldStateNotChangeField = state['notChangedField']['oldState']
        self.newStateChangeField = state['changedField']['newState']
        self.newStateNotChangeField = state['notChangedField']['newState']

    def test_gamer_change_enemy_field(self):
        for old,new in zip(self.oldStateChangeField,self.newStateChangeField):
            changed = State(old,new).check_blank()
            self.assertEqual(changed,False)

    def test_gamer_didnt_change_enemy_field(self):
        for old, new in zip(self.oldStateNotChangeField, self.newStateNotChangeField):
            changed = State(old, new).check_blank()
            self.assertEqual(changed, True)