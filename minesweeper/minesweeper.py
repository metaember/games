import numpy as np
import itertools

SEEN = "."
UNSEEN = "#"
FLAG = "F"


class Square:
    def __init__(self, isMine = False, isSeen = False, isFlag = False, val=0):
        self.isMine = isMine
        self.isSeen = isSeen
        self.isFlag = isFlag
        self.val = val

    def __str__(self):
        if self.isSeen:
            return str(self.val) if self.val > 0 else SEEN
        elif self.isFlag:
            return FLAG
        else:
            return UNSEEN

    def disp(self):
        if self.isMine:
            return "M"
        else:
            return str(self.val) if self.val > 0 else SEEN




class Minesweeper:
    def __init__(self, size, nb_mines):
        self.size = size
        self.nb_mines = nb_mines
        self.map = [[Square() for _a in range(self.size)] for _b in range(self.size)]
        self.explored = set()

    def gen_mines(self, init_x, init_y):
        mine_xloc = list(np.random.choice(range(self.size), self.nb_mines))
        mine_yloc = list(np.random.choice(range(self.size), self.nb_mines))
        mine_locs = set(zip(mine_xloc, mine_yloc))

        iteration = 0
        tries = 1000000
        initial_n = set(self.get_neighbors(init_x, init_y) + [init_x, init_y])

        while (len(initial_n.intersection(mine_locs)) > 0 or len(mine_locs) < self.nb_mines) and iteration<tries:
            mine_xloc = list(np.random.choice(range(self.size), self.nb_mines))
            mine_yloc = list(np.random.choice(range(self.size), self.nb_mines))
            mine_locs = set(zip(mine_xloc, mine_yloc))
            iteration+=1

        if iteration == tries:
            print("failed to generate a good map within {} iterations".format(tries))
            raise Exception


        for i in range(self.nb_mines):
            selected = self.map[mine_yloc[i]][mine_xloc[i]]
            selected.isMine = True
            for (y,x) in self.get_neighbors(mine_yloc[i],mine_xloc[i]):
                self.map[y][x].val += 1


    def get_neighbors(self,x,y):
        if x < 0 or x > self.size or y < 0 or y > self.size:
            raise ValueError
        x_vals = [x+i for i in (-1,0,1) if 0 <= x+i < self.size]
        y_vals = [y+i for i in (-1,0,1) if 0 <= y+i < self.size]

        neighbors = list(itertools.product(x_vals, y_vals))
        neighbors.remove((x,y))
        return neighbors

    def disp(self, hidden=True):
        for row in range(self.size):
            print(row, "|", end = " ")
            for col in range(self.size):
                if hidden:
                    print(self.map[row][col], end = " ")
                else:
                    print(self.map[row][col].disp(), end = " ")
            print()
        print("    "+"--"*self.size)
        print("    "+" ".join(list(map(str, list(range(self.size))))))

    def explore(self,x,y):
        self.explored.add((x,y))
        sq = self.map[y][x]
        if not sq.isMine:
            sq.isSeen = True
            if sq.val == 0:
                for n in self.get_neighbors(x,y):
                    if n not in self.explored:
                        self.explore(*n)


    def play(self):
        gameover = False
        print()
        self.disp()
        firstClick = True

        while not gameover:
            query = input("Query ?")
            self.explored = set()
            if query == 'q':
                print("Goodbye")
                self.disp(False)
                break
            else:
                command, x, y = query.split()
                x = int(x)
                y = int(y)

                if command == 'f':
                    if self.map[y][x].isSeen:
                        print("already seen")
                    else:
                        self.map[y][x].isFlag = not self.map[y][x].isFlag

                elif command == 'c':
                    if firstClick:
                        self.gen_mines(x,y)
                        firstClick = False
                    if self.map[y][x].isFlag:
                        print("Careful, that square is flagged!")
                        continue
                    elif self.map[y][x].isMine:
                        print("BOOM! You die...")
                        gameover = True
                        self.disp(False)
                        break
                    elif self.map[y][x].isSeen:
                        print("You explored that square already")
                    else:
                        self.explore(x,y)

                else:
                    print("Unrecognized command")

            self.disp()
            print()


if __name__ == "__main__":
    M = Minesweeper(8,10)
    M.disp(False)
    M.play()
