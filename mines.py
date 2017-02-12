#!/usr/bin/env python
import Tkinter as tk
from PIL import Image, ImageTk
import tkMessageBox as tkmsg
import random

# 9x9 16x16 30x16 maximum size 30x24 with 667 mines
# Beginner has 10 mines, Intermediate has 40 mines, and Expert has 99 mines
map_size = 9
mine_num = 10

class TileMap:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.tilenum = self.w * self.h
        self.tiles = [[0 for x in range(self.w)] for y in range(self.h)]

        for j in range(0, self.h):
            for i in range(0, self.w):
                self.tiles[j][i] = Tile(i, j)
        self.setBombs()
        return

    def setBombs(self):
        self.bombs = random.sample(range(0, self.w * self.h), mine_num)
        self.bombs.sort()
        self.bombs = [(b % self.w, b / self.h) for b in self.bombs]

        k = 0
        for j in range(0, self.h):
            for i in range(0, self.w):
                if k < mine_num and self.bombs[k] == (i, j):
                    self.tiles[j][i].changeType("bomb")
                    k += 1

    def endGame(self):
        for b in self.bombs:
            self.tiles[b[1]][b[0]].show()
        for j in range(0, self.h):
            for i in range(0, self.w):
                self.tiles[j][i].disable()

    def pressTile(self, x, y):
        if (x >= 0 and y >= 0 and x < self.w and y < self.h):
            if not self.tiles[y][x].isDisabled() and not self.bombIsIn(x, y):
                self.tiles[y][x].press()
        return

    def decreaseTiles(self):
        self.tilenum -= 1
        if self.tilenum == mine_num:
            msg = tkmsg.showinfo(":)", "You Win!")
            self.reset()
            return

    def bombIsIn(self, x, y):
        return (x >= 0 and y >= 0 and x < self.w and y < self.h) and self.tiles[y][x].isBomb()

    def reset(self):
        self.tilenum = self.w * self.h

        for j in range(0, self.h):
            for i in range(0, self.w):
                self.tiles[j][i].reset()
        self.setBombs()


class Tile:
    def __init__(self, posX, posY, t="normal"):
        self.disabled = False
        self.count = 0
        self.type = t
        self.flagged = False

        # Load graphics
        self.img = photoBank.getImage("normaltile")
        self.flagimg = photoBank.getImage("flag")
        self.disabledimg = photoBank.getImage("nothing")

        # Create the button
        self.button = tk.Button(app.lframe, image=self.img, command=self.press)

        # Position the button on the grid
        self.x = posX
        self.y = posY
        self.button.grid(row=self.y, column=self.x)

        self.button.bind('<Button-3>', self.rightClick)

    def press(self):
        if not self.disabled and not self.flagged:
            if self.isBomb():
                self.disabledimg = photoBank.getImage("bombed")
                board.endGame()
            else:
                self.checkNearby()

            #self.button.config(state=tk.DISABLED)
            self.disable()
            self.button.config(image=self.disabledimg)

            if self.count == 0 and not self.isBomb():
                board.pressTile(self.x+1, self.y)
                board.pressTile(self.x+1, self.y+1)
                board.pressTile(self.x+1, self.y-1)
                board.pressTile(self.x, self.y)
                board.pressTile(self.x, self.y+1)
                board.pressTile(self.x, self.y-1)
                board.pressTile(self.x-1, self.y)
                board.pressTile(self.x-1, self.y+1)
                board.pressTile(self.x-1, self.y-1)
            if not self.isBomb():
                board.decreaseTiles()

    def rightClick(self, event):
        if not self.disabled:
            if self.flagged:
                self.button.config(image=self.img)
            else:
                self.button.config(image=self.flagimg)

            self.flagged = not self.flagged

    def disable(self):
        self.disabled = True

    def isDisabled(self):
        return self.disabled or self.flagged

    def changeType(self, t):
        self.type = t

    def checkNearby(self):
        self.count = 0
        for j in range(0, 3):
            for i in range(0, 3):
                if i == 1 and j == 1:
                    continue
                elif board.bombIsIn(self.x-1 + i, self.y-1 + j):
                    self.count += 1
        if self.count > 0:
            self.disabledimg = photoBank.getImage("disabled" + str(self.count))

    def isBomb(self):
        return self.type == "bomb"

    def show(self):
        if self.isBomb():
            if self.flagged:
                self.img = photoBank.getImage("badflag")
            else:
                self.img = photoBank.getImage("bomb")
            self.button.config(image=self.img)

    def reset(self):
        self.disabled = False
        self.flagged = False
        self.button.grid()
        self.img = photoBank.getImage("normaltile")
        self.disabledimg = photoBank.getImage("nothing")
        self.button.config(state=tk.NORMAL)
        self.button.config(image=self.img)
        self.type = "normal"

class ImageBank:
    def __init__(self):
        self.images = {}
        return

    def getImage(self, name):
        if name in self.images:
            return self.images[name]
        else:
            print "Failed to fetch " + name
            return None

    def loadImage(self, name, filename):
        if name not in self.images:
            print "Loading " + filename + "..."
            photo = ImageTk.PhotoImage(Image.open(filename))

            if photo != None:
                self.images[name] = photo
                print "Loaded " + filename + " as " + name
            else:
                print "Failed to load " + filename
        return self.images[name]

    def freeImage(self, name):
        if name in self.images:
            del self.images[name]

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(row=0, column=0)
        top = self.winfo_toplevel()
        top.resizable(False, False)

    def createWidgets(self):
        self.menu = Menu(self)

        self.quitButton = tk.Button(self, text='Reset', command=self.reset)
        self.quitButton.grid(row=0, column=1, sticky=tk.W)

        self.lframe = tk.LabelFrame()
        self.lframe.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

    def reset(self):
        board.reset()

class Menu:
    def __init__(self, frame):
        self.fileButton = tk.Menubutton(frame, text="File")
        self.fileButton.menu = tk.Menu(self.fileButton, tearoff=0)
        self.fileButton['menu'] = self.fileButton.menu
        self.fileButton.grid(row=0, column=0, sticky=tk.W)

        self.fileButton.menu.add_command(label='New',
        command=app.reset)
        self.fileButton.menu.add_command(label='Quit',
        command=app.quit)

app = Application()

photoBank = ImageBank()
photoBank.loadImage("normaltile", "normaltile.png")
photoBank.loadImage("nothing", "nothing.png")
photoBank.loadImage("bombed", "bombed.png")
photoBank.loadImage("flag", "flag.png")
photoBank.loadImage("badflag", "badflag.png")
photoBank.loadImage("bomb", "bomb.png")

for i in range(1, 9):
    sti = str(i)
    photoBank.loadImage("disabled" + sti, sti + ".png")

app.createWidgets()
board = TileMap(map_size, map_size)

app.master.title('Mines')
app.mainloop()
