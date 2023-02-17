from tkinter import *
from PIL import ImageTk, Image
import os
import random
from tkinter import messagebox 
from tkinter import simpledialog

class SaveManGame:
    def __init__(self, wordlist):
        self.wordlist = wordlist
        self.word = self.getWord()
        self.remainingGuesses = 6
        self.guesses = set()

    def getWord(self):
        return random.choice(self.wordlist)

    def guessLetter(self, letter):
        self.guesses.add(letter)

        if letter not in self.word:
            self.remainingGuesses -= 1

    def getMaskedWord(self):
        return ' '.join(c if c in self.guesses else '_' for c in self.word)

    def isGameOver(self):
        return set(self.word) <= self.guesses or self.remainingGuesses == 0

    def playAgain(self):
        self.__init__(self.wordlist)


class SaveManGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.timer = 30
        self.isCustomWord = False

        self.images = []
        for i in range(7):
            imgPath = os.path.join('images', f'saveman{i}.png')
            img = Image.open(imgPath)
            img = img.resize((200, 200))
            img = ImageTk.PhotoImage(img)
            self.images.append(img)

        self.gameMode = Button(self.root, text='Game Mode', command=self.inputWord)
        self.gameMode.pack()

        self.guessesTextBox = Text(self.root, width=12, height=12, state=DISABLED)
        self.guessesTextBox.pack(side = RIGHT, anchor=N, padx=10, pady=10, fill=Y)

        self.imageLabel = Label(root, image=self.images[0])
        self.imageLabel.pack()

        self.wordLabel = Label(self.root, text=self.game.getMaskedWord())
        self.guessesLabel = Label(self.root, text=f'Remaining Guesses: {self.game.remainingGuesses}')
        self.inputLabel = Label(self.root, text='Enter a letter:')
        self.inputEntry = Entry(self.root)
        self.inputButton = Button(self.root, text='Guess', command=self.guess)

        self.wordLabel.pack()
        self.guessesLabel.pack()
        self.inputLabel.pack()
        self.inputEntry.pack()
        self.inputButton.pack()

        self.timerLabel = Label(self.root, text=f'Time Remaining:\n {self.timer}')
        self.timerLabel.pack()
        self.startTimer()

    def inputWord(self):
        inputWindow = Toplevel(self.root)
        inputWindow.title('Choose a Word')
        inputWindow.geometry('150x50')
        inputWindow.resizable(0,0)

        def selectCustomWord():
            nonlocal word
            word = simpledialog.askstring(title='Custom Word', prompt='Enter a custom word:\nWord most be less than 20 characters.')
            if word is None or word == '':
                return
            elif word.__len__() >= 21:
                selectPredefinedWord()
            word = word.lower()
            self.game.word = word
            self.game.remainingGuesses = 6
            self.game.guesses = set()
            self.updateLabels()
            self.timer = 30
            self.playAgain()
            inputWindow.destroy()

        def selectPredefinedWord():
            nonlocal word
            word = self.game.getWord()
            self.game.word = word
            self.game.remainingGuesses = 6
            self.game.guesses = set()
            self.updateLabels()
            self.timer = 30
            self.playAgain()
            inputWindow.destroy()   

        word = None
        customWordButton = Button(inputWindow, text='Custom Word', command=selectCustomWord)
        customWordButton.pack()
        predefinedWordButton = Button(inputWindow, text='Predefined Word', command=selectPredefinedWord)
        predefinedWordButton.pack()

        inputWindow.grab_set()
        self.root.wait_window(inputWindow)

        if word:
            self.game.word = word
            self.updateLabels()


    def startTimer(self):
        if self.game.isGameOver():
            return
        if self.timer >= 1:
            self.timer -= 1
            self.timerLabel.config(text=f'Time Remaining:\n {self.timer}')
            self.root.after(1000, self.startTimer)
        else:
            self.inputEntry.config(state='disabled')
            self.gameOver()

    def guess(self):
        letter = self.inputEntry.get()
        if not letter:
            messagebox.showerror("Error, Foolish move", "Enter a vaild letter. \n \nPress enter to continue.")
            return
        if self.isCustomWord:
            self.game.word = self.game.maskedWord
            self.isCustomWord = False
            self.playAgain()
        else:
            self.game.guessLetter(letter)
            self.updateLabels()
            self.guessesTextBox.config(state=NORMAL)
            self.guessesTextBox.insert(END, f"{letter}, ")
            self.guessesTextBox.config(state=DISABLED)
            self.inputEntry.delete(0, END)
            self.inputEntry.focus()
            self.timer = 30 
            self.timerLabel.config(text=f'Time Remaining:\n {self.timer}')

        if self.game.isGameOver():
            self.gameOver()
        else:
            self.nextImage(self.game.remainingGuesses)
            self.inputEntry.config(state='normal')

    def nextImage(self, remainingGuesses):
        self.imageLabel.configure(image=self.images[6 - remainingGuesses])
        

    def gameOver(self):
        if set(self.game.word) <= self.game.guesses:
            msg ='You win!\nThe word was \n' + self.game.word
        else:
            msg ='You lose! \nThe word was \n' + self.game.word 
            self.imageLabel.configure(image=self.images[6])
        self.wordLabel.config(text=msg)
        self.guessesLabel.config(text='')
        self.inputLabel.config(text='')
        self.inputEntry.config(state='disabled')
        self.inputButton.config(text= 'Play Again', command=self.playAgain)

    
    def playAgain(self):
        self.game.playAgain()
        self.updateLabels()
        self.inputEntry.config(state=NORMAL)
        self.inputEntry.delete(0, END)
        self.inputButton.config(text='Guess', command=self.guess)
        self.nextImage(6)
        self.guessesTextBox.config(state=NORMAL)
        self.guessesTextBox.delete(1.0, END)
        self.guessesTextBox.config(state=DISABLED)
        self.timer = 30
        self.timerLabel.config(text=f'Time Remaining:\n {self.timer}')
        self.startTimer()


    def updateLabels(self):
        self.wordLabel.config(text=self.game.getMaskedWord())
        self.guessesLabel.config(text=f'Remaining Guesses: {self.game.remainingGuesses}')

