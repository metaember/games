SYMBOL = ("X", "O")

class Grid :
    def __init__(self):
        self.grid = [[None, None, None] for x in range(3)]

    def display(self):
        for row in self.grid:
            for cell in row:
                print(cell, end= " ")


def main():
    stillPlaying = True
    player_one_turn = True
    while stillPlaying:
        player = "player 1" if player_one_turn else "player 2"
        symbol = SYMBOL[0] if player_one_turn else SYMBOL[1]
        print("It's {}'s turn. You play {}".format(player, symbol))


        player_one_turn = not player_one_turn


if __name__ == "__main__":
    main()
