
from re import fullmatch, search


class TicTacToe:
    wins = {
        'columns': {
            'X..X..X..': 'X',
            'O..O..O..': 'O',
            '.X..X..X.': 'X',
            '.O..O..O.': 'O',
            '..X..X..X': 'X',
            '..O..O..O': 'O',
        },
        'rows': {
            'XXX': 'X',
            'OOO': 'O',
        },
        'diagonal': {
            'X...X...X': 'X',
            'O...O...O': 'O',
            '..X.X.X..': 'X',
            '..O.O.O..': 'O',
        }
    }

    def __init__(self, old_state, new_state):
        self.new_state = list(new_state)
        self.old_state = list(old_state)


    def check_move(self):
        num_dif = sum(i != j for i, j in zip(self.new_state, self.old_state))
        if  num_dif == 1:
            return True
        elif num_dif>1:
            return False


    def check_finished(self):
        return '_' not in self.new_state

    def check_columns(self):
        columns = self.wins['columns']
        try:
            index = \
                [index for index, value in enumerate([(fullmatch(t, ''.join(self.old_state))) for t in columns.keys()])
                 if
                 value][0]
            winner = columns[list(columns.keys())[index]]
            return winner
        except IndexError:
            return False

    def check_rows(self):
        columns = self.wins['rows']
        try:
            index = \
                [index for index, value in enumerate([(search(t, ''.join(self.old_state))) for t in columns.keys()]) if
                 value][0]
            winner = columns[list(columns.keys())[index]]
            return winner
        except IndexError:
            return False

    def check_diag(self):
        columns = self.wins['diagonal']
        try:
            index = \
                [index for index, value in enumerate([(fullmatch(t, ''.join(self.old_state))) for t in columns.keys()])
                 if
                 value][0]
            winner = columns[list(columns.keys())[index]]
            return winner
        except IndexError:
            return False

    def check_blank(self):
        if self.check_move() and not self.check_finished():
            for idx, (item_o, item_n) in enumerate(zip(self.old_state, self.new_state)):
                if item_n != item_o and item_o not in 'XO':
                    print(f'Zmiana {idx} pola z {item_o} na {item_n}')
                    return True
                elif item_n != item_o and item_o in 'XO':
                    print('Próba zmiany Pola innego usera')
                    return False
        else:
            return False

    def run(self):
        logic = [self.check_rows, self.check_columns, self.check_diag]
        if self.check_blank():
            for i in logic:
                value = i()
                if value:
                    return value


