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

#Tkinter entry setup
D1Entry = Entry(root, width = 20)
DicEntry = Entry(root, width = 20)
ValEntry = Entry(root, width = 20)
VerifEntry1 = Entry(root, width = 10)
VerifEntry2 = Entry(root, width = 10)
VerifEntry3 = Entry(root, width = 10)
VerifEntry4 = Entry(root, width = 10)
VerifEntry5 = Entry(root, width = 10)

#Tkinter functions
def addDead():
    DEAD_LETTERS.append(str(D1Entry.get()))
def showDead():
    DeadLabel = Label(root, text = str(DEAD_LETTERS))
    DeadLabel.grid(row = 1)
def addDic():
    if str(DicEntry.get()) in CORRECT_LETTERS_WRONG_POSITIONS:
        CORRECT_LETTERS_WRONG_POSITIONS[str(DicEntry.get())].append(int(ValEntry.get()))
    else:
        CORRECT_LETTERS_WRONG_POSITIONS[str(DicEntry.get())] = [int(ValEntry.get())]
def showDic():
    DicLabel = Label(root, text = str(CORRECT_LETTERS_WRONG_POSITIONS))
    DicLabel.grid(row = 3)
def addVeri():
    VERIFIED_LETTERS[0] = str(VerifEntry1.get())
    VERIFIED_LETTERS[1] = str(VerifEntry2.get())
    VERIFIED_LETTERS[2] = str(VerifEntry3.get())
    VERIFIED_LETTERS[3] = str(VerifEntry4.get())
    VERIFIED_LETTERS[4] = str(VerifEntry5.get())
def showVeri():
    VeriLabel = Label(root, text = str(VERIFIED_LETTERS))
    VeriLabel.grid()

#Tkinter button setup
EntryAdd = Button(root, text = 'Add Dead Letters', command = addDead)
EntryShow = Button (root, text = 'Show Dead Letters', command = showDead)
DicAdd = Button(root, text = 'Add flawed Dictionary', command = addDic)
DicShow = Button(root, text = 'Show flawed Dictionary', command = showDic)
VeriAdd = Button(root, text = 'Add Verified Letters', command = addVeri)
VeriShow = Button(root, text = 'Show Verified Letters', command = showVeri)
# TODO: Add a result generator button at the end

#Layout of Buttons and Entrys
D1Entry.grid(row = 0, column = 0, columnspan = 5)
EntryAdd.grid(row = 0, column = 5, columnspan = 2)
EntryShow.grid(row = 0, column = 7, columnspan = 2)
DicEntry.grid(row = 2, column = 0, columnspan = 2)
ValEntry.grid(row = 2, column = 2, columnspan = 2)
DicAdd.grid(row = 2, column = 4, columnspan = 2)
DicShow.grid(row = 2, column = 6, columnspan = 2)
VerifEntry1.grid(row = 4, column = 0, columnspan = 2)
VerifEntry2.grid(row = 4, column = 2, columnspan = 2)
VerifEntry3.grid(row = 4, column = 4, columnspan = 2)
VerifEntry4.grid(row = 4, column = 6, columnspan = 2)
VerifEntry5.grid(row = 4, column = 8, columnspan = 2)
VeriAdd.grid(row = 5, column = 0, columnspan = 3)
VeriShow.grid(row = 5, column = 3, columnspan = 3)

#The answer button
AnswerShow = Button(root, text = "Show Answer")
AnswerShow.grid(row = 6, column = 2, ipadx = 100)
root.mainloop()