from algorithms import normalforms as nf
import tkinter as tk
from helpers import functions
from algorithms import abstractTree

current = ''
start = False
inFormula = False


def startAlgorithm(window, output, entry, startButton):
    if entry.get() == "":
        return
    global current
    global start
    var = tk.IntVar()
    start = True
    current = entry.get()
    output.delete('1.0', tk.END)
    functions.insertInTextbox(output, entry.get())
    entry.delete(0, tk.END)
    buttonHeight, buttonWidth = 3, 17
    button_1 = tk.Button(window, height=buttonHeight, width=buttonWidth, wraplength=120,
                         text="1. (p <-> q) ≡ ((p->q) & (q->p))",
                         command=lambda: firstButton(window, output, entry, var))
    button_2 = tk.Button(window, height=buttonHeight, width=buttonWidth, wraplength=120, text="2. (p -> q) ≡ (~p | q)",
                         command=lambda: secondButton(window, output, entry, var))
    button_3 = tk.Button(window, height=buttonHeight, width=buttonWidth, wraplength=120,
                         text="3. (p | (q & r)) ≡ ((p | q) & (p | r))",
                         command=lambda: thirdButton(window, output, entry, var))
    button_4 = tk.Button(window, height=buttonHeight, width=buttonWidth, wraplength=120,
                         text="4. ((p & q) | r) ≡ ((q | p) & (r | p))",
                         command=lambda: fourthButton(window, output, entry, var))
    button_5 = tk.Button(window, height=buttonHeight, width=buttonWidth, wraplength=120,
                         text="5. (p | (q | r)) ≡ ((p | q) | r);",
                         command=lambda: fifthButton(window, output, entry, var))
    button_6 = tk.Button(window, height=buttonHeight, width=buttonWidth, wraplength=120,
                         text="6. (p & (q & r)) ≡ ((p & q) & r);",
                         command=lambda: sixthButton(window, output, entry, var))
    button_7 = tk.Button(window, height=buttonHeight, width=buttonWidth, wraplength=120,
                         text="7. ~(p | q) ≡ (~p & ~q);",
                         command=lambda: seventhButton(window, output, entry, var))
    button_8 = tk.Button(window, height=buttonHeight, width=buttonWidth, wraplength=120,
                         text="8. ~(p & q) ≡ (~p | ~q);", command=lambda: eighthButton(window, output, entry, var))
    button_9 = tk.Button(window, height=buttonHeight, width=buttonWidth, wraplength=120, text="9. ¬¬p ≡ p",
                         command=lambda: ninthButton(window, output, entry, var))
    button_1.place(x=20, y=150)
    button_2.place(x=150, y=150)
    button_3.place(x=280, y=150)
    button_4.place(x=20, y=210)
    button_5.place(x=150, y=210)
    button_6.place(x=280, y=210)
    button_7.place(x=20, y=270)
    button_8.place(x=150, y=270)
    button_9.place(x=280, y=270)
    startButton.wait_variable(var)
    functions.insertInTextbox(output, "\nFormula este în FNC")


def formEntryText(text, entries, output, var):
    for entry in entries:
        if entry.get() == "":
            functions.insertInTextbox(output, f"Unul din câmpuri este gol...")
            return
    for entry in entries:
        text.append(entry.get())
        var.set(1)


def getEntries(values, window, output):
    text = []
    ypos = 70
    entries = []
    for index, c in enumerate(values):
        entries.append(tk.Entry(window, font=('Arial', 9), width=25, borderwidth=4))
        entries[index].place(x=20, y=ypos)
        entries[index].insert(0, f'Valoarea pentru {c}...')
        ypos += 25

    if len(entries) == 3:
        entries[2].bind("<FocusIn>", lambda args: entries[2].delete('0', 'end'))
    if len(entries) >= 2:
        entries[1].bind("<FocusIn>", lambda args: entries[1].delete('0', 'end'))
    entries[0].bind("<FocusIn>", lambda args: entries[0].delete('0', 'end'))

    var = tk.IntVar()
    continueButton = tk.Button(window, text="Adăugați", height=1, width=10,
                               command=lambda: formEntryText(text, entries, output, var))
    continueButton.place(x=220, y=70)

    continueButton.wait_variable(var)

    for entry in entries:
        entry.destroy()
    continueButton.destroy()

    return text


