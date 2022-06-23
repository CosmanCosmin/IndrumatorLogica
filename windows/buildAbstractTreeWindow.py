from helpers import functions
from algorithms import abstractTree
import tkinter as tk
from PIL import ImageTk, Image


def buttonClickCompute(window, entry, outputText):
    outputText.delete('1.0', tk.END)
    valid, height, nodes, varPropSet = abstractTree.createTree(entry.get(), outputText)
    if valid:
        canvas = tk.Canvas(window, width=275, height=300)
        image = Image.open("graphs/graph.png")
        img = ImageTk.PhotoImage(image.resize((275, 300), Image.Resampling.LANCZOS))
        canvas.imgref = img
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.place(x=100, y=100)
        buttonShowOriginal = tk.Button(window, text="Afișează", height=3, width=10,
                                       command=lambda: image.show())
        buttonShowOriginal.place(x=200, y=440)
        functions.insertInTextbox(outputText, f"Arborele are înălțimea {height}"
                                              f" și dimensiunea (numărul de noduri) {nodes}.\n"
                                              f"Mulțimea variabilelor propoziționale este "
                                              f"{'{' + ','.join(sorted(list(varPropSet))) + '}'}")


def showHelp(output):
    output.delete('1.0', tk.END)
    functions.insertInTextbox(output, "Introduceți formula pentru a crea arborele abstract corespunzător.\n"
                                      "După ce este creat puteți apăsa butonul 'Afișează' pentru a deschide imaginea "
                                      "extern. \n\n "
                                      " Mod de scriere:\n"
                                      "- orice literă de la a la z este considerată variabilă propozițională\n"
                                      "- folosiți ~ în loc de ¬\n"
                                      "- folosiți & în loc de ∧\n"
                                      "- folosiți | în loc ∨\n"
                                      "- orice formulă care nu este atomică sau de forma ~p trebuie"
                                      " scrisă între paranteze\n")


def buildAbstractTree():
    window = tk.Tk()
    window.title("Arbori abstracți")
    windowWidth, windowHeight = 750, 500
    buttonHeight, buttonWidth = 3, 30
    centerX = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
    centerY = int(window.winfo_screenheight() / 2 - windowHeight / 2)
    window.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
    window.resizable(False, False)

    entry = tk.Entry(window, font=('Arial', 12), width=30, borderwidth=4)
    output = tk.Text(window, height=25, width=40, wrap=tk.WORD)
    buttonCompute = tk.Button(window, text="Calculează", height=1, width=10,
                              command=lambda: buttonClickCompute(window, entry, output))
    backButton = tk.Button(window, text="Back", height=buttonHeight, width=10,
                           command=lambda: functions.goBackToMainWindow(window))
    helpButton = tk.Button(window, text="Indicații", height=buttonHeight, width=10, command=lambda: showHelp(output))
    showHelp(output)

    entry.place(x=100, y=30)
    output.place(x=400, y=30)
    buttonCompute.place(x=200, y=60)
    backButton.place(x=2, y=440)
    helpButton.place(x=525, y=440)

    window.mainloop()
