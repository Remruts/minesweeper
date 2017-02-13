import threading as th

class Ticker:
    def __init__(self, frequency, function):
        self.freq = frequency
        self.func = function

        self.timer = None
        self.ticking = False
        self.start()

    def start(self):
        if not self.ticking:
            self.timer = th.Timer(self.freq, self.run)
            self.timer.start()
            self.ticking = True

    def run(self):
        self.ticking = False
        self.start()
        self.func()

    def stop(self):
        self.timer.cancel()
        self.ticking = False
