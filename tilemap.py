import random
import tkMessageBox as tkmsg
from imagebank import *
import sys
sys.setrecursionlimit(10000)

class TileMap:
    def __init__(self, width, height, mine_num, app):
        self.w = width
        self.h = height
        self.app = app
        self.mine_num = mine_num
        self.flag_num = mine_num
        self.app.updateFlags(self.flag_num)

        self.tilenum = self.w * self.h
        self.tiles = [[0 for x in range(self.w)] for y in range(self.h)]

        for j in range(0, self.h):
            for i in range(0, self.w):
                self.tiles[j][i] = Tile(i, j, self, app.lframe)
        self.setBombs()
        return

    def setBombs(self):
        self.bombs = random.sample(range(0, self.w * self.h), self.mine_num)
        self.bombs.sort()
        self.bombs = [(b / self.w, b % self.w) for b in self.bombs]

        for b in self.bombs:
            y = b[0]
            x = b[1]
            self.tiles[y][x].changeType("bomb")
            # debug
            # self.tiles[b[1]][b[0]].show()

    def endGame(self):
        self.app.endGame(False)
        for b in self.bombs:
            y = b[0]
            x = b[1]
            self.tiles[y][x].show()
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
        if self.tilenum == self.mine_num:
            self.app.endGame(True)

    def decreaseFlags(self):
        self.flag_num -= 1
        self.app.updateFlags(self.flag_num)

    def increaseFlags(self):
        self.flag_num += 1
        self.app.updateFlags(self.flag_num)

    def getFlags(self):
        return self.flag_num

    def bombIsIn(self, x, y):
        return (x >= 0 and y >= 0 and x < self.w and y < self.h) and self.tiles[y][x].isBomb()

    def reset(self):
        self.flag_num = self.mine_num
        self.app.updateFlags(self.flag_num)
        self.tilenum = self.w * self.h

        for j in range(0, self.h):
            for i in range(0, self.w):
                self.tiles[j][i].reset()
        self.setBombs()


class Tile:
    def __init__(self, posX, posY, board, frame, t="normal"):
        self.disabled = False
        self.count = 0
        self.type = t
        self.flagged = False
        self.frame = frame
        self.board = board

        # Get graphics
        self.img = photoBank.getImage("normaltile")
        self.flagimg = photoBank.getImage("flag")
        self.disabledimg = photoBank.getImage("nothing")

        # Create the button
        self.button = tk.Button(self.frame, image=self.img, command=self.press)

        # Position the button on the grid
        self.x = posX
        self.y = posY
        self.button.grid(row=self.y, column=self.x)

        self.button.bind('<Button-3>', self.rightClick)

    def press(self):
        if not self.disabled and not self.flagged:
            if self.isBomb():
                self.disabledimg = photoBank.getImage("bombed")
                self.board.endGame()
            else:
                self.checkNearby()

            #self.button.config(state=tk.DISABLED)
            self.disable()
            self.button.config(image=self.disabledimg)

            if self.count == 0 and not self.isBomb():
                self.board.pressTile(self.x+1, self.y)
                self.board.pressTile(self.x+1, self.y+1)
                self.board.pressTile(self.x+1, self.y-1)
                self.board.pressTile(self.x, self.y)
                self.board.pressTile(self.x, self.y+1)
                self.board.pressTile(self.x, self.y-1)
                self.board.pressTile(self.x-1, self.y)
                self.board.pressTile(self.x-1, self.y+1)
                self.board.pressTile(self.x-1, self.y-1)
            if not self.isBomb():
                self.board.decreaseTiles()

    def rightClick(self, event):
        if not self.disabled:
            if self.flagged:
                self.board.increaseFlags()
                self.button.config(image=self.img)
                self.flagged = False
            elif self.board.getFlags() > 0:
                self.board.decreaseFlags()
                self.button.config(image=self.flagimg)
                self.flagged = True

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
                elif self.board.bombIsIn(self.x-1 + i, self.y-1 + j):
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
