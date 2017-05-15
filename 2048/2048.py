from random import randint
import os
import curses
import numpy as np


def get_random (table):
    """ Places a random 1 or 2 in an empty square of the table"""
    # count empty slots
    tab = table.flatten()
    count = 0
    for item in tab:
        if item == 0:
            count += 1

    if count == 0:
        # No empty squares, we return None
        return table

    # choose one at random
    selected = randint(1,count)

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


def reduce_row(row):
    """ reduces one row, in the direction end --> start of list"""
    # remove empty space below
    while 0 in row:
        row.remove(0)

    # combine numbers if possible
    idx = 0
    end = len(row)
    while idx < end:
        if idx < end-1 and row[idx] == row [idx+1] != 0:
            row.pop(idx) #remove item at idx
            row[idx] += 1
            end -= 1
        idx += 1

    # repad with 0's on the other end
    row = row +[0]*(4-len(row))
    return row

def move(table, direction):
    """ Returns a table after the move has been completed"""
    rotations = {curses.KEY_DOWN: 3, curses.KEY_UP: 1, curses.KEY_LEFT:0, curses.KEY_RIGHT:2}

    k = rotations[direction]
    rotated = np.rot90(table, k) # flip to have the  "down" pointing left (so each row is correctly aligned)
    rot_reduced = []
    for r in rotated:
        rot_reduced.append(reduce_row(r.tolist()))


    ans = np.array(rot_reduced)
    ans = np.rot90(ans, -k)

    return ans


    # Get the columns / rows in the right direction



    # Perform reduction


def disp(table, win):
    for y in range (1,5):
        for x in range(1,5):
            char = table[y-1, x-1]
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
        table_new = get_random(table)
        if table_new is table:
            # Todo: move cursor to display this text lower
            print("No empty squares: game is over! You survived {} turns, with a score of {}. Press any key to quit.".format(turn, table.max()))
            stdscr.getch()
            return
        else:
            table = table_new
            turn += 1






curses.wrapper(main)
