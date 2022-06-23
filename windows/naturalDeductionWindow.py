import json
import random
import tkinter as tk

from helpers import functions
from copy import deepcopy


def showHelp(output):
    output.delete('1.0', tk.END)
    functions.insertInTextbox(output, "Când apăsați pe butonul 'Începe' veți primi o secvență pe care trebuie să o"
                                      " demonstrați folosind regulile care fac parte din deducția naturală\n"
                                      " Mod de scriere:\n"
                                      "- orice literă de la a la z este considerată variabilă propozițională\n"
                                      "- folosiți ~ în loc de ¬\n"
                                      "- folosiți & în loc de ∧\n"
                                      "- folosiți | în loc ∨\n"
                                      "- folosiți -> în loc →\n"
                                      "- orice formulă care nu este atomică sau de forma ~p trebuie"
                                      " scrisă între paranteze\n")


def composeFormula(output, entry, var, text):
    if entry.get() == "":
        return
    functions.insertInTextbox(output, f"{entry.get()}")
    text.append(entry.get())
    var.set(1)


def getEntries(values, window, output):
    text = []
    for c in values:
        functions.insertInTextbox(output, f"\n{c}=")
        entry = tk.Entry(window, font=('Arial', 12), width=30, borderwidth=4)
        entry.place(x=20, y=30)
        var = tk.IntVar()
        insertButton = tk.Button(window, text="Inserează", height=1, width=8,
                                 command=lambda: composeFormula(output, entry, var, text))
        insertButton.place(x=310, y=30)
        insertButton.wait_variable(var)
        insertButton.destroy()
        entry.destroy()
    return text


def checkInDomain(val, formulaSet, output):
    if val not in formulaSet:
        functions.insertInTextbox(output, f"\nFormula {val} nu se află în domeniu")
        return False
    return True


def checkDemonstrated(values, formulaSet, solvedQueue, output):
    for val in values:
        if getFormulaString(formulaSet, val) not in solvedQueue.values():
            functions.insertInTextbox(output, f"\nFormula {getFormulaString(formulaSet, val)}"
                                              f" nu este demonstrată anterior")
            return False
    return True


def getIndexes(values, solvedQueue, formulaSet):
    indexes = []
    for val in values:
        indexes.append(str(list(solvedQueue.keys())[list(solvedQueue.values())
                           .index(getFormulaString(formulaSet, val))]))
    return indexes


def getFormulaString(formulaSet, val):
    return f"{'{' + ','.join(formulaSet) + '}'}⊢{val}"


def resolveButtonClick(val, defName, output, index, formulaSet, solvedQueue, ending, endingVar):
    functions.insertInTextbox(output, f"\n{index[0]}. {getFormulaString(formulaSet, val)}   {defName}")
    solvedQueue[index[0]] = getFormulaString(formulaSet, val)
    index[0] += 1
    if ending == getFormulaString(formulaSet, val):
        endingVar.set(1)