icon = Image.open("images/saveman6.png")
icon = icon.convert("RGBA")
icon.save("icon.ico", format="ICO")

root = Tk()
root.title("SaveMan")
root.geometry("320x400")
root.iconbitmap("icon.ico")
root.resizable(0, 0)
list = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango", "lemon", "pear", "peach", "strawberry", "blueberry", "raspberry", "blackberry", "watermelon", "grape", "grapefruit", "pineapple", "apricot", "avocado", "coconut", "cantaloupe", "honeydew", "papaya", "tomato", "potato", "carrot", "pepper", "onion", "garlic", "ginger", "cucumber", "lettuce", "spinach", "broccoli", "cauliflower", "asparagus", "mushroom", "zucchini", "squash", "beetroot", "corn", "sweetcorn", "sweetpotato", "yam", "eggplant", "aubergine", "peas", "beans", "lentils", "pumpkin", "chili", "chilli", "chocolate", "candy", "sweets", "programmer", "develeper", "ide", "compiler", "interpreter", "debugger", "algorithm", "variable", "function", "loop", "array", "string", "integer", "float", "boolean", "list", "dictionary", "tuple", "set", "class", "object", "method", "attribute", "inheritance", "polymorphism", "encapsulation", "abstraction", "file", "module", "package", "library", "framework", "database", "network", "server", "client", "website", "webpage", "webapp", "webserver", "webbrowser", "webhost", "webdeveloper", "webdesigner", "webmaster", "webhosting", "webhostprovider", "amongus", "minecraft", "cod", "fortnite", "roblox", "gta", "fifa", "pes", "pubg", "chess", "ludo", "snake", "monopoly", "uno", "pictionary", "charades", "scrabble", "battleship", "checkers", "chess", "backgammon", "go", "poker", "dominoes", "mahjong", "solitaire", "texas holdem", "blackjack", "python", "java", "c", "c++", "c#", "javascript", "html", "css", "php", "sql", "swift", "kotlin", "dart", "ruby", "perl", "assembly", "bash", "powershell", "visual basic", "fortran", "matlab", "go", "rust", "scala", "haskell", "prolog", "lisp", "scheme", "erlang", "clojure", "coffeescript", "typescript", "lua", "groovy", "julia", "delphi", "pascal", "math", "english", "swedish", "spanish", "french", "german", "italian", "portuguese", "chinese", "japanese", "korean", "arabic", "hebrew", "russian", "turkish", "polish", "danish", "norwegian", "finnish", "dutch", "greek", "romanian", "hungarian", "czech", "slovak", "slovenian", "croatian", "serbian", "bulgarian", "ukrainian", "estonian", "latvian", "lithuanian", "albanian", "maltese", "irish", "welsh", "scottish", "english", "afrikaans", "indonesian", "malay", "thai", "vietnamese", "cambodian", "laotian", "burmese", "mongolian", "tibetan", "kazakh", "kyrgyz", "uzbek", "tajik", "turkmen", "azerbaijani", "georgian", "arme", "sofia", "sofia", "sofia", "sofia", "sofia", "sofia"]
game = SaveManGame(list)
gui = SaveManGUI(root, game)

root.mainloop()