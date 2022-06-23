import tkinter as tk
from helpers import functions
import re

exitFlag = False


def addToDict(valDict, key, entry, var, output):
    if entry.get() in ['0', '1']:
        valDict[key] = entry.get()
        functions.insertInTextbox(output, f'{entry.get()}\n')
        var.set(1)


def calculate(window, entry, output):
    if entry.get() == 'Formula...' or not entry.get():
        return
    output.delete('1.0', tk.END)
    formula = entry.get()
    invalidIndex, valid = functions.validate(formula)
    if not valid:
        return
    functions.printIfValid(valid, invalidIndex, output, formula)

    islp, ruleType, split = functions.parse(formula)
    if not islp[0][len(formula) - 1]:
        functions.insertInTextbox(output, f"Formula {formula} nu face parte din LP.")
        return

    varProps = dict.fromkeys(set(re.split("[^a-zA-Z]*", formula)), 0)
    varProps.pop('')

    functions.insertInTextbox(output, f'Introduceți valorile din atribuire (0 sau 1):\n')
    for index, key in enumerate(sorted(varProps.keys())):
        entry.delete('0', 'end')
        var = tk.IntVar()
        functions.insertInTextbox(output, f'τ({key})=')
        backButton = tk.Button(window, text="Back", height=3, width=10,
                               command=lambda: back(window, var))
        buttonAdd = tk.Button(window, text="Adaugă", height=1, width=8,
                              command=lambda: addToDict(varProps, key, entry, var, output))
        buttonAdd.place(x=325, y=50)
        backButton.place(x=2, y=440)
        window.protocol("WM_DELETE_WINDOW", lambda: closeWindow(window, var))
        buttonAdd.wait_variable(var)

    global exitFlag
    if exitFlag:
        return
    mainButtons(window, entry, output)
    entry.delete('0', 'end')
    functions.insertInTextbox(output, f'Se calculează...\n')
    functions.insertInTextbox(output, f'{formula}=τ({formula})=')
    initialFormula = formula
    for key in varProps.keys():
        formula = formula.replace(key, varProps[key])
    formula = formula.replace('&', '*')
    formula = formula.replace('|', '+')

    functions.insertInTextbox(output, f'{formula}=')
    while formula not in ['0', '1']:
        changed = False
        for i in ['0', '1']:
            for j in ['0', '1']:
                for conn in ['*', '+']:
                    if not changed:
                        newFormula = formula.replace(f'({i}{conn}{j})', compute(i, j, conn))
                        if newFormula != formula:
                            formula = newFormula
                            changed = True
        newFormula = ''
        index = 0
        while index < len(formula):
            if formula[index] == '~' and (index != len(formula) - 1) and formula[index + 1] in ['0', '1']:
                newFormula += str((int(formula[index + 1]) + 1) % 2)
                index += 1
            else:
                newFormula += formula[index]
            index += 1
        formula = newFormula
        functions.insertInTextbox(output, f'{formula}')
        if formula not in ['0', '1']:
            functions.insertInTextbox(output, f'=')
    if formula == '1':
        functions.insertInTextbox(output, f'\n\nAtribuirea dată este model al formulei {initialFormula}.\n'
                                          f'Astfel, formula este satisfiabilă.')
    else:
        functions.insertInTextbox(output, f'\n\nAtribuirea dată nu este model al formulei {initialFormula}.')


def compute(i, j, conn):
    if conn == '*':
        return str(int(i) * int(j))
    if conn == '+':
        return str(min(1, int(i) + int(j)))


def showHelp(output):
    output.delete('1.0', tk.END)
    functions.insertInTextbox(output, "Introduceți o formulă și apoi o atribuire pentru a calcula valoarea de adevăr a"
                                      " formulei în acea atribuire.\n\n"
                                      "Mod de scriere:\n"
                                      "- orice literă de la a la z este considerată variabilă propozițională\n"
                                      "- folosiți ~ în loc de ¬\n"
                                      "- folosiți & în loc de ∧\n"
                                      "- folosiți | în loc ∨\n"
                                      "- orice formulă care nu este atomică sau de forma ~p trebuie"
                                      " scrisă între paranteze\n")


def closeWindow(window, var):
    global exitFlag
    exitFlag = True
    var.set(1)
    window.destroy()


def back(window, var):
    global exitFlag
    exitFlag = True
    var.set(1)
    functions.goBackToMainWindow(window)


def mainButtons(window, entry, output):
    backButton = tk.Button(window, text="Back", height=3, width=10,
                           command=lambda: functions.goBackToMainWindow(window))
    buttonCompute = tk.Button(window, text="Calculează", height=1, width=8,
                              command=lambda: calculate(window, entry, output))
    backButton.place(x=2, y=440)
    buttonCompute.place(x=325, y=50)
    entry.insert(0, 'Formula...')


def getAssignmentValue():
    window = tk.Tk()
    window.title("Valoarea de adevăr")
    windowWidth, windowHeight = 750, 500
    buttonHeight, buttonWidth = 3, 30
    centerX = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
    centerY = int(window.winfo_screenheight() / 2 - windowHeight / 2)
    window.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
    window.resizable(False, False)
    output = tk.Text(window, height=25, width=40, wrap=tk.WORD)

    entry = tk.Entry(window, font=('Arial', 12), width=32, borderwidth=4)
    helpButton = tk.Button(window, text="Indicații", height=buttonHeight, width=10, command=lambda: showHelp(output))
    showHelp(output)

    entry.place(x=20, y=50)
    output.place(x=400, y=30)
    helpButton.place(x=525, y=440)

    mainButtons(window, entry, output)
    entry.bind("<FocusIn>", lambda args: entry.delete('0', 'end'))

    window.mainloop()
