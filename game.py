#!/usr/bin/env python
import Tkinter as tk
from PIL import Image, ImageTk
from imagebank import *
from ticker import *
from tilemap import *
import time
import os.path

class Game(tk.Frame):
    def __init__(self, app=None):
        tk.Frame.__init__(self, app)
        self.app = app
        self.difficulty = app.difficulty

        self.loadGraphics()

        self.ticker = Ticker(1, self.update)
        self.ticker.stop()

        self.str_diff_time = tk.StringVar()
        self.str_flag = tk.StringVar()
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

    def start(self):
        self.grid()
        self.start_time = time.time()
        self.diff_time = self.start_time - time.time()
        self.str_diff_time.set('000')
        self.ticker.start()

        self.str_flag.set('000')

        self.board = TileMap(self.app.map_width, self.app.map_height, self.app.mine_num, self)

        #self.resetButton.grid(row=0, column=self.app.map_width/2, sticky=tk.W)
        #self.clock_label.grid(row=0, column=self.app.map_width-2, sticky=tk.E)

    def reset(self):
        self.str_diff_time.set('000')
        self.start_time = time.time()
        self.ticker.start()
        self.board.reset()

    def updateFlags(self, num):
        stnum = str(min(num, 999))
        while len(stnum) < 3:
            stnum = '0' + stnum
        self.str_flag.set(stnum)
        return

    def update(self):
        self.diff_time = time.time() - self.start_time
        stdiff = str(min(int(self.diff_time), 999))
        while len(stdiff) < 3:
            stdiff = '0' + stdiff
        self.str_diff_time.set(stdiff)

    def finish(self):
        self.ticker.stop()

    def endGame(self):
        self.finish()
        self.diff_time = time.time() - self.start_time

        self.readSaveFile("beginnersfilemeh")

        txt = "Time: " + "%.2f" % (self.diff_time, ) + "      \n\n"
        if self.difficulty != "Custom":
            txt += "Highscore:\n"
            scores = self.readSaveFile(self.difficulty+"Savefile")
            for s in scores:
                txt += "  " + s + "\n"

        msg = tkmsg.showinfo("You Win! :)", txt)
        self.reset()

    def readSaveFile(self, filename):
        formatted_time = "%.2f" % (self.diff_time, )
        scores = []
        # Nothing fancy
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                scores = f.readlines()
                scores = [float(x) for x in scores]
                scores.append(self.diff_time)
                scores.sort()
                scores = scores[:-1]
        else:
            scores.append(self.diff_time)
            scores.append(999.99)
            scores.append(999.99)

        scores = [("%.2f" % (x, )).zfill(6) for x in scores]
        f = open(filename, "w")
        for s in scores:
            f.write(s+"\n")
        f.close()

        return scores


    def createWidgets(self):
        #self.menu = Menu(self)

        self.resetButton = tk.Button(self, text='Reset', command=self.reset)
        self.resetButton.grid(row=0, column=self.app.map_width/2, sticky=tk.W)

        self.lframe = tk.LabelFrame(self)
        self.lframe.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W+tk.E, columnspan=self.app.map_width)

        self.clock_label = tk.Label(self, textvariable=self.str_diff_time)
        self.clock_label.grid(row=0, column=self.app.map_width-2, sticky=tk.E)

        self.flag_label = tk.Label(self, textvariable=self.str_flag)
        self.flag_label.grid(row=0, column=1, sticky=tk.W)
