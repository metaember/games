import argparse

import numpy as np
import curses
from collections import deque
import time
import random

parser = argparse.ArgumentParser(description='Play Snake!\n At any time press `q` to quit!')
parser.add_argument('-d', '--difficulty', help="Difficulty", choices = ('easy', 'med', 'hard'), required=False, default='med')
args = parser.parse_args()


class CONST :
    diff = {'easy': 400, 'med': 200, 'hard': 100}
    init_len = 3
    time_increment = diff[args.difficulty]
    board_size = 20

class CollisionError (Exception):
    def __init__ (self):
        pass


class Food():
    def __init__(self, win, snake):
        self.win = win
        self.snake = snake
        self.pos = None
        self.new()

    def new(self):
        outside_snake = False
        while not outside_snake:
            x = random.randint(1, CONST.board_size-2)
            y = random.randint(1, CONST.board_size-2)
            pos = (x,y)

            if pos not in self.snake.pos:
                outside_snake = True
                self.pos = pos
                self.win.addch(y, x, ord('O'))


    def remove(self):
        if self.pos is not None:
            self.win.addch(self.pos[1], self.pos[0], ord(' '))
        else:
            return

    def eat (self):
        self.remove()
        self.new()


class Snake():
    def __init__(self, win):
        self.pos = deque()
        self.win = win
        self.food = None

    def associate_food(self, food):
        self.food = food

    def score(self):
        return len(self.pos) + 1

    def init_snake(self):
        self.pos = deque()
        self.pos.append((4,5))
        self.pos.append((5,5))
        self.pos.append((6,5))

        for p in self.pos:
            self.win.addch(p[1], p[0], ord('X'))


    def move(self, dx, dy):

        curr = self.pos[-1]
        #print(curr, self.food.pos)

        next_pos = (curr[0]+dx, curr[1]+dy) #this will be the next square

        if self.food is not None and next_pos == self.food.pos:
            print("Yum!")
            self.food.eat()
        else:
            # do not grow
            to_remove = self.pos.popleft() # remove the last item of the tail
            self.win.addch(to_remove[1],to_remove[0], ord(' '))

        if next_pos in self.pos:
            curses.flash()
            return "Collision with self!"

        if next_pos[0] in (0, CONST.board_size-1) or next_pos[1] in (0, CONST.board_size-1):
            curses.flash()
            return "Collision with board sides!"


        self.pos.append(next_pos)
        self.win.addch(next_pos[1], next_pos[0], ord('X'))
        return None



# board = np.ndarray((CONST.board_size,CONST.board_size))

def main (stdscr):
    dx = 1
    dy = 0


    begin_x = 1
    begin_y = 1
    height = CONST.board_size
    width = CONST.board_size
    win = curses.newwin(height, width, begin_y, begin_x)

    #init the window
    stdscr.timeout(CONST.time_increment)
    #stdscr.nodelay(True)
    win.clear()
    win.box(0,0)
    win.refresh()

    Sn = Snake(win)
    Sn.init_snake()

    food = Food(win, Sn)
    Sn.associate_food(food)



    turn = 0
    alive = True
    while alive:
        turn += 1

        win.box(0,0)

        c = stdscr.getch()
        if c == ord('q'):
            break  # Exit the while()
        elif c == curses.KEY_UP:
            dx = 0
            dy = -1
        elif c == curses.KEY_DOWN:
            dx = 0
            dy = 1
        elif c == curses.KEY_RIGHT:
            dx = 1
            dy = 0
        elif c == curses.KEY_LEFT:
            dx = -1
            dy = 0
        #elif c == -1:
            #print("nothing")

        status = Sn.move(dx,dy)
        win.move(0,0)
        win.refresh()

        if status is not None:
            alive = False
            win.addstr(0,0,status)
            win.addstr(1,0,"Survived {} turns.".format(turn))
            win.addstr(2,0,"Snake length {}.".format(Sn.score()))
            win.addstr(3, 0, "Press any key!")

    c = win.getch()



curses.wrapper(main)
