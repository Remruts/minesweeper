#!/usr/bin/env python
import Tkinter as tk
from ticker import *
from tilemap import *
from selectionscreen import *
from game import *

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(row=0, column=0)
        top = self.winfo_toplevel()
        top.resizable(False, False)

        # 9x9 16x16 30x16 maximum size 30x24 with 667 mines
        # Beginner has 10 mines, Intermediate has 40 mines, and Expert has 99 mines
        self.map_width = 9
        self.map_height = 9
        self.mine_num = 10
        self.difficulty = "Beginner"

        self.menu = Menu(self)
        self.selScreen = SelectScreen(self)
        self.game = Game(app=self)

    def setDifficulty(self, diff):
        self.difficulty = diff

    def startGame(self):
        self.selScreen.setVisible(False)
        self.game.finish()
        self.game = Game(app=self)
        self.game.start()

    def reset(self):
        self.selScreen.setVisible(True)
        self.game.finish()
        self.game.grid_forget()

    def cleanup(self):
        self.game.finish()

class Menu:
    def __init__(self, app):
        self.fileButton = tk.Menubutton(app, text="File")
        self.fileButton.menu = tk.Menu(self.fileButton, tearoff=0)
        self.fileButton['menu'] = self.fileButton.menu
        self.fileButton.grid(row=0, column=0, sticky=tk.W)

        self.fileButton.menu.add_command(label='New',
        command=app.reset)
        self.fileButton.menu.add_command(label='Quit',
        command=app.quit)

app = Application()
app.master.title('Mines')
app.mainloop()
app.cleanup()
