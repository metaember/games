from random import choice
import os
import curses
#import curses.ascii

HIDDEN_LETTER = "_"

file_name = 'word_dictionary.txt'




def load_words():
    file_path = os.path.join('hangman', file_name)
    with open(file_path, 'r') as fp:
        data = fp.read()

    words = data.splitlines()
    words = list(filter(None, words))  # Remove empty strings
    return words


def disp_in_win(win, text, autocut = True, delay = 0):
    nb_lines = win.getmaxyx()[0]-2
    max_len = win.getmaxyx()[1]-2 #-2 because border on each side

    if len(text) > nb_lines * max_len:
        raise ValueError("Text too long to print on {} lines!".format(nb_lines))

    if autocut:
        # cut along the newline chars
        text_list = text.split("\n")
        if len(text_list) > nb_lines:
            raise ValueError("Too many lines to fit!")

        for line in text_list:
            if len(line) > max_len:
                raise ValueError("One of the lines ({}) is too long to print ({} > {})".format(line, len(line), max_len))

    else:
        # cut text into max_len length pieces
        text_list = [text[i*max_len:(i+1)*max_len] for i in range(nb_lines)]

    for i in range(nb_lines):
        win.addstr(i+1,1," " * max_len)  #erase everything on line i +1 because of border
        if i < len(text_list): # stop trying to write if the text has less lines than window
            win.addstr(i+1,1,text_list[i].strip()) # Write correct piece

    win.refresh()
    if delay > 0:
        curses.napms(delay)
    return None

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def main(stdscr, word):

    stdscr.box(0,0)
    stdscr.refresh()

    window_width = 70
    mess_win = curses.newwin(4, window_width, 1, 1) # Message window
    mess_win.box(0,0)
    mess_win.refresh()

    text_win = curses.newwin(3, window_width, 5, 1) # Window with word
    text_win.box(0,0)
    text_win.refresh()

    pic_win = curses.newwin(9, 11, 1, 73) # Window with word
    pic_win.box(0,0)
    pic_win.refresh()


    wordfound = [HIDDEN_LETTER for letter in word]
    stillPlaying = True
    lettersTried = set()
    lives = 10

    disp_in_win(mess_win,"You have {} lives left.".format(lives))

    while stillPlaying:


        disp_in_win(text_win,"Word so far : {}".format(' '.join(wordfound)))
        #disp_in_win(pic_win, "Hangman")
        print_pic(pic_win, 10-lives)
        stdscr.move(0,0)

        letter = ''
        # make robust
        while not (letter.isalpha() and is_ascii(letter)):
            c = stdscr.getch()
            if c == ord('!') or c== ord("1"):
                stillPlaying = False
                return
            else:
                letter = chr(c)
                if not is_ascii(letter) or not letter.isalpha():
                    disp_in_win(mess_win,"You typed `{}`. Please enter a valid letter!".format(letter))

        letter = letter.upper()

        if letter in lettersTried:
            disp_in_win(mess_win, "You already tried letter : {}. Select another.\n"
                "(You have tried : {})".format(letter, ", ".join(sorted(lettersTried))))
            continue
        else :
            lettersTried.add(letter)

        if letter in word:
            for i, l in enumerate(word):
                if l == letter:
                    wordfound[i] = l
            disp_in_win(mess_win,"Correct! The letter {} is indeed in the hidden word! \n"
                                    "You have {} lives left.".format(letter, lives))
            if HIDDEN_LETTER not in wordfound:
                stillPlaying = False
                disp_in_win(mess_win,"You win! The word was {}. You had {} lives left!".format(word, lives))
                break

        else :
            lives -= 1
            disp_in_win(mess_win,"The letter {} is not in the hidden word.\n You loose a life. "
                                        "Lives left : {}.".format(letter, lives))
            if lives == 0:
                stillPlaying = False
                disp_in_win(mess_win,"You ran out of lives ! GAME OVER."
                            "The hidden word was {}\n Press any key to quit.".format(word))
                print_pic(pic_win, 10-lives)
                c = stdscr.getch() # in order to delay the quit
                break



hangman_pic = {
    0 : ["","","","","","",""],
    1 : ["","","","","",""," ________"],
    2 : ["", "|", "|", "|", "|", "|","|________" ],
    3 : ["______", "|", "|", "|", "|", "|","|________" ],
    4 : ["______", "|     |", "|", "|", "|", "|","|________" ],
    5 : ["______", "|     |", "|     0", "|", "|", "|","|________" ],
    6 : ["______", "|     |", "|     0", "|     |", "|     |", "|","|________" ],
    7 : ["______", "|     |", "|     0", "|     |", "|     |", "|    /","|________" ],
    8 : ["______", "|     |", "|     0", "|     |", "|     |", "|    / \\","|________" ],
    9 : ["______", "|     |", "|     0", "|    /|", "|     |", "|    / \\","|________" ],
    10 : ["______", "|     |", "|     0", "|    /|\\", "|     |", "|    / \\","|________" ]
}

def print_pic(win, level):
    to_draw = hangman_pic[level]
    for i in range(len(to_draw)):
        win.addstr(i+1,1,to_draw[i])

    win.refresh()





WORDS = load_words()
curses.wrapper(lambda x: main(x,choice(WORDS)))
