#!/usr/bin/env python
import Tkinter as tk
from PIL import Image, ImageTk
import random

# 9x9 16x16 30x16 maximum size 30x24 with 667 mines
# Beginner has 10 mines, Intermediate has 40 mines, and Expert has 99 mines
map_size = 9
mine_num = 10

class TileMap:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.tiles = [[0 for x in range(self.w)] for y in range(self.h)]

        self.bombs = random.sample(range(0, self.w * self.h), mine_num)
        self.bombs.sort()
        print self.bombs
        self.bombs = [(b % self.w, b / self.h) for b in self.bombs]
        print self.bombs

        k = 0
        for j in range(0, self.h):
            for i in range(0, self.w):
                if k < mine_num and self.bombs[k] == (i, j):
                    print self.bombs[k]
                    self.tiles[j][i] = BombTile(i, j)
                    k += 1
                else:
                    self.tiles[j][i] = Tile(i, j)
        return

    def endGame(self):
        for b in self.bombs:
            self.tiles[b[1]][b[0]].show()
        for j in range(0, self.h):
            for i in range(0, self.w):
                self.tiles[j][i].disable()

    def pressTile(self, x, y):
        if (x >= 0 and y >= 0 and x < self.w and y < self.h):
            if not self.bombIsIn(x, y):
                self.tiles[y][x].press()
        return

    def bombIsIn(self, x, y):
        return (x >= 0 and y >= 0 and x < self.w and y < self.h) and self.tiles[y][x].isBomb()

class Tile:
    def __init__(self, posX, posY):
        self.disabled = False
        self.count = 0

        # Load graphics
        self.img = photoBank.getImage("smiley")
        self.disabledimg = photoBank.getImage("nothing")

        # Create the button
        self.button = tk.Button(app.lframe, image=self.img, command=self.press)

        # Position the button on the grid
        self.x = posX
        self.y = posY
        self.button.grid(row=self.y, column=self.x)

    def press(self):
        if self.disabled == False:
            if not self.isBomb():
                self.checkNearby()
            self.button.config(state=tk.DISABLED)
            #self.button.config(image=self.disabledimg)
            self.disable()
            self.button.pack_forget()

            self.button = tk.Label(app.lframe, image=self.disabledimg)
            self.button.grid(row=self.y, column=self.x)

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

    def disable(self):
        self.disabled = True

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
        return False

class BombTile(Tile):
    def __init__(self, posX, posY):
        Tile.__init__(self, posX, posY)
        self.img = photoBank.getImage("bomb")
        self.disabledimg = photoBank.getImage("bombed")

    def press(self):
        Tile.press(self)
        board.endGame()

    def isBomb(self):
        return True

    def show(self):
        if not self.disabled:
            self.button.config(image=self.img)

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
        self.grid()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Reset', command=self.quit)
        self.quitButton.grid()

        self.lframe = tk.LabelFrame()
        self.lframe.grid()


#finished = False
#while not finished:
app = Application()
photoBank = ImageBank()
photoBank.loadImage("smiley", "smiley.png")
photoBank.loadImage("nothing", "nothing.png")
photoBank.loadImage("bombed", "bombed.png")
photoBank.loadImage("bomb", "bomb.png")
for i in range(1, 9):
    sti = str(i)
    photoBank.loadImage("disabled" + sti, sti + ".png")
app.createWidgets()
board = TileMap(map_size, map_size)
app.master.title('Mines')
app.mainloop()
