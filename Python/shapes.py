import tkinter as tk
import json as js

class shape:

    def __init__(self, shape="circle",size="50 px",color="black",location=(150,150) ):
        self.shape = shape
        self.size = size
        self.color = color
        self.loc = location

    def __str__(self):
        return f'{self.shape},{self.size},{self.color},{self.loc}'



class drawingBoard:

    DEFAULT_COLOR = 'black'
    DEFAULT_SIZE = 25
    COLUMN_NO = 4

    def __init__(self):

        #Root is our base window
        self.root = tk.Tk()
        self.root.title("Drawing Board Networking App")

        #create buttons
        #rectangle
        
        self.rec_button = tk.Button(self.root, text='Rect.', command=self.build_rec)
        self.rec_button.grid(row=0, column=0)

        #circle
        self.circle_button = tk.Button(self.root, text='Circle.', command=self.build_circle)
        self.circle_button.grid(row=0, column=1)

        self.active_button = self.rec_button
        self.activate_button(self.rec_button)

        #size
        self.size_button = tk.Entry(self.root, text='Size.')
        self.size_button.grid(row=0, column=2)

        #color
        self.color_button = tk.Entry(self.root, text='Color.')
        self.color_button.grid(row=0, column=3)

        #build the canvas
        self.can = tk.Canvas(self.root, width=800, height=800, bg='white')
        self.can.grid(row=1, columnspan = self.COLUMN_NO)

        #setup and loop stuff
        self.setup()
        self.root.mainloop()

        #our temp shape var to create current shapes
        temp = shape()


    def createShape(self, event):
        """
        size = self.size_button.get()
        color = self.color_button.get()
        """
        size = self.DEFAULT_SIZE
        color = self.DEFAULT_COLOR


        if self.active_button == self.rec_button:
            x0, y0 = event.x, event.y
            x1, y1 = x0 + int(size), y0 + int(size)
            self.can.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)
        elif self.active_button == self.circle_button:
            x, y, r = event.x, event.y, int(size)
            self.can.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)
        
        self.addToJSON()

    def addToJSON(self):
        pass
        #needs to be able to add each shape to the JSON file

    def build_rec(self):
        self.activate_button(self.rec_button)

    def build_circle(self):
        self.activate_button(self.circle_button)

    def pick_size(self):
        pass
    
    def setup(self):
        #binding events
        self.active_button = self.rec_button
        self.rec_button.bind("<Button-1>", self.build_rec())
        self.circle_button.bind("<Button-1>", self.build_circle())
        self.can.bind("<Button-1>", self.createShape)

    def activate_button(self, some_button):
        self.active_button.config(relief=tk.RAISED)
        some_button.config(relief=tk.SUNKEN)
        self.active_button = some_button


if __name__ == "__main__":
    drawingBoard()