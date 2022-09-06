from tkinter import *
root = Tk()
root.title('Wordle Solver')

import json
import os
import string
from collections import Counter, defaultdict
from typing import Dict, List

DEAD_LETTERS = []

CORRECT_LETTERS_WRONG_POSITIONS: Dict[str, int] = {}

VERIFIED_LETTERS: List[str] = ['', '', '', '', '']

#Tkinter functions
def addDead():
    DEAD_LETTERS.append(str(D1Entry.get()))
    DeadLabel = Label(DeadFrame, text = str(DEAD_LETTERS))
    DeadLabel.grid(row = 1)

def addDic():
    if str(DicEntry.get()) in CORRECT_LETTERS_WRONG_POSITIONS:
        CORRECT_LETTERS_WRONG_POSITIONS[str(DicEntry.get())].append(int(ValEntry.get()))
    else:
        CORRECT_LETTERS_WRONG_POSITIONS[str(DicEntry.get())] = [int(ValEntry.get())]
    DicLabel = Label(DicFrame, text = str(CORRECT_LETTERS_WRONG_POSITIONS))
    DicLabel.grid(row = 1)

def addVeri():
    VERIFIED_LETTERS[0] = str(VerifEntry1.get())
    VERIFIED_LETTERS[1] = str(VerifEntry2.get())
    VERIFIED_LETTERS[2] = str(VerifEntry3.get())
    VERIFIED_LETTERS[3] = str(VerifEntry4.get())
    VERIFIED_LETTERS[4] = str(VerifEntry5.get())
    VeriLabel = Label(VeriFrame, text = str(VERIFIED_LETTERS))
    VeriLabel.grid(row = 2)

    
answerList = []




#DeadLetters Frame
DeadFrame = Frame(root, bg = 'red')
D1Entry = Entry(DeadFrame, width = 2)
D1Entry.grid(row = 0, column = 0)
EntryAdd = Button(DeadFrame, padx = 20, text = 'Add Dead Letters', command = addDead)
EntryAdd.grid(row = 0, column = 1)
DeadFrame.pack(fill = 'x')

#Dictionary Frame
DicFrame = Frame(root, bg = 'blue')
DicEntry = Entry(DicFrame, width = 2)
ValEntry = Entry(DicFrame, width = 2)
DicAdd = Button(DicFrame, padx = 5, text = 'Add Flawed Dictionary', command = addDic)
DicEntry.grid(row = 0, column = 0)
ValEntry.grid(row = 0, column = 1)
DicAdd.grid(row = 0, column = 2)
DicFrame.pack(fill = 'x')

#Verified Frame
VeriFrame = Frame(root, bg = 'green')
VerifEntry1 = Entry(VeriFrame, width = 2)
VerifEntry2 = Entry(VeriFrame, width = 2)
VerifEntry3 = Entry(VeriFrame, width = 2)
VerifEntry4 = Entry(VeriFrame, width = 2)
VerifEntry5 = Entry(VeriFrame, width = 2)
VeriAdd = Button(VeriFrame, text = 'Add Verified Letters', command = addVeri)
VerifEntry1.grid(row = 0, column = 0, padx = 1)
VerifEntry2.grid(row = 0, column = 1, padx = 1)
VerifEntry3.grid(row = 0, column = 2, padx = 1)
VerifEntry4.grid(row = 0, column = 3, padx = 1)
VerifEntry5.grid(row = 0, column = 4, padx = 1)
VeriAdd.grid(row = 1, columnspan = 5)
VeriFrame.pack(fill = 'x')







"""Do not edit code below this line!"""

def convertTuple(tup):
        # initialize an empty string
    w = ''
    for item in tup:
        w = w + str(item)
    return w

def main():
    """Wordle has two sets of lists (one is a short unordered list of the answers, one is a long
    ordered list of all possible words). All words in the lists are unique and are exactly 5
    letters long. Some words have repeating letters such as `knoll`
    """
    answerList.clear()

    global ALPHABET
    global NUM_BEST_GUESSES
    global DEAD_LETTERS_MINUS_VERIFIED

    ALPHABET = string.ascii_lowercase
    NUM_BEST_GUESSES = 5  # The number of best guesses to return to the user
