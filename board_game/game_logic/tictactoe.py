from re import fullmatch, search, findall

wins = {
    'columns': {
       'X..X..X': 'X',
       'O..O..O': 'O',
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


class State:
    def __init__(self, old_state, new_state):
        self.new_state = new_state
        self.old_state = old_state

    def check_move(self):
        num_dif = sum(i != j for i, j in zip(self.new_state, self.old_state))
        if num_dif == 1:
            return True
        elif num_dif > 1:
            return False

    def check_finished(self):
        return '-' not in self.new_state

    def check_blank(self):
        if self.check_move() and not self.check_finished():
            for idx, (item_o, item_n) in enumerate(zip(self.old_state, self.new_state)):
                if item_n != item_o and item_o not in 'XO':
                    print(f'Field {idx} was changed from {item_o} to {item_n}')
                    return True
                elif item_n != item_o and item_o in 'XO':
                    print('Some tried to change other user\'s field')
                    return False
        else:
            return False

    def check_mark(self):
        for idx, (item_o, item_n) in enumerate(zip(self.old_state, self.new_state)):
            if item_n != item_o and item_o not in 'XO':
                return item_n


class TicTacToe:

    def __init__(self, state):
        self.state = list(state)

    def check_finished(self):
        return '-' not in self.state

    def check_columns(self):
        columns = wins['columns']
        try:
            index = \
                [index for index, value in enumerate([(search(t, ''.join(self.state))) for t in columns.keys()]) if
                 value][0]
            winner = columns[list(columns.keys())[index]]
            return winner
        except IndexError:
            return False

    def check_rows(self):
        rows = wins['rows']
        state = ''.join(self.state)
        for winnerState in rows.keys():
            if winnerState in findall('...?',state):
                return rows[winnerState]
        return False


    def check_diag(self):
        columns = wins['diagonal']
        try:
            index = \
                [index for index, value in enumerate([(fullmatch(t, ''.join(self.state))) for t in columns.keys()])
                 if
                 value][0]
            winner = columns[list(columns.keys())[index]]
            return winner
        except IndexError:
            return False

    def run(self):
        logic = [self.check_rows, self.check_columns, self.check_diag]
        for i in logic:
            value = i()
            if value:
                return value








