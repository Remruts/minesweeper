#!/usr/bin/env python
import Tkinter as tk
from PIL import Image, ImageTk

class Application(tk.Frame):
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.grid()
    self.createWidgets()

  def createWidgets(self):
    self.quitButton = tk.Button(self, text='Quit', command=self.quit)
    self.quitButton.grid()

    img = Image.open("smiley.png")
    photo = ImageTk.PhotoImage(img)
    self.label = tk.Button(image=photo)
    self.label.image = photo
    self.label.grid()

app = Application()
app.master.title('Sample application')
app.mainloop()
