import tkinter
import tkinter.messagebox

from tkinter import *

root = Tk()

cv = Canvas(root, bg='white')
cv.create_oval(10, 10, 100, 100, fill='red')
cv.pack()
root.mainloop()