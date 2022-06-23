import math
import random
import tkinter as tk
from helpers import functions
import json

score = 0
stance = 0
numberOfQuestions = 10


class Question:
    def __init__(self, question, correct, answers):
        self.question = question
        self.answers = answers
        self.correct = correct


def createButtons(window, questions):
    global stance
    for widgets in window.winfo_children():
        widgets.destroy()

    buttonHeight, buttonWidth = 3, 20
    output = tk.Text(window, height=10, width=43, wrap=tk.WORD)
    output.place(x=200, y=20)
    functions.insertInTextbox(output, f"{stance + 1}. {questions[stance].question}")
    button1 = tk.Button(window, text=questions[stance].answers[0], height=buttonHeight, width=buttonWidth,
                        wraplength=130, command=lambda: buttonClick(questions, questions[stance].answers[0], window))
    button2 = tk.Button(window, text=questions[stance].answers[1], height=buttonHeight, width=buttonWidth,
                        wraplength=130, command=lambda: buttonClick(questions, questions[stance].answers[1], window))
    button3 = tk.Button(window, text=questions[stance].answers[2], height=buttonHeight, width=buttonWidth,
                        wraplength=130, command=lambda: buttonClick(questions, questions[stance].answers[2], window))
    button4 = tk.Button(window, text=questions[stance].answers[3], height=buttonHeight, width=buttonWidth,
                        wraplength=130, command=lambda: buttonClick(questions, questions[stance].answers[3], window))
    backButton = tk.Button(window, text="Back", height=buttonHeight, width=10,
                           command=lambda: functions.goBackToMainWindow(window))
    button1.place(x=200, y=200)
    button2.place(x=400, y=200)
    button3.place(x=200, y=270)
    button4.place(x=400, y=270)
    backButton.place(x=2, y=440)


def buttonClick(questions, answer, window):
    global stance, score
    if questions[stance].correct == answer:
        score += 1

    buttonHeight, buttonWidth = 3, 30
    stance += 1
    if stance == numberOfQuestions:
        for widgets in window.winfo_children():
            widgets.destroy()

        scoreLabel = tk.Label(window,
                              text=f"Scorul tău a fost {math.floor(score / numberOfQuestions * 100)}%."
                                   f"\n Ai răspuns corect la {score} din {numberOfQuestions} întrebări.",
                              borderwidth=0)
        button_back = tk.Button(window, text="Back", height=buttonHeight, width=10,
                                command=lambda: functions.goBackToMainWindow(window))
        button_retry = tk.Button(window, text="Retry", height=buttonHeight, width=10,
                                 command=lambda: retry(window))

        scoreLabel.place(x=210, y=200)
        scoreLabel.config(font=('Helvatical bold', 15))
        button_back.place(x=2, y=440)
        button_retry.place(x=85, y=440)
    else:
        createButtons(window, questions)


def retry(window):
    window.destroy()
    global score, stance
    score = 0
    stance = 0
    quizz()


def quizz():
    window = tk.Tk()
    window.title("Chestionar")
    windowWidth = 750
    windowHeight = 500
    centerX = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
    centerY = int(window.winfo_screenheight() / 2 - windowHeight / 2)
    window.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
    window.resizable(False, False)

    questions = []

    with open('info/questions.json') as file:
        data = json.load(file)
        for question in random.sample(data["questions"], k=numberOfQuestions):
            random.shuffle(question["answers"])
            questions.append(Question(question["question"], question["correct"], question["answers"]))

    createButtons(window, questions)

    window.mainloop()