def introduceAnd(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p, q = getEntries('pq', window, output)
    if not checkDemonstrated([p, q], formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(&i, {", ".join(getIndexes([p, q], solvedQueue, formulaSet))})'
    resolveButtonClick(f'({p}&{q})', definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def eliminateAnd1(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p, q = getEntries('pq', window, output)
    values = [f'({p}&{q})']
    if not checkDemonstrated(values, formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(&e1, {", ".join(getIndexes(values, solvedQueue, formulaSet))})'
    resolveButtonClick(f'{p}', definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def eliminateAnd2(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p, q = getEntries('pq', window, output)
    values = [f'({p}&{q})']
    if not checkDemonstrated(values, formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(&e2, {", ".join(getIndexes(values, solvedQueue, formulaSet))})'
    resolveButtonClick(f'{q}', definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def eliminateImplication(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p, q = getEntries('pq', window, output)
    values = [f'({p}->{q})', p]
    if not checkDemonstrated(values, formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(->e, {", ".join(getIndexes(values, solvedQueue, formulaSet))})'
    resolveButtonClick(f'{q}', definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def introduceImplication(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p, q = getEntries('pq', window, output)
    values = [q]
    if not checkInDomain(p, formulaSet, output) or not checkDemonstrated(values, formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(->i, {", ".join(getIndexes(values, solvedQueue, formulaSet))})'
    formulaSet.remove(p)
    resolveButtonClick(f'({p}->{q})', definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def introduceOr1(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p, q = getEntries('pq', window, output)
    values = [p]
    if not checkDemonstrated(values, formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(|i1, {", ".join(getIndexes(values, solvedQueue, formulaSet))})'
    resolveButtonClick(f'({p}|{q})', definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def introduceOr2(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p, q = getEntries('pq', window, output)
    values = [q]
    if not checkDemonstrated(values, formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(|i2, {", ".join(getIndexes(values, solvedQueue, formulaSet))})'
    resolveButtonClick(f'({p}|{q})', definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def eliminateOr(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p, q, r = getEntries('pqr', window, output)
    values = [f'({p}|{q})']
    if not checkDemonstrated(values, formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    values1 = [r]
    formulaSet1 = deepcopy(formulaSet)
    formulaSet1.append(p)
    if not checkDemonstrated(values1, formulaSet1, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    formulaSet2 = deepcopy(formulaSet)
    formulaSet2.append(q)
    if not checkDemonstrated(values1, formulaSet2, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    index1 = getIndexes(values, solvedQueue, formulaSet)
    index2 = getIndexes(values1, solvedQueue, formulaSet1)
    index3 = getIndexes(values1, solvedQueue, formulaSet2)
    definitionName = f'(|e, {", ".join([index1[0], index2[0], index3[0]])})'
    resolveButtonClick(f'{r}', definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def eliminateNegation(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p = getEntries('p', window, output)[0]
    values = [p, f'~{p}']
    if not checkDemonstrated(values, formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(~e, {", ".join(getIndexes(values, solvedQueue, formulaSet))})'
    resolveButtonClick(f'⊥', definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def introduceNegation(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p = getEntries('p', window, output)[0]
    values = ['⊥']
    if not checkInDomain(p, formulaSet, output) or not checkDemonstrated(values, formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(~i, {", ".join(getIndexes(values, solvedQueue, formulaSet))})'
    formulaSet.remove(p)
    resolveButtonClick(f'~{p}', definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def eliminateContradiction(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p = getEntries('p', window, output)[0]
    values = ['⊥']
    if not checkDemonstrated(values, formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(⊥e, {", ".join(getIndexes(values, solvedQueue, formulaSet))})'
    resolveButtonClick(p, definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def premiss(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p = getEntries('p', window, output)[0]
    if not checkInDomain(p, formulaSet, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(ipoteză)'
    resolveButtonClick(p, definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def extend(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p, q = getEntries('pq', window, output)
    values = [p]
    if not checkDemonstrated(values, formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(extindere, {", ".join(getIndexes(values, solvedQueue, formulaSet))})'
    formulaSet.append(q)
    resolveButtonClick(p, definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def eliminateDoubleNegation(formulaSet, window, output, index, solvedQueue, ending, endingVar):
    p = getEntries('p', window, output)[0]
    values = [f'~~{p}']
    if not checkDemonstrated(values, formulaSet, solvedQueue, output):
        functions.insertInTextbox(output, f"\nSelectați altă formulă.")
        return
    definitionName = f'(~~e, {", ".join(getIndexes(values, solvedQueue, formulaSet))})'
    resolveButtonClick(p, definitionName, output, index, formulaSet, solvedQueue, ending, endingVar)


def start(window, output, startButton, formula):
    output.delete('1.0', tk.END)
    functions.insertInTextbox(output, f"Arătați că următoarea secvență este validă:\n{formula['ending']}\n")
    functions.insertInTextbox(output, f"Având ca domeniu Γ = {'{' + ','.join(formula['formulaSet']) + '}'}")

    index = [1]
    solvedQueue = {}
    endingVar = tk.IntVar()
    formulaSet = formula["formulaSet"]
    buttonWidth = 16
    button1 = tk.Button(window, text="p   q \n (p&q)", height=3, width=buttonWidth,
                        command=lambda: introduceAnd(formulaSet, window, output,
                                                     index, solvedQueue, formula['ending'], endingVar))
    button2 = tk.Button(window, text="(p&q)\n p", height=3, width=buttonWidth,
                        command=lambda: eliminateAnd1(formulaSet, window, output,
                                                      index, solvedQueue, formula['ending'], endingVar))
    button3 = tk.Button(window, text="(p&q)\n q", height=3, width=buttonWidth,
                        command=lambda: eliminateAnd2(formulaSet, window, output,
                                                      index, solvedQueue, formula['ending'], endingVar))
    button4 = tk.Button(window, text="(p->q)   p\n q", height=3, width=buttonWidth,
                        command=lambda: eliminateImplication(formulaSet, window, output,
                                                             index, solvedQueue, formula['ending'], endingVar))
    button5 = tk.Button(window, text="p ⊢ q \n (p->q)", height=3, width=buttonWidth,
                        command=lambda: introduceImplication(formulaSet, window, output,
                                                             index, solvedQueue, formula['ending'], endingVar))
    button6 = tk.Button(window, text="p \n (p|q)", height=3, width=buttonWidth,
                        command=lambda: introduceOr1(formulaSet, window, output,
                                                     index, solvedQueue, formula['ending'], endingVar))
    button7 = tk.Button(window, text="q \n (p|q)", height=3, width=buttonWidth,
                        command=lambda: introduceOr2(formulaSet, window, output,
                                                     index, solvedQueue, formula['ending'], endingVar))
    button8 = tk.Button(window, text="(p|q)   p ⊢ r    q ⊢ r \n r", height=3, width=2 * buttonWidth + 2,
                        command=lambda: eliminateOr(formulaSet, window, output,
                                                    index, solvedQueue, formula['ending'], endingVar))
    button9 = tk.Button(window, text="p   ~p\n ⊥", height=3, width=buttonWidth,
                        command=lambda: eliminateNegation(formulaSet, window, output,
                                                          index, solvedQueue, formula['ending'], endingVar))
    button10 = tk.Button(window, text="p ⊢ ⊥\n ~p", height=3, width=buttonWidth,
                         command=lambda: introduceNegation(formulaSet, window, output,
                                                           index, solvedQueue, formula['ending'], endingVar))

    button11 = tk.Button(window, text="⊥ \n p", height=3, width=buttonWidth,
                         command=lambda: eliminateContradiction(formulaSet, window, output,
                                                                index, solvedQueue, formula['ending'], endingVar))
    button12 = tk.Button(window, text="ipoteză p∈Γ\n p", height=3, width=buttonWidth,
                         command=lambda: premiss(formulaSet, window, output,
                                                 index, solvedQueue, formula['ending'], endingVar))
    button13 = tk.Button(window, text="p \n q ⊢ p", height=3, width=buttonWidth,
                         command=lambda: extend(formulaSet, window, output,
                                                index, solvedQueue, formula['ending'], endingVar))
    button14 = tk.Button(window, text="~~p \n p", height=3, width=buttonWidth,
                         command=lambda: eliminateDoubleNegation(formulaSet, window, output,
                                                                 index, solvedQueue, formula['ending'], endingVar))

    button1.place(x=20, y=100)
    button2.place(x=145, y=100)
    button3.place(x=270, y=100)
    button4.place(x=20, y=160)
    button5.place(x=145, y=160)
    button6.place(x=270, y=160)
    button7.place(x=20, y=220)
    button8.place(x=145, y=220)
    button9.place(x=20, y=280)
    button10.place(x=145, y=280)
    button11.place(x=270, y=280)
    button12.place(x=20, y=340)
    button13.place(x=145, y=340)
    button14.place(x=270, y=340)

    startButton.wait_variable(endingVar)
    functions.insertInTextbox(output, f"\nAstfel, secvența este validă.")


def readFromJson():
    with open('info/sequences.json') as file:
        data = json.load(file)
        return random.choice(data["sequences"])


def naturalDeduction():
    window = tk.Tk()
    window.title("Deducția naturală")
    windowWidth = 750
    windowHeight = 500
    centerX = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
    centerY = int(window.winfo_screenheight() / 2 - windowHeight / 2)
    window.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
    window.resizable(False, False)

    output = tk.Text(window, height=25, width=40, wrap=tk.WORD)
    buttonWidth = 16
    backButton = tk.Button(window, text="Back", height=3, width=buttonWidth,
                           command=lambda: functions.goBackToMainWindow(window))
    startButton = tk.Button(window, text="Începe", height=3, width=10,
                            command=lambda: start(window, output, startButton, readFromJson()))
    helpButton = tk.Button(window, text="Indicații", height=3, width=10, command=lambda: showHelp(output))
    showHelp(output)

    output.place(x=400, y=30)
    backButton.place(x=2, y=440)
    helpButton.place(x=525, y=440)
    startButton.place(x=400, y=440)

    window.mainloop()
