from ship import *

class Player ():

    def __init__(self, name=None, ships=None, board=None, ranking=None):
        self.name = name
        self.ships = ships
        self.board = board
        self.ranking = ranking

        if self.name is None:
            self.name = input("\tWhat's your name? ")
