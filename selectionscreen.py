import Tkinter as tk
from PIL import Image, ImageTk
from imagebank import *

class SelectScreen(tk.Frame):
    def __init__(self, app=None):
        tk.Frame.__init__(self, app)
        self.app = app
        self.grid()
        self.selFrame = tk.LabelFrame(self)
        self.selFrame.grid()
        self.setupDifficultySettings()
        self.createSelectionWidgets()

    def setVisible(self, visible):
        if visible:
            self.grid()
        else:
            self.grid_forget()

    def setupDifficultySettings(self):
        self.difficultySettings = {}

        setting = {}
        setting["map_width"] = 9
        setting["map_height"] = 9
        setting["mine_num"] = 10
        self.difficultySettings["Beginner"] = setting

        setting = {}
        setting["map_width"] = 16
        setting["map_height"] = 16
        setting["mine_num"] = 40
        self.difficultySettings["Intermediate"] = setting

        setting = {}
        setting["map_width"] = 30
        setting["map_height"] = 24
        setting["mine_num"] = 99
        self.difficultySettings["Advanced"] = setting

    def createSelectionWidgets(self):
        beginnerSelImg = photoBank.loadImage("9x9", "images/9x9.png")
        intermediateSelImg = photoBank.loadImage("16x16", "images/16x16.png")
        advancedSelImg = photoBank.loadImage("30x24", "images/30x24.png")
        customSelImg = photoBank.loadImage("XxY", "images/XxY.png")

        self.beginnerBut = self.createSelButton(0, 0, "9x9", lambda: self.setupGame("Beginner"))
        self.intermediateBut = self.createSelButton(0, 1, "16x16", lambda: self.setupGame("Intermediate"))
        self.advancedBut = self.createSelButton(1, 0, "30x24", lambda: self.setupGame("Advanced"))
        self.customBut = self.createSelButton(1, 1, "XxY", self.quit)

    def createSelButton(self, x, y, img, cmd):
        img = photoBank.getImage(img)
        button = tk.Button(self.selFrame, image=img, command=cmd)
        button.grid(row=x, column=y, padx=2, pady=2, sticky=tk.N+tk.E+tk.S+tk.W)
        self.selFrame.columnconfigure(x, minsize=128)
        self.selFrame.rowconfigure(y, minsize=128)
        return button

    def setupGame(self, difficulty):
        dif = self.difficultySettings[difficulty]
        self.app.map_width = dif["map_width"]
        self.app.map_height = dif["map_height"]
        self.app.mine_num = dif["mine_num"]

        self.app.startGame()
