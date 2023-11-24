import tkinter as tk

colors = [
    'black',
    'blue',
    'green',
    'red',
    'pink',
    'orange',
    'purple',
    'yellow',
    'white'
]

class Shape:

    def __init__(self, shape="circle",size="50 px",color="black",location=(150,150) ):
        self.shapeType = shape
        self.size = size
        self.color = color
        self.loc = location

    def __str__(self):
        return f'{self.shapeType},{self.size},{self.color},{self.loc}'
        

class drawingBoard:

    DEFAULT_COLOR = 'black'
    DEFAULT_SIZE = 25
    COLUMN_NO = 4

    def __init__(self):

        #Root is our base window
        self.root = tk.Tk()
        self.root.title("Drawing Board Networking App")
        #create array to store shapes being "drawn" on canvas
        self.shapes = []
        self.active_button = None   #added this initialization for active_button(IJ)
        #build the canvas
        self.can = tk.Canvas(self.root, width=800, height=800, bg='beige')
        self.can.grid(row=1, columnspan = self.COLUMN_NO)

        #create buttons
        #rectangle
        
        #added an initial button relief state of sunken for both rect and circle button
        self.rec_button = tk.Button(self.root, text='Rectangle.', command=self.build_rec)
        self.rec_button.grid(row=0, column=0)

        #circle
        self.circle_button = tk.Button(self.root, text='Circle.',command=self.build_circle)
        self.circle_button.grid(row=0, column=1)

        self.active_button = self.rec_button
        self.activate_button(self.rec_button)

        #the stuff to make the color drop down work
        self.color_selected = tk.StringVar(self.root)
        self.color_selected.set("select color")
        self.color_drop = tk.OptionMenu(self.root, self.color_selected, *colors)
        self.color_drop.grid(row=0, column=2,padx=5,pady=5)

        #size button stuff
        self.size_var = tk.DoubleVar()
        self.size_button = tk.Scale(self.root, from_=10, to=200, orient="horizontal", 
                                    label="shape size", variable=self.size_var)
        self.size_button.grid(row=0, column=3)
        

        #setup and loop stuff
        self.setup()
        self.root.mainloop()


    def create_shape(self, event):
       
       #temporary til we allow user to change size and color
        size = self.size_var.get()
        color = self.color_selected.get()

        if color == "select color":
            color = self.DEFAULT_COLOR


        #create square stuff
        if self.active_button == self.rec_button:
            x0, y0 = event.x, event.y
            x1, y1 = x0 + int(size), y0 + int(size)
            self.can.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)
            new_shape = Shape("rectangle", size, color, (x0,y0))
            self.add_to_list(new_shape)

        #create circle stuff
        elif self.active_button == self.circle_button:
            x, y, r = event.x, event.y, int(size)
            self.can.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)
            new_shape = Shape("circle", size, color, (int(x), int(y)))
            self.add_to_list(new_shape)

    def setup(self):
        #binding events
        self.active_button = self.rec_button
        self.rec_button.bind("<Button-1>", self.build_rec)
        self.circle_button.bind("<Button-1>", self.build_circle)
        self.can.bind("<Button-1>", self.create_shape)


    
    def activate_button(self, clicked_button):
        if self.active_button == clicked_button:
            current_relief = self.active_button.cget("relief")
            new_relief = tk.RAISED if current_relief == tk.SUNKEN else tk.SUNKEN
            self.active_button.config(relief=new_relief)
            self.active_button = None if new_relief == tk.RAISED else clicked_button
        else:
            if self.active_button:
                self.active_button.config(relief=tk.RAISED)
            clicked_button.config(relief=tk.SUNKEN)
            self.active_button = None if self.active_button == self.circle_button else clicked_button




    def build_rec(self,event=None):
        self.activate_button(self.rec_button)

    def build_circle(self,event=None):
        self.activate_button(self.circle_button)

    def add_to_list(self, shape=Shape()):
        self.shapes.append(shape)

    def print_list(self):
        for shape in self.shapes:
            print(shape)

    def build_from_list(self, list = []):
        for shape in list:
            try:
                match shape.shapeType:
                    case "rectangle":
                        self.can.create_rectangle(shape.location[0], shape.location[0] + int(shape.size), 
                                                shape.location[0], 
                                                shape.location[0] + int(shape.size), 
                                                color=shape.color, outline=shape.color)
                        self.add_to_list(shape)

                    case "circle":
                        #big ass chunk of code to create a damn circle
                        self.can.create_oval(shape.location[0] - int(shape.size), 
                                             shape.location[1] - int(shape.size), 
                                             shape.location[0] + int(shape.size), 
                                             shape.location[1] + int(shape.size),
                                             fill=shape.color, outline=shape.color)
                        self.add_to_list(shape)

                    case _:
                        print("improper shape type during import")

            except Exception as ex:
                print(f'error: {ex}')

            self.add_to_list(shape)


if __name__ == "__main__":
    drawingBoard()