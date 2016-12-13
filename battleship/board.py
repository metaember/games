from common import *


class Board:

    def __init__(self, size=10):
        self.size = size
        edge = list(range(0, size + 2))
        self.board = pd.DataFrame(columns=edge, index=edge, data=".")
        self.board.loc[1:self.size, 1:self.size] = ""

    def disp(self, show_border=False):
        if show_border:
            print(self.board)
        else:
            print(self.board.loc[1:self.size, 1:self.size])
        return None

    def transform_board (self):
        self.board = self.board.loc[1:self.size, 1:self.size].applymap(lambda x: 1 if x == "X" else 0)