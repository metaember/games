from random import randint
import os
import curses
import numpy as np


def get_random (table):
    """ THIs has a bug"""
    # count empty slots
    tab = table.flatten()
    count = 0
    for item in tab:
        if item == 0:
            count += 1

    # choose one at random
    selected = randint(0,count-1)

    # fill it with at random 1 or 2
    count = 0
    index = None
    for idx, item in enumerate(tab):
        if item == 0:
            count += 1
            if count == selected:
                index = idx
                break

    tab[index] = randint(1,2)
    ans = np.reshape(tab, (4,4))
    return ans

def table_to_row (table, direction):
    if direction == curses.KEY_UP:
        ans = [table[:i:-1] for i in range(4)]

def move(table, direction):
    """ Returns a table after the move has been completed"""
    return table


    # Get the columns / rows in the right direction



    # Perform reduction


def disp(table, win):
    for y in range (1,5):
        for x in range(1,5):
            char = table[x-1, y-1]
            if char == 0:
                char = " "
            else:
                char = str(char)
            win.addstr(y,x,char)
    win.refresh()




def main (stdscr):
    stdscr.box(0,0)
    stdscr.refresh()

    win_width = 6
    win_height = 6
    game_win = curses.newwin(win_height, win_width, 1, 1) # Message window
    game_win.box(0,0)
    game_win.refresh()

    stillPlaying = True

    table = np.array([[0]*4]*4)
    turn = 0
    # make robust
    while stillPlaying:
        disp(table, game_win)
        letter = ''
        while letter not in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
            letter = stdscr.getch()
            if letter == ord('q'):
                stillPlaying = False
                return
        table = move(table, letter)
        table = get_random(table)
        turn += 1






curses.wrapper(main)
