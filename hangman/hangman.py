from random import choice
HIDDEN_LETTER = "_"

file_name = 'word_dictionary.txt'

def load_words():
    with open(file_name, 'r') as fp:
        data = fp.read()

    words = data.splitlines()
    words = list(filter(None, words))  # Remove empty strings
    return words


def main(word):
    wordfound = [HIDDEN_LETTER for letter in word]
    stillPlaying = True
    lettersTried = set()
    lives = 10

    while stillPlaying:
        print("You have {} lives left. Word so far : {}".format(lives, ' '.join(wordfound)))
        letter = ''
        while len(letter) != 1 :
            letter = input("Choose a letter : ")

        letter = letter.upper()

        if letter in lettersTried:
            print("You already tried letter : {}. Select another. (You have tried : {})".format(letter, ", ".join(sorted(lettersTried))))
            continue
        else :
            lettersTried.add(letter)

        if letter in word:
            for i, l in enumerate(word):
                if l == letter:
                    wordfound[i] = l
            print("Correct! The letter {} is indeed in the hidden word!".format(letter))
            if HIDDEN_LETTER not in wordfound:
                stillPlaying = False
                print("You win! The word was {}. You had {} lives left!".format(word, lives))
                break

        else :
            lives -= 1
            print("Sorry, the letter {} is not in the hidden word. You loose a life. Lives left : {}.".format(letter, lives))
            if lives == 0:
                stillPlaying = False
                print("You ran out of lives ! GAME OVER. The hidden word was {}".format(word))
                break


WORDS = load_words()
main(choice(WORDS))