def firstButton(window, output, entry, var):
    global start, inFormula
    if not start or inFormula:
        return
    inFormula = True
    p, q = getEntries('pq', window, output)

    global current
    entry.delete(0, tk.END)
    if current.find(f'({p}<->{q})') == -1:
        functions.insertInTextbox(output, f"Formula selectată nu poate fi aplicată.")
        inFormula = False
        return
    current = current.replace(f'({p}<->{q})', nf.eliminateDoubleImplication(p, q))
    functions.insertInTextbox(output, f"\n=1={current}")

    if checkFormulaFNC():
        var.set(1)
    inFormula = False


def secondButton(window, output, entry, var):
    global start, inFormula
    if not start or inFormula:
        return
    inFormula = True
    p, q = getEntries('pq', window, output)
    global current
    entry.delete(0, tk.END)
    if current.find(f'({p}->{q})') == -1:
        functions.insertInTextbox(output, f"Formula selectată nu poate fi aplicată.")
        inFormula = False
        return
    current = current.replace(f'({p}->{q})', nf.eliminateImplication(p, q))
    functions.insertInTextbox(output, f"\n=2={current}")

    if checkFormulaFNC():
        var.set(1)
    inFormula = False


def thirdButton(window, output, entry, var):
    global start, inFormula
    if not start or inFormula:
        return
    inFormula = True
    p, q, r = getEntries('pqr', window, output)
    global current
    entry.delete(0, tk.END)
    if current.find(f'({p}|({q}&{r}))') == -1:
        functions.insertInTextbox(output, f"Formula selectată nu poate fi aplicată.")
        inFormula = False
        return
    current = current.replace(f'({p}|({q}&{r}))', nf.distributeOr1(p, q, r))
    functions.insertInTextbox(output, f"\n=3={current}")

    if checkFormulaFNC():
        var.set(1)
    inFormula = False


def fourthButton(window, output, entry, var):
    global start, inFormula
    if not start or inFormula:
        return
    inFormula = True
    p, q, r = getEntries('pqr', window, output)
    global current
    entry.delete(0, tk.END)
    if current.find(f'(({p}&{q})|{r})') == -1:
        functions.insertInTextbox(output, f"Formula selectată nu poate fi aplicată.")
        inFormula = False
        return
    current = current.replace(f'(({p}&{q})|{r})', nf.distributeOr2(p, q, r))
    functions.insertInTextbox(output, f"\n=4={current}")
    if checkFormulaFNC():
        var.set(1)
    inFormula = False


def fifthButton(window, output, entry, var):
    global start, inFormula
    if not start or inFormula:
        return
    inFormula = True

    p, q, r = getEntries('pqr', window, output)
    global current
    entry.delete(0, tk.END)
    if current.find(f'({p}|({q}|{r}))') == -1:
        functions.insertInTextbox(output, f"Formula selectată nu poate fi aplicată.")
        inFormula = False
        return
    current = current.replace(f'({p}|({q}|{r}))', nf.swapBracketOr(p, q, r))
    functions.insertInTextbox(output, f"\n=5={current}")

    if checkFormulaFNC():
        var.set(1)
    inFormula = False


def sixthButton(window, output, entry, var):
    global start, inFormula
    if not start or inFormula:
        return
    inFormula = True
    p, q, r = getEntries('pqr', window, output)
    global current
    entry.delete(0, tk.END)
    if current.find(f'({p}&({q}&{r}))') == -1:
        functions.insertInTextbox(output, f"Formula selectată nu poate fi aplicată.")
        inFormula = False
        return
    current = current.replace(f'({p}&({q}&{r}))', nf.swapBracketAnd(p, q, r))
    functions.insertInTextbox(output, f"\n=6={current}")

    if checkFormulaFNC():
        var.set(1)
    inFormula = False


