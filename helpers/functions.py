import main
import tkinter as tk
from enum import Enum


def goBackToMainWindow(window):
    window.destroy()
    main.mainWindow()


def insertInTextbox(textbox, text):
    textbox.insert(tk.END, text)


# a-z, &, |, ~, (, )
def validate(formula):
    for index, c in enumerate(formula):
        if not c.isalpha() and not (c in '&|~()'):
            return index, False
    return -1, True


def printIfValid(valid, invalidIndex, output, formula):
    if not valid:
        insertInTextbox(output,
                        f"Formula {formula} nu este validă, deoarece conține un caracter care nu "
                        f"face parte din alfabet pe poziția {invalidIndex}.")
        return
    insertInTextbox(output, f"Formula {formula} este validă.\n")


class Rule(Enum):
    baseRule, andRule, orRule, notRule, invalidRule = range(5)


def parse(formula):
    islp = [[False for _ in range(len(formula))] for _ in range(len(formula))]
    ruleType = [[Rule.invalidRule for _ in range(len(formula))] for _ in range(len(formula))]
    split = [[0 for _ in formula] for _ in formula]

    for index, c in enumerate(formula):
        if c.isalpha():
            islp[index][index] = True
            ruleType[index][index] = Rule.baseRule
    for length in range(2, len(formula) + 1):
        for index, c in enumerate(formula):
            end = index + length - 1
            if end >= len(formula):
                continue
            if c == '~' and islp[index + 1][end]:
                islp[index][end] = True
                ruleType[index][end] = Rule.notRule
            if c == '(' and formula[end] == ')':
                for k in range(index + 1, end):
                    if formula[k] == '&' or formula[k] == '|':
                        if islp[index + 1][k - 1] and islp[k + 1][end - 1]:
                            islp[index][end] = True
                            ruleType[index][end] = Rule.andRule if formula[k] == '&' else Rule.orRule
                            split[index][end] = k
                            break
    return islp, ruleType, split
