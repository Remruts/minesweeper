#!/usr/bin/env python
import Tkinter as tk
from PIL import Image, ImageTk

class TileMap:
    def __init__(self, size):
        self.w = size
        self.h = size
        self.tiles = [[0 for x in range(self.w)] for y in range(self.h)]

        for i in range(0, 10):
            for j in range(0, 10):
                if (j == 1):
                    button = BombTile(i, j)
                else:
                    button = Tile(i, j)
        return

    def bombIsIn(self, x, y):
        return self.tiles[x][y].isBomb()

class Tile:
    def __init__(self, posX, posY):
        # Load graphics
        self.img = photoBank.getImage("smiley")
        self.disabledimg = photoBank.getImage("nothing")
        # Create the button
        self.button = tk.Button(app.lframe, image=self.img, command=self.press)
        # Position the button on the grid
        self.button.grid(row=posX, column=posY)

    def press(self):
        self.button.config(state=tk.DISABLED)
        self.button.config(image=self.disabledimg)

    def isBomb(self):
        return False

class BombTile(Tile):
    def __init__(self, posX, posY):
        Tile.__init__(self, posX, posY)
        self.disabledimg = photoBank.getImage("bombed")

    def isBomb(self):
        return True

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
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid()

        self.lframe = tk.LabelFrame()
        self.lframe.grid()





app = Application()
photoBank = ImageBank()
photoBank.loadImage("smiley", "smiley.png")
photoBank.loadImage("nothing", "nothing.png")
photoBank.loadImage("bombed", "bombed.png")
for i in range(1, 9):
    sti = str(i)
    photoBank.loadImage("disabled" + sti, sti + ".png")
app.createWidgets()
board = TileMap(10)
app.master.title('Mines')
app.mainloop()
