import tkinter
from html.parser import HTMLParser
import threading
import pickle
import random

class textParser(HTMLParser):

    parsingWords = []
    startTag = ""
    currentTag = ""
    currentWords = {}

    def handle_starttag(self, tag, attrs):
        self.currentTag = tag
        if tag == "br":
            self.parsingWords.append(self.currentWords.copy())

    def handle_endtag(self, tag):
        if self.currentTag == tag:
            self.currentTag = ""


    def handle_data(self, data):
        if self.currentTag == "a":
            self.currentWords["eng"] = data.strip()
        elif self.currentTag == "":
            self.currentWords["rus"] = data.strip()

class GUI:

    _ITEMS_WIDTH = 20
    _currentWord = dict()

    def __init__(self):
        """

        :rtype : object
        """
        self.setupGUI()

    def setupGUI(self):
        self.root = tkinter.Tk()
        self.root.title = "English"
        self.root.resizable(width=False, height=False)
        self.root.geometry("400x100+100+80")
        self.root.wm_attributes("-topmost", 1)

        dictToTranslate = self.randomWord
        self.wordLabel = tkinter.Label(self.root,
                                  text=dictToTranslate["eng"],
                                  width=self._ITEMS_WIDTH,height=2)
        self.wordLabel.grid(row = 1, column = 1)

        self.entryText = tkinter.Entry(self.root,
                                    width=self._ITEMS_WIDTH)
        self.entryText.grid(row = 1,column = 2)
        self.entryText.focus()

        errorLabel = tkinter.Label(self.root,
                                        width = self._ITEMS_WIDTH,
                                        text = "", bg = "white")
        errorLabel.grid(row = 2, column = 1, columnspan = 2)
        self._errorLabel = errorLabel

        checkButton = tkinter.Button(self.root,
                                    text="Check",
                                    width = self._ITEMS_WIDTH,
                                    bg="red",fg="black")
        checkButton.bind("<Button-1>", self.tapCheckButton)
        checkButton.grid(row = 3, column = 1)

        helpButton = tkinter.Button(self.root,
                                    text="Show answer",
                                    width = self._ITEMS_WIDTH,
                                    bg = "red", fg = "black")
        helpButton.bind("<Button-1>", self.tapHelpButton)
        helpButton.grid(row = 3, column = 2)

        self.timerFunc()
        self.root.mainloop()

    def tapCheckButton(self, event):
        translatedWord = self.entryText.get().lower()
        currentWord =  self._currentWord["rus"].split(';')[0].split(',')[0].lower()

        if translatedWord == currentWord:
            self.root.withdraw()
            self._errorLabel.config(bg = "white", text = "")
        else:
            self._errorLabel.config(bg = "yellow", text = "wrong")

    def tapHelpButton(self, event):
        self.entryText.delete(0, tkinter.END)
        self.entryText.insert(0, self._currentWord["rus"])

    def showGui(self):
        try:
            self.root.deiconify()
            dictToTranslate = self.randomWord
            self.entryText.delete(0, tkinter.END)
            self.wordLabel.configure(text=dictToTranslate["eng"])
        except Exception:
            self.root.quit()
            print(Exception)

    def timerFunc(self):
        self.showGui()
        threading.Timer(60.0, self.timerFunc).start()

    @property
    def randomWord(self) -> dict:
        """
            :rtype : dictionary
         """
        words = open("wordsDB", "rb")
        wordsToTranslate = pickle.load(words)
        words.close()

        indexNumber = random.randint(1, 999)
        assert isinstance(indexNumber, int)
        self._currentWord = wordsToTranslate[indexNumber]
        return self._currentWord


"""
textFile = open("words.txt", "r")
textForParse = textFile.read().replace("\n","").replace("-","")
textFile.close()

parser = textParser()
parser.feed(textForParse)
storeWords = parser.parsingWords

dbFile = open("wordsDB", "wb")
pickle.dump(storeWords,dbFile)
dbFile.close()

print(storeWords)
parsedWords = open("Translated_words","w")
parsedWords.write(storeWords)
parsedWords.close()
"""

gui = GUI()

threading.Thread(target = gui.setupGUI(),args=gui).start()
#timerFunc()
