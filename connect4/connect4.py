import numpy as np
from random import choice

class Grid:
    SYMBOLS = (".","X","O")
    def __init__(self, width = 7, height = 7):
        self.width = width
        self.height = height
        self.grid = np.zeros((7,7))
        self.WIN_MIN = 4


    def display(self):
        for row in self.grid:
            print("\t| " , end = '')
            for item in row:
                print(Grid.SYMBOLS[int(item)], end=' ')
            print("|", end = '')
            print()

    def place(self, col, val):
        column = self.grid[:,col]
        for i in range(self.height):
            if self.grid[self.height-i-1,col] == 0:
                self.grid[self.height-i-1,col] = val
                return (self.height-i-1, col)

    def check_win(self, row, col):
        player = self.grid[row,col]
        directions = [(1,0), (1,1), (0,1), (1,-1)] # since directions are bidirectional, we only need 4 not 8
        for increments in directions:
            curr_conseq = self.check_win_dir(row, col, *increments)
            curr_conseq += self.check_win_dir(row, col, -increments[0], -increments[1])
            curr_conseq -= 1
            if curr_conseq >= self.WIN_MIN:
                return True
        return False

    def check_win_dir(self, row, col, increment_row = 0, increment_col = 0):
        count = 0
        player = self.grid[row,col]

        while 0 <= row < self.height and 0 <= col < self.width and \
                self.grid[row,col] == player and count <= self.WIN_MIN:
                row += increment_row
                col += increment_col
                count += 1

        return count

print("Welcome to connect four. Please enter the player names!")
g = Grid()

player1 = input("Please enter the neame of the first player ... ")
player1 = "player 1" if player1 is "" else player1
player2 = input("Now enter the neame of the second player ... ")
player2 = "player 2" if player2 is "" else player2
players = (player1, player2)

print("{} is playing {} and {} is playing {}".format(player1,Grid.SYMBOLS[1],player2,Grid.SYMBOLS[2]))

won = False
turn  = 0
while won is False:
    print("Turn {}, {} is playing.".format(turn, players[turn % 2]))
    valid_input = False
    while not valid_input:
        g.display()
        try:
            played_col = int(input("What column to play? "))
        except ValueError:
            print("Please enter a column number between 1 and {}".format(g.width))
        else:
            if not (1 <= played_col <= g.width):
                print("Please enter a column number between 1 and {}".format(g.width))
            elif g.grid[0][played_col - 1] != 0:
                print("Column {} is full, please play another".format(played_col))
            else:
                valid_input = True
                played_col -= 1


    (x,y) = g.place(played_col, turn % 2 + 1)
    if g.check_win(x,y):
        g.display()
        print("Player {} has won!".format(players[int(g.grid[x,y]) - 1]))
        won = True


    turn += 1
