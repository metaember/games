from player import *
from common import *
from board import *

def print_board(board):
    for row in board:
        for cell in row:
            print(cell, ' ', end=' ')
        print('\n')


def print_opponent_board(board):
    for index in range(1,len(board.index)+1):
        for col_index in range(1,len(board.columns)+1):
            cell = board.loc[index][col_index]
            if cell == 0 or cell == 1:
                print(0, ' ', end=' ')
            elif cell == 2:
                print('M', ' ', end=' ')
            elif cell == 3:
                print('T', ' ', end=' ')
            elif cell == 4:
                print('S', ' ', end=' ')
            else:
                print('error', ' ', end=' ')
        print('\n')


def get_ship_from_point(x, y, ships):
    for ship in ships:
        if x == ship.x and y == ship.y:
            return ship
        elif x == ship.x:
            if ship.direction == 'W':
                if 0 < ship.y - y < ship.size:
                    return ship
            elif ship.direction == 'E':
                if 0 < y - ship.y < ship.size:
                    return ship
        elif y == ship.y:
            if ship.direction == 'N':
                if 0 < ship.x - x < ship.size:
                    return ship
            elif ship.direction == 'S':
                if 0 < x - ship.x < ship.size:
                    return ship
    return Ship(-1, -1, 0, None)


def turn_board_cells_to_sunk(ship, board):
    if ship.direction == 'N':
        for i in range(ship.size):
            board.loc[ship.x - i][ship.y] = 4
    elif ship.direction == 'S':
        for i in range(ship.size):
            board.loc[ship.x + i][ship.y] = 4
    elif ship.direction == 'W':
        for i in range(ship.size):
            board.loc[ship.x][ship.y - i] = 4
    elif ship.direction == 'E':
        for i in range(ship.size):
            board.loc[ship.x][ship.y + i] = 4


def place_ships(ship_sizes, myboard, player, display=True):
    print("Placing {} ships. The sizes are : {}".format(len(ship_sizes) + 1, ship_sizes))
    for shipNb, shipSize in enumerate(ship_sizes):
        print("Please place ship number {} of size {} :".format(shipNb, shipSize))
        success = False
        while not success:
            try:
                sh = Ship(owner = player, size=shipSize)
                sh.add_to_board(myboard.board)
            except PlacementError:
                print("Placement Error: The ship can't fit here! Try again ...")
            else:
                success = True

        if display:
            myboard.disp()


def throw_missile(boardc, ships):
    board = boardc.board
    print('This is the opponent\'s board:', end='\n\n')
    print_opponent_board(board)
    x_fire = -1
    y_fire = -1
    while x_fire < 0 or x_fire > len(board.index):
        x_fire = int(input("Where do you want to fire on the x axis ?"))
    while y_fire < 0 or y_fire > len(board.columns):
        y_fire = int(input("Where do you want to fire on the y axis ?"))
    if board.loc[x_fire][y_fire] == 0:
        board.loc[x_fire][y_fire] = 2
        print('Missed')
    elif board.loc[x_fire][y_fire] == 1:
        board.loc[x_fire][y_fire] = 3
        print('Touched')
        current_ship = get_ship_from_point(x_fire, y_fire, ships)
        current_ship.touch(max(abs(current_ship.x-x_fire), abs(current_ship.y-y_fire)))
        if current_ship.is_sunk():
            turn_board_cells_to_sunk(current_ship, board)
            print('Sunk')
    print('This is the updated opponent\'s board:', end='\n\n')
    print_opponent_board(board)


board_test = [[1, 0, 2, 3, 1], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 1, 1, 1], [0, 0, 0, 0, 0]]
ships = [Ship(0, 0, 4, 'S')]

# a = get_ship_from_point(1, 1, ships)

# print(a.size, a.direction)

# print(print_board(board_test))

# print_opponent_board(board_test)
# throw_missile(board_test, ships)

def initialize_players():
    player1_name = input('What is the first player\'s name?')
    player2_name = input('What is the second player\'s name?')

    player1 = Player(player1_name)
    player2 = Player(player2_name)

    print('{}, place your ships'.format(player1.name))
    player1.board = Board()
    place_ships(SHIPS, player1.board, player1)
    player1.ships = [sh for sh in Ship.members if sh.owner == player1]
    player1.board.transform_board()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    print('{}, place your ships'.format(player2.name))
    player2.board = Board()
    place_ships(SHIPS, player2.board, player2)
    player2.ships = [sh for sh in Ship.members if sh.owner == player2]
    player2.board.transform_board()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    return (player1, player2)


def start_game():

    (p1, p2) = initialize_players()

    i = 0
    game_over = False
    winner = "No one"
    while not game_over:
        if i % 2 == 0:
            print(p1.name, ', where do you want to throw a missile?')
            throw_missile(p2.board, p2.ships)
            if all_ships_sunk(p2.ships):
                game_over = True
                winner = p1.name
            i+=1
        elif i % 2 == 1:
            print(p2.name, ', where do you want to throw a missile?')
            throw_missile(p1.board, p1.ships)
            if all_ships_sunk(p1.ships):
                game_over = True
                winner = p2.name
            i+=1

    print('Game is over, {} won'.format(winner))


def all_ships_sunk(ships):
    res = True
    for ship in ships:
        if not ship.is_sunk():
            res = False
            break
    return res