def seventhButton(window, output, entry, var):
    global start, inFormula
    if not start or inFormula:
        return
    inFormula = True
    p, q = getEntries('pq', window, output)
    global current
    entry.delete(0, tk.END)
    if current.find(f'~({p}|{q})') == -1:
        functions.insertInTextbox(output, f"Formula selectată nu poate fi aplicată.")
        inFormula = False
        return
    current = current.replace(f'~({p}|{q})', nf.insertNegationOr(p, q))
    functions.insertInTextbox(output, f"\n=7={current}")

    if checkFormulaFNC():
        var.set(1)
    inFormula = False


def eighthButton(window, output, entry, var):
    global start, inFormula
    if not start or inFormula:
        return
    inFormula = True
    p, q = getEntries('pq', window, output)
    global current
    entry.delete(0, tk.END)
    if current.find(f'~({p}&{q})') == -1:
        functions.insertInTextbox(output, f"Formula selectată nu poate fi aplicată.")
        inFormula = False
        return
    current = current.replace(f'~({p}&{q})', nf.insertNegationAnd(p, q))
    functions.insertInTextbox(output, f"\n=8={current}")

    if checkFormulaFNC():
        var.set(1)
    inFormula = False


def ninthButton(window, output, entry, var):
    global start, inFormula
    if not start or inFormula:
        return
    inFormula = True
    p = getEntries('p', window, output)[0]
    global current
    entry.delete(0, tk.END)
    if current.find(f'~~{p}') == -1:
        functions.insertInTextbox(output, f"\nFormula selectată nu poate fi aplicată.")
        inFormula = False
        return
    current = current.replace(f'~~{p}', nf.eliminateDoubleNegation(p))
    functions.insertInTextbox(output, f"\n=9={current}")

    if checkFormulaFNC():
        var.set(1)
    inFormula = False


def checkSyntaxTree(root, found, fncFlag):
    if not root:
        return
    if root.value == '~':
        if root.left and not ('a' <= root.left.value <= 'z'):
            fncFlag[0] = False
        if root.right and not ('a' <= root.right.value <= 'z'):
            fncFlag[0] = False
    if root.value == '|':
        found = True
    if found and root.value == '&':
        fncFlag[0] = False
    if not fncFlag[0]:
        return
    checkSyntaxTree(root.left, found, fncFlag)
    checkSyntaxTree(root.right, found, fncFlag)


def checkFormulaFNC():
    global current
    fncFlag = [True]
    if '-' in current:
        return False
    islp, ruleType, split = functions.parse(current)
    binaryTree, _ = abstractTree.tree(0, len(current) - 1, current, islp, ruleType, split, 0)
    checkSyntaxTree(binaryTree, False, fncFlag)
    return fncFlag[0]


def showHelp(output):
    global start, inFormula
    start, inFormula = False, False
    functions.insertInTextbox(output, "Introduceți o formulă pentru a o aduce în forma normală conjunctivă.\n"
                                      " Mod de scriere:\n"
                                      "- orice literă de la a la z este considerată variabilă propozițională\n"
                                      "- folosiți ~ în loc de ¬\n"
                                      "- folosiți & în loc de ∧\n"
                                      "- folosiți | în loc ∨\n"
                                      "- folosiți -> în loc →\n"
                                      "- folosiți <-> în loc ↔\n"
                                      "- orice formulă care nu este atomică sau de forma ~p trebuie"
                                      " scrisă între paranteze\n")


def bringFormulaToNormalForm():
    window = tk.Tk()
    window.title(f"Forme normale")
    windowWidth = 750
    windowHeight = 500
    centerX = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
    centerY = int(window.winfo_screenheight() / 2 - windowHeight / 2)
    window.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
    window.resizable(False, False)

    buttonHeight, buttonWidth = 3, 17
    entry = tk.Entry(window, font=('Arial', 12), width=30, borderwidth=4)
    backButton = tk.Button(window, text="Back", height=buttonHeight, width=10,
                           command=lambda: functions.goBackToMainWindow(window))
    startButton = tk.Button(window, text="Start", height=1, width=10,
                            command=lambda: startAlgorithm(window, output, entry, startButton))
    output = tk.Text(window, height=25, width=40, wrap=tk.WORD)
    showHelp(output)

    entry.place(x=20, y=30)
    output.place(x=420, y=30)
    backButton.place(x=2, y=440)
    startButton.place(x=310, y=30)
