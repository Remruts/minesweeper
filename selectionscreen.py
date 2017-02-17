import Tkinter as tk
from PIL import Image, ImageTk
import tkFont
from imagebank import *

class SelectScreen(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app)
        self.app = app
        self.grid()
        self.selFrame = tk.LabelFrame(self)
        self.selFrame.grid()
        self.setupDifficultySettings()
        self.createSelectionWidgets()
        self.custom_screen = customScreen(self)

    def setVisible(self, visible):
        if visible:
            self.grid()
            self.selFrame.grid()
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
        self.customBut = self.createSelButton(1, 1, "XxY", self.customSelected)

    def createSelButton(self, x, y, img, cmd):
        img = photoBank.getImage(img)
        button = tk.Button(self.selFrame, image=img, command=cmd)
        button.grid(row=x, column=y, padx=2, pady=2, sticky=tk.N+tk.E+tk.S+tk.W)
        self.selFrame.columnconfigure(x, minsize=128)
        self.selFrame.rowconfigure(y, minsize=128)
        return button

    def customSelected(self):
        self.selFrame.grid_forget()
        self.custom_screen.setVisible(True)

    def setupGame(self, difficulty):
        if difficulty != "Custom":
            dif = self.difficultySettings[difficulty]
            self.app.map_width = dif["map_width"]
            self.app.map_height = dif["map_height"]
            self.app.mine_num = dif["mine_num"]
        else:
            self.app.map_width = self.map_width
            self.app.map_height = self.map_height
            self.app.mine_num = self.mine_num

        self.app.setDifficulty(difficulty)
        self.app.startGame()

class customScreen(tk.Frame):
    def __init__(self, app=None):
        tk.Frame.__init__(self, app)
        self.app = app

        self.sel_width = tk.IntVar()
        self.sel_height = tk.IntVar()
        self.sel_mines = tk.IntVar()

        self.addWidgets()

    def setVisible(self, visible):
        if visible:
            self.grid(padx=16, pady=8)
        else:
            self.grid_forget()

    def addWidgets(self):
        # max 30x24 with 667 mines

        helv24 = tkFont.Font(family='Helvetica', size=24, weight='bold')
        helv16 = tkFont.Font(family='Helvetica', size=16)

        self.textw = tk.Label(self, text="Width", font=helv24)
        self.textw.grid(row=0, column=0, sticky=tk.W)
        self.texth = tk.Label(self, text="Height", font=helv24)
        self.texth.grid(row=1, column=0, sticky=tk.W)
        self.textm = tk.Label(self, text="Mines", font=helv24)
        self.textm.grid(row=2, column=0, sticky=tk.W)

        self.sel_width.set(9)
        self.width_select = tk.Spinbox(self, from_=8, to=30, textvariable=self.sel_width, font=helv24, width=3)
        self.width_select.grid(row=0, column=1, padx=2, pady=2, sticky=tk.E)

        self.sel_height.set(9)
        self.height_select = tk.Spinbox(self, from_=8, to=24, textvariable=self.sel_height, font=helv24, width=3)
        self.height_select.grid(row=1, column=1, padx=2, pady=2, sticky=tk.E)

        self.sel_mines.set(10)
        self.minenum_select = tk.Spinbox(self, from_=1, to=667, textvariable=self.sel_mines, font=helv24, width=3)
        self.minenum_select.grid(row=2, column=1, padx=2, pady=2, sticky=tk.E)

        self.start_button = tk.Button(self, text="Start", font=helv16, command=self.startGame)
        self.start_button.grid(row=3, column=1, sticky=tk.S)

        self.back_button = tk.Button(self, text="Back", font=helv16, command=self.back)
        self.back_button.grid(row=3, column=0, sticky=tk.S)

    def startGame(self):
        mine_num = self.sel_mines.get()
        w = self.sel_width.get()
        h = self.sel_height.get()
        mine_num = min(mine_num, int((h * w) - (h * w * 0.05)))

        self.app.map_width = w
        self.app.map_height = h
        self.app.mine_num = mine_num

        self.setVisible(False)
        self.app.setupGame("Custom")

    def back(self):
        self.setVisible(False)
        self.app.setVisible(True)
