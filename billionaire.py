"""
Author: Thanos Moschou
Description: This is an imitation of 'Who wants to be a millionaire' question game. It is built with tkinter.
Last Modification Date: 10/12/2023
"""

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from random import randint
from random import shuffle

currentQuestionNumber = 0


def checkIfAnswerIsCorrect(givenAnswer):
    global currentQuestionNumber, questions

    #take only the letter from the line that contains the correct answer (keep in mind that it contains \n also which is unnecessary for my case)
    correct = questions[currentQuestionNumber][5][0]

    if(correct == givenAnswer):
        messagebox.showinfo("Yesssss", "This is correct!!!")
    else:
        messagebox.showerror("Nooooo", "This is wrong...\nThe correct is: " + correct)

    currentQuestionNumber += 1
    changeQuestion()
    

def audienceHelp(helpButton):
    global questions, possibilities
    possibilities = [0, 0, 0, 0]

    #For each question's answers check if the answer is correct. If yes then assign a possibility number from 50 to 70
    #else assign a possibility from 10 to 40 (both endpoints included)
    #Repeat this until sum of the possibilities is 100
    while True:
        for i in range(1, 5):
            if questions[currentQuestionNumber][i][0] == questions[currentQuestionNumber][5][0]: #take only the letter a, b, c or d and not the whole answer
                possibilities[i - 1] = randint(50, 70)
            else:
                possibilities[i - 1] = randint(0, 49)
        
        if sum(possibilities) == 100:
            messagebox.showinfo("Audience Results", "Audience said: \n" + 
                                "a : " + str(possibilities[0]) + "%\n" +
                                "b : " + str(possibilities[1]) + "%\n" +
                                "c : " + str(possibilities[2]) + "%\n" +
                                "d : " + str(possibilities[3]) + "%\n")
            break

    helpButton.config(state = DISABLED)


def fiftyFiftyHelp(helpButton):
    global questions, currentQuestionNumber 

    answerButtons = [answerAButton, answerBButton, answerCButton, answerDButton]
    wrongAnswersIndexes = []

    #For the current question save the indexes of the wrong answers in order to delete them from the screen
    #check the file indexing in the load questions function
    for i in range(1, 5):
        if questions[currentQuestionNumber][i][0] != questions[currentQuestionNumber][5][0]:
            wrongAnswersIndexes.append(i - 1) #in each question/answer nested list, answer indexes start from 1 so I need to subtract it in order to sync with the answer buttons list

    #delete 1 random value from all the wrong ones and delete the remaining ones from the screen
    wrongAnswersIndexes.pop(randint(0, len(wrongAnswersIndexes) - 1))

    #now you can traverse the buttons list and delete the answers
    for i in wrongAnswersIndexes:
        answerButtons[i].config(text = "", state = DISABLED)

    helpButton.config(state = DISABLED)


def placeQuestionToTheScreen():
    global questions, questionLabel, currentQuestionNumber, answerAButton, answerBButton, answerCButton, answerDButton

    questionLabel.config(text = questions[currentQuestionNumber][0])
    answerAButton.config(text = questions[currentQuestionNumber][1], state = ACTIVE)
    answerBButton.config(text = questions[currentQuestionNumber][2], state = ACTIVE)
    answerCButton.config(text = questions[currentQuestionNumber][3], state = ACTIVE)
    answerDButton.config(text = questions[currentQuestionNumber][4], state = ACTIVE)


def changeQuestion():
    global currentQuestionNumber, root

    if currentQuestionNumber <= numberOfQuestionsAvailable - 1: #Check if I have questions available. Last question is in index numberOfQuestionsAvailable - 1
        placeQuestionToTheScreen()
    else:
        messagebox.showinfo("End of game", "Thank you for playing!!!")
        root.destroy()


def loadQuestions():
    global questions, questionLabel, numberOfQuestionsAvailable

    questions = []
    numberOfQuestionsAvailable = 0

    #I have a list that contains lists. Each nested list is a list that contains the question, the possible answers and the correct answer
    #Inside each nested list the indexing goes like this:
    #0: Question
    #1: Answer A
    #2: Answer B
    #3: Answer C
    #4: Answer D
    #5: Correct answer
    with open("questions.txt", "r", encoding = "utf-8") as filename:
        ctr = 0
        nestedQuestionList = []
        for quest in filename:
            nestedQuestionList.append(quest)
            if ctr == 5:
                numberOfQuestionsAvailable += 1 
                ctr = 0 #begin with a new question-answers set
                questions.append(nestedQuestionList)
                nestedQuestionList = []
            else:
                ctr += 1
    
    #suffle the list multiple times in order to receive the questions with random order
    for i in range(10):
        shuffle(questions) 
    changeQuestion()
    

