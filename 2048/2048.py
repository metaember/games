from random import choice
import os
import curses
import numpy as np


def table_to_row (table, direction):
    if direction == curses.KEY_UP:
        ans = [table[:i:-1] for i in range(4)]

def move(table, direction):
    """ Returns a table after the move has been completed"""



    # Get the columns / rows in the right direction



    # Perform reduction


def disp(table, win):
    for y in range (1,5):
        for x in range(1,5):





def main (stdscr):
    stdscr.box(0,0)
    stdscr.refresh()

    win_width = 6
    win_height = 6
    game_win = curses.newwin(win_height, win_width, 1, 1) # Message window
    game_win.box(0,0)
    game_win.refresh()

    stillPlaying = True
    letter = ''
    table = np.array([[0]*4]*4)
    # make robust
    while stillPlaying:
        disp(table, win)
        while letter not in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
            c = stdscr.getch()
            if c == ord('q'):
                stillPlaying = False
                return
        table = move(table, c)






curses.wrapper(main)
