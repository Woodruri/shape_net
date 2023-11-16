import tkinter as tk

class shape:

    def __init__(self, shape="circle",size="50 px",color="black",location=(150,150) ):
        self.shape = shape
        self.size = size
        self.color = color
        self.loc = location

    def __str__(self):
        return f'{self.shape},{self.size},{self.color},{self.loc}'



class drawingBoard:
    def __init__(self,root):
        self.root = tk.Tk()
        self.root.title = "Drawing Board Networking App"

        #create buttons
        #rectangle
        self.rec_button = tk.Button(self.root, text='Rect.', command=self.build_rec)
        self.rec_button.grid(row=0, column=0)

        #circle
        self.circle_button = tk.Button(self.root, text='Circle.', command=self.build_circle)
        self.circle_button.grid(row=0, column=1)

        #size
        self.size_button = tk.Entry(self.root, text='Size.', command=self.pick_size)
        self.size_button.grid(row=0, column=2)

        #color
        self.color_button = tk.Entry(self.root, text='Color.')
        self.color_button.grid(row=0, column=3)

        #build the canvas
        self.canvas = tk.Canvas(root, width=800, height=800, bg='white')
        self.canvas.pack()

        #our temp shape var to create current shapes
        temp = shape()

        #binding events
        self.canvas.bind('<Button-1>', self.createShape)

    def createShape(self, shape):
        pass

    def addToJSON(self, shape):
        pass


if __name__ == "__main__":
    drawingBoard(tk.Tk())