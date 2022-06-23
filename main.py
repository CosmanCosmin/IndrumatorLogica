from windows import lpformulawindow, normalformwindow, quizzWindow, buildAbstractTreeWindow, assignmentValueWindow,\
    naturalDeductionWindow
import tkinter as tk
from PIL import ImageTk, Image


def mainWindow():
    window = tk.Tk()
    window.title("Îndrumător Logică")
    windowWidth, windowHeight = 750, 500
    centerX = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
    centerY = int(window.winfo_screenheight() / 2 - windowHeight / 2)
    window.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
    window.resizable(False, False)
    buttonHeight, buttonWidth = 3, 30

    title = tk.Label(window, text="Îndrumător Logică", borderwidth=0)
    quizzButton = tk.Button(window, text="Chestionar", height=buttonHeight, width=buttonWidth,
                            command=lambda: changeWindow(quizzWindow.quizz, window))
    lpButton = tk.Button(window, text="Verifică dacă o formulă face parte din logica propozițională",
                         height=buttonHeight, width=buttonWidth, wraplength=130,
                         command=lambda: changeWindow(lpformulawindow.formulaIsLp, window))
    fnButton = tk.Button(window, text="Aducerea unei formule în formă normală conjunctivă",
                         height=buttonHeight, width=buttonWidth, wraplength=130,
                         command=lambda: changeWindow(normalformwindow.bringFormulaToNormalForm, window))
    treeButton = tk.Button(window, text="Arborele abstract al unei formule",
                           height=buttonHeight, width=buttonWidth, wraplength=130,
                           command=lambda: changeWindow(buildAbstractTreeWindow.buildAbstractTree, window))
    assignButton = tk.Button(window, text="Valoarea de adevăr a unei formule într-o atribuire",
                             height=buttonHeight, width=buttonWidth, wraplength=130,
                             command=lambda: changeWindow(assignmentValueWindow.getAssignmentValue, window))
    DNButton = tk.Button(window, text="Deducția Naturală",
                         height=buttonHeight, width=buttonWidth, wraplength=130,
                         command=lambda: changeWindow(naturalDeductionWindow.naturalDeduction, window))
    quitButton = tk.Button(window, text="Quit", height=buttonHeight, width=buttonWidth // 3,
                           command=lambda: window.destroy())
    canvas = tk.Canvas(window, width=250, height=250)

    quizzButton.place(x=windowWidth / 6, y=windowHeight / 4 - 19 * buttonHeight)
    lpButton.place(x=windowWidth / 6, y=windowHeight / 4)
    treeButton.place(x=windowWidth / 6, y=windowHeight / 4 + 19 * buttonHeight)
    assignButton.place(x=windowWidth / 6, y=windowHeight / 4 + 38 * buttonHeight)
    DNButton.place(x=windowWidth / 6, y=windowHeight / 4 + 57 * buttonHeight)
    fnButton.place(x=windowWidth / 6, y=windowHeight / 4 + 76 * buttonHeight)
    quitButton.place(x=2, y=440)
    canvas.place(x=windowWidth / 2, y=windowHeight / 4)
    img = ImageTk.PhotoImage(Image.open("assets/fiilogo.png").resize((225, 225), Image.Resampling.LANCZOS))
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    title.config(font=('Helvatical bold', 20))
    title.place(x=windowWidth / 2, y=windowHeight / 6)

    window.mainloop()


def changeWindow(func, window):
    window.destroy()
    func()


if __name__ == "__main__":
    mainWindow()
