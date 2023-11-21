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

    DEFAULT_COLOR = 'black'
    DEFAULT_SIZE = 25
    COLUMN_NO = 4

    def __init__(self):

        #Root is our base window
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
        self.size_button = tk.Entry(self.root, text='Size.')
        self.size_button.grid(row=0, column=2)

        #color
        self.color_button = tk.Entry(self.root, text='Color.')
        self.color_button.grid(row=0, column=3)

        #build the canvas
        self.can = tk.Canvas(self.root, width=800, height=800, bg='white')
        self.can.grid(row=0, column = self.COLUMN_NO)

        self.setup()
        self.root.mainloop()

        #our temp shape var to create current shapes
        temp = shape()


    def createShape(self, shape):
        pass

    def addToJSON(self, shape):
        pass

    def build_rec(self):
        pass

    def build_circle(self):
        pass

    def pick_size(self):
        pass
    
    def setup(self):
        #binding events
        self.can.bind('<Button-1>', self.createShape)
        pass


if __name__ == "__main__":
    drawingBoard()