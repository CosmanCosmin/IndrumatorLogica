from algorithms import lpformula
from helpers import functions
import tkinter as tk


def buttonClickCompute(entry, outputText):
    outputText.delete('1.0', tk.END)
    lpformula.checkIfLP(entry.get(), outputText)


def buttonClickAddCharacter(entry, char):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, str(current) + str(char))


def showHelp(output):
    output.delete('1.0', tk.END)
    functions.insertInTextbox(output, "Introduceți o formulă pentru a verifica dacă face parte din "
                                      "Logica Propozițională.\n\n"
                                      "Mod de scriere:\n"
                                      "- orice literă de la a la z este considerată variabilă propozițională\n"
                                      "- folosiți ~ în loc de ¬\n"
                                      "- folosiți & în loc de ∧\n"
                                      "- folosiți | în loc ∨\n"
                                      "- orice formulă care nu este atomică sau de forma ~p trebuie"
                                      " scrisă între paranteze\n")


def formulaIsLp():
    window = tk.Tk()
    window.title("Logica Propozițională")
    windowWidth = 750
    windowHeight = 500
    centerX = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
    centerY = int(window.winfo_screenheight() / 2 - windowHeight / 2)
    window.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
    window.resizable(False, False)
    output = tk.Text(window, height=25, width=40, wrap=tk.WORD)
    buttonHeight, buttonWidth = 3, 12

    # create widgets
    entry = tk.Entry(window, font=('Arial', 12), width=32, borderwidth=4)
    notButton = tk.Button(window, text="~", height=buttonHeight, width=buttonWidth,
                          command=lambda: buttonClickAddCharacter(entry, "~"))
    andButton = tk.Button(window, text="&", height=buttonHeight, width=buttonWidth,
                          command=lambda: buttonClickAddCharacter(entry, "&"))
    orButton = tk.Button(window, text="|", height=buttonHeight, width=buttonWidth,
                         command=lambda: buttonClickAddCharacter(entry, "|"))
    leftBracketButton = tk.Button(window, text="(", height=buttonHeight, width=buttonWidth,
                                  command=lambda: buttonClickAddCharacter(entry, "("))
    rightBracketButton = tk.Button(window, text=")", height=buttonHeight, width=buttonWidth,
                                   command=lambda: buttonClickAddCharacter(entry, ")"))
    clearButton = tk.Button(window, text="Șterge", height=buttonHeight, width=buttonWidth,
                            command=lambda: entry.delete(0, tk.END))
    computeButton = tk.Button(window, text="Calculează", height=buttonHeight, width=buttonWidth,
                              command=lambda: buttonClickCompute(entry, output))
    backButton = tk.Button(window, text="Back", height=buttonHeight, width=10,
                           command=lambda: functions.goBackToMainWindow(window))
    helpButton = tk.Button(window, text="Indicații", height=buttonHeight, width=10, command=lambda: showHelp(output))
    showHelp(output)

    # display widgets
    entry.place(x=20, y=50)
    notButton.place(x=20, y=150)
    andButton.place(x=120, y=150)
    orButton.place(x=220, y=150)
    leftBracketButton.place(x=20, y=208)
    rightBracketButton.place(x=120, y=208)
    clearButton.place(x=220, y=208)
    computeButton.place(x=20, y=90)
    backButton.place(x=2, y=440)
    output.place(x=350, y=20)
    helpButton.place(x=475, y=440)

    entry.insert(tk.END, "(p&q)")
    window.mainloop()