# We do this in case the user forgot to remove the letter from the dead letters when if it
# becomes verified (such as double occurnaces).
    DEAD_LETTERS_MINUS_VERIFIED = set(DEAD_LETTERS) - set(VERIFIED_LETTERS)
    
    # TODO: Longterm we should grab the lists from the site in the chance they get updated overtime
    answer_list = _read_file('wordle_answers.json')
    non_answer_possible_words = _read_file('non_wordle_answers.json')
    combined_lists = answer_list + non_answer_possible_words  # noqa

    total_numbers = len(answer_list + non_answer_possible_words)
    print('Total number of Wordles:', total_numbers)

    possible_words = get_best_guess(
        answer_list
    )  # Replace the param with `combined_lists` if desired, but the answers come from `answer_list`
    most_common_start, most_common_letters, possible_words = get_most_common(possible_words)
    best_words = get_best_words(most_common_letters, possible_words)

    print(f'Top {NUM_BEST_GUESSES} Best Guesses:')
    # Sort the best guesses by best starting letter first, then highest weighted
    for word in sorted(best_words, key=lambda x: x[0].startswith(most_common_start[0][0]), reverse=True)[
        :NUM_BEST_GUESSES
    ]:
        answerList.append(convertTuple(word)) 
    AnsLabel.config(text = str(answerList))



def get_most_common(possible_words):
    """Gets the most common starting letters and letters overall."""
    letter_start_count = defaultdict(int)
    letter_counts = defaultdict(int)

    # TODO: There are better ways than a double (triple) nested for loop (could we use zip instead?)
    for word in possible_words:
        for letter in ALPHABET:
            if word.startswith(letter):
                letter_start_count[letter] += 1
            for letter in word:
                if letter in ALPHABET:
                    letter_counts[letter] += 1

    most_common_start = Counter(letter_start_count).most_common()
    most_common_letters = Counter(letter_counts).most_common()
    print('Most common starting letter:', most_common_start)
    print('Most common letters:', most_common_letters)

    return most_common_start, most_common_letters, possible_words


def get_best_words(most_common_letters, possible_words):
    """Gets the best possible words to guess based on their weighted probability."""
    letter_probabilities = sorted(
        list(set(most_common_letters) - set(DEAD_LETTERS_MINUS_VERIFIED)),
        key=lambda x: x[1],
        reverse=True,
    )

    letter_weights = {}
    for weight, letter in enumerate(letter_probabilities):
        letter_weights[letter[0]] = len(letter_probabilities) - weight

    highest_ranking_words = {}
    possible_words_count = 0
    for word in possible_words:
        word_failed = False
        letters_that_match_criteria = 0
        for letter in [possible_letter[0] for possible_letter in letter_probabilities]:
            # Toss out words that don't match verified letter positions
            for index, verified_letter in enumerate(VERIFIED_LETTERS):
                if verified_letter != word[index] and verified_letter != '':
                    word_failed = True
                    break
            for (
                correct_letter,
                bad_positions,
            ) in CORRECT_LETTERS_WRONG_POSITIONS.items():
                for bad_position in bad_positions:
                    if correct_letter == word[bad_position]:
                        word_failed = True
                        break
            if letter in word:
                letters_that_match_criteria += 1

        # TODO: this doesn't account well for repeated letters, simply making the match count `4` for now, fix later
        if letters_that_match_criteria >= 4 and not word_failed:
            word_weight = 0
            possible_words_count += 1
            for letter in word:
                word_weight += letter_weights[letter[0]]
                highest_ranking_words[word] = word_weight

    print('Possible words:', possible_words_count)

    best_words = []
    for word, weight in sorted(
        highest_ranking_words.items(),
        key=lambda x: x[1],
        reverse=True,
    ):
        best_words.append((word, weight))

    return best_words


def get_best_guess(answer_list):
    """Get the best guess based on probability from what's been eliminated,
    what was guess correctly, and what letters remain.
    """
    # TODO: Could we use zip here instead?
    possible_words = []
    for word in answer_list:
        word_failed = False
        for dead_letter in DEAD_LETTERS_MINUS_VERIFIED:
            if dead_letter in word:
                word_failed = True
                break
        for correct_letter in CORRECT_LETTERS_WRONG_POSITIONS:
            if correct_letter not in word:
                word_failed = True
                break

        if word_failed is True:
            # do nothing as the word is not valid
            pass
        else:
            possible_words.append(word)

    return possible_words


def _read_file(filename):
    with open(filename, 'r') as data:
        word_list = json.load(data)
    return word_list


def clearAnswer():
    answerList.clear()

#Answer Frame
AnswerFrame = Frame(root, bg = 'yellow')
AnsLabel = Label(AnswerFrame)
AnsLabel.grid(row = 1)
AnswerShow = Button(AnswerFrame, text = "Show Answer", command = main)
AnswerShow.grid(row = 0)
AnswerFrame.pack(fill = 'x')

root.mainloop()

#Key binding: https://www.plus2net.com/python/tkinter-events.php
