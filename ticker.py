import threading as th

class Ticker:
    def __init__(self, freq, func):
        self.freq = freq
        self.func = func

        self.t = th.Timer(self.freq, self.updateTime)
        self.t.start()
        self.ticking = True

    def waitForExit(self):
        self.ticking = False
        self.t.join()

    def updateTime(self):
        if self.ticking:
            self.func()
            self.t = th.Timer(self.freq, self.updateTime)
            self.t.start()

    def pause(self):
        self.ticking = False

    def resume(self):
        self.ticking = True
        self.t = th.Timer(self.freq, self.updateTime)
        self.t.start()