def initializeScreen():
    global root, titleLabel, questionLabel, answerAButton, answerBButton, answerCButton, answerDButton
    global askTheAudienceImage, askTheAudienceHelpButton, fiftyFiftyImage, fiftyFiftyHelpButton

    titleLabel = Label(root, text = "Do you want to become a Billionaire?", bg = "black", fg = "gold", font = ("Arial", 24))
    titleLabel.place(x = 125, y = 5, width = 750, height = 90)

    questionLabel = Label(root, bg = "#000076", fg = "white", font = ("Arial", 24))
    questionLabel.place(x = 130, y = 155, width = 700, height = 90)

    answerAButton = Button(root, bg = "#000076", fg = "white", font = ("Arial", 15), 
                           bd = 0.1, activebackground = "#000076", activeforeground = "white", command = lambda m = "a": checkIfAnswerIsCorrect(m))
    answerAButton.place(x = 100, y = 380, width = 300, height = 50)

    answerBButton = Button(root, bg = "#000076", fg = "white", font = ("Arial", 15), 
                           bd = 0.1, activebackground = "#000076", activeforeground = "white", command = lambda m = "b": checkIfAnswerIsCorrect(m))
    answerBButton.place(x = 545, y = 380, width = 300, height = 50)

    answerCButton = Button(root, bg = "#000076", fg = "white", font = ("Arial", 15), 
                           bd = 0.1, activebackground = "#000076", activeforeground = "white", command = lambda m = "c": checkIfAnswerIsCorrect(m))
    answerCButton.place(x = 100, y = 530, width = 300, height = 50)

    answerDButton = Button(root, bg = "#000076", fg = "white", font = ("Arial", 15), 
                           bd = 0.1, activebackground = "#000076", activeforeground = "white", command = lambda m = "d": checkIfAnswerIsCorrect(m))
    answerDButton.place(x = 545, y = 530, width = 300, height = 50)

    askTheAudienceImage = ImageTk.PhotoImage(Image.open("assets/askTheAudienceHelp.jpg").resize((30, 30)))
    askTheAudienceHelpButton = Button(root, image = askTheAudienceImage, width = 30, height = 30, bg = "black", activebackground = "black", bd = 0.1)
    askTheAudienceHelpButton.place(x = 830, y = 40)
    askTheAudienceHelpButton.config(command = lambda helpButton = askTheAudienceHelpButton : audienceHelp(helpButton)) #I wrote the command after I declared the button because I want to pass the button to my lambda

    fiftyFiftyImage = ImageTk.PhotoImage(Image.open("assets/fiftyFiftyHelp.jpg").resize((30, 30)))
    fiftyFiftyHelpButton = Button(root, image = fiftyFiftyImage, width = 30, height = 30, bg = "black", activebackground = "black", bd = 0.1)
    fiftyFiftyHelpButton.place(x = 870, y = 40)
    fiftyFiftyHelpButton.config(command = lambda helpButton = fiftyFiftyHelpButton : fiftyFiftyHelp(helpButton))

    authorLabel = Label(root, text = "v1.0 by Thanos Moschou, 2023", bg = "black", fg = "gold", font = ("Arial", 8))
    authorLabel.place(x = 780, y = 665)


def centerWindowToTheScreen(window):
    appWidth = 950
    appHeight = 690
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()

    #center the window to the screen
    x = (screenWidth / 2) - (appWidth / 2)
    y = (screenHeight / 2) - (appHeight / 2)

    window.title("Billionaire!")
    window.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")
    window.resizable(False, False)


def welcomeScreen():
    global welcomeWindow, startButton
    welcomeScreenDuration = 4000 #in ms

    welcomeWindow = Tk()
    centerWindowToTheScreen(welcomeWindow)

    welcomeImage = ImageTk.PhotoImage(Image.open("assets/welcomeLogo.jpg").resize((950, 690)))
    welcomeBackground = Label(welcomeWindow, image = welcomeImage)
    welcomeBackground.grid()

    authorLabel = Label(welcomeWindow, text = "v1.0 by Thanos Moschou, 2023", bg = "#221a3f", fg = "gold", font = ("Arial", 8))
    authorLabel.place(x = 780, y = 665)

    icon = ImageTk.PhotoImage(Image.open("assets/welcomeLogo.ico"))
    welcomeWindow.iconphoto(False, icon)

    welcomeWindow.after(welcomeScreenDuration, lambda : welcomeWindow.destroy())
    welcomeWindow.mainloop()


def main():
    global root
    
    root = Tk()
    centerWindowToTheScreen(root)
    
    backgroundImage = ImageTk.PhotoImage(Image.open("assets/background.png").resize((950, 690)))
    background = Label(root, image = backgroundImage)
    background.grid()

    icon = ImageTk.PhotoImage(Image.open("assets/welcomeLogo.ico"))
    root.iconphoto(False, icon)

    initializeScreen()
    loadQuestions()
    root.mainloop()

welcomeScreen()
main()