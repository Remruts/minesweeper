import Tkinter as tk
from PIL import Image, ImageTk

class ImageBank:
    def __init__(self):
        self.images = {}
        return

    def getImage(self, name):
        if name in self.images:
            return self.images[name]
        else:
            #print "Failed to fetch " + name
            return None

    def loadImage(self, name, filename):
        if name not in self.images:
            #print "Loading " + filename + "..."
            photo = ImageTk.PhotoImage(Image.open(filename))

            if photo != None:
                self.images[name] = photo
                #print "Loaded " + filename + " as " + name
            else:
                print "Failed to load " + filename
        return self.images[name]

    def freeImage(self, name):
        if name in self.images:
            del self.images[name]

photoBank = ImageBank()
