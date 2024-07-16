import os
import webbrowser
import sys
import re
import pygtkcompat


def test_your_skill(passage: str = None):
    if passage == None:
        passage = input("What is the passage\n").strip()
        sys.stdout.write("\n\n\n\n\n\n\n\n\n=======\n\n\n\n")
        re.sub("\\\\u.*\s", "", passage)
    passaget = passage
    score = 0
    for i in range(0, 9):
        guess = input("What can you remember?\n")
        if guess in passage:
            print("Yay!:)")
            passage.replace(guess, "")
            passage.strip()
            score += 1
        else:
            print("wrong!:(")
    print(passage+"\n")
    print(passaget)
    print(len(passage)/len(passaget))


test_your_skill()
guiopen = webbrowser.Mozilla("firefox")
