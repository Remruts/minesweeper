#!/usr/bin/env python
import Tkinter as tk
from PIL import Image, ImageTk
from ticker import *
from tilemap import *
import time

# 9x9 16x16 30x16 maximum size 30x24 with 667 mines
# Beginner has 10 mines, Intermediate has 40 mines, and Expert has 99 mines
map_size = 9
mine_num = 10

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(row=0, column=0)
        top = self.winfo_toplevel()
        top.resizable(False, False)

        # start ticker
        self.start_time = time.time()
        self.diff_time = self.start_time - time.time()
        self.str_diff_time = tk.StringVar()
        self.str_diff_time.set('time: ' + str(int(self.diff_time)))
        self.ticker = Ticker(1, self.update)

        self.loadGraphics()
        self.createWidgets()

    def loadGraphics(self):
        photoBank.loadImage("normaltile", "images/normaltile.png")
        photoBank.loadImage("nothing", "images/nothing.png")
        photoBank.loadImage("bombed", "images/bombed.png")
        photoBank.loadImage("flag", "images/flag.png")
        photoBank.loadImage("badflag", "images/badflag.png")
        photoBank.loadImage("bomb", "images/bomb.png")

        for i in range(1, 9):
            sti = str(i)
            photoBank.loadImage("disabled" + sti, "images/" + sti + ".png")

    def createWidgets(self):
        #self.menu = Menu(self)

        self.quitButton = tk.Button(self, text='Reset', command=self.reset)
        self.quitButton.grid(row=0, column=1, sticky=tk.W)

        self.lframe = tk.LabelFrame()
        self.lframe.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

        self.clock_label = tk.Label(self, textvariable=self.str_diff_time)
        self.clock_label.grid(row=1, column=0, sticky=tk.E)

    def update(self):
        self.diff_time = time.time() - self.start_time
        self.str_diff_time.set('time: ' + str(int(self.diff_time)))

    def finish(self):
        self.ticker.pause()

    def reset(self):
        self.str_diff_time.set('time: 0')
        self.start_time = time.time()
        self.ticker.resume()
        board.reset()

    def cleanup(self):
        self.ticker.waitForExit()

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
board = TileMap(map_size, map_size, mine_num, app)

app.master.title('Mines')
app.mainloop()
app.cleanup()
