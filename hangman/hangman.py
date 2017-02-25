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


def disp_in_win(win, text, wait = True):
    nb_lines = win.getmaxyx()[0]-2
    max_len = win.getmaxyx()[1]-2 #-2 because border on each side

    if len(text) > 2 * max_len:
        raise ValueError("Text too long to print on {} lines!".format(nb_lines))

    # cut text into max_len length pieces
    text_list = [text[i*max_len:(i+1)*max_len] for i in range(nb_lines)]

    for i in range(nb_lines):
        win.addstr(i+1,1," " * max_len)  #erase everything on line i +1 because of border
        win.addstr(i+1,1,text_list[i]) # Write correct piece

    win.refresh()
    if wait:
        curses.napms(1500)
    return None

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





    wordfound = [HIDDEN_LETTER for letter in word]
    stillPlaying = True
    lettersTried = set()
    lives = 10



    while stillPlaying:
        disp_in_win(mess_win,"You have {} lives left.".format(lives), False)
        disp_in_win(text_win,"Word so far : {}".format(' '.join(wordfound)), False)

        letter = ''
        # make robust
        c = stdscr.getch()
        if c == ord('!') or c== ord("1"):
            stillPlaying = False
            break  # Exit the while()
        else:
            letter = chr(c)
            disp_in_win(mess_win,"You typed {}".format(letter))
            #continue

        letter = letter.upper()

        if letter in lettersTried:
            disp_in_win(mess_win, "You already tried letter : {}. Select another. (You have tried : {})".format(letter, ", ".join(sorted(lettersTried))))
            continue
        else :
            lettersTried.add(letter)

        if letter in word:
            for i, l in enumerate(word):
                if l == letter:
                    wordfound[i] = l
            disp_in_win(mess_win,"Correct! The letter {} is indeed in the hidden word!".format(letter))
            if HIDDEN_LETTER not in wordfound:
                stillPlaying = False
                disp_in_win(mess_win,"You win! The word was {}. You had {} lives left!".format(word, lives))
                break

        else :
            lives -= 1
            disp_in_win(mess_win,"The letter {} is not in the hidden word. You loose a life. Lives left : {}.".format(letter, lives))
            if lives == 0:
                stillPlaying = False
                disp_in_win(mess_win,"You ran out of lives ! GAME OVER. The hidden word was {}".format(word))
                break





WORDS = load_words()
curses.wrapper(lambda x: main(x,choice(WORDS)))
