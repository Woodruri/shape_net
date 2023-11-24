import tkinter as tk


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

        #size and color featured have been implemeted yet

        #create a combo drop down for shape sizes in case we can get it to work as entry option 
        '''
        self.label = tk.Label(self.root, text='Size:')
        self.grid(row=0, column=2, padx=5, pady=5)
        '''
        self.size_button = tk.Entry(self.root)
        self.size_button.grid(row=0, column=2,padx=5,pady=5)
        self.size_button = tk.Entry(self.root, text='Size.')
        self.size_button.grid(row=0, column=2)
        

        #color
        
        self.color_button = tk.Entry(self.root, text='Color.')
        self.color_button.grid(row=0, column=3)  

        #setup and loop stuff
        self.setup()
        self.root.mainloop()


    def create_shape(self, event):
       
        size = self.DEFAULT_SIZE
        color = self.DEFAULT_COLOR


        if self.active_button == self.rec_button:
            x0, y0 = event.x, event.y
            x1, y1 = x0 + int(size), y0 + int(size)
            self.can.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)
            new_shape = Shape("rectangle", size="50px", color="black", location=(x0,y0))
            self.addToJSON(new_shape)
        elif self.active_button == self.circle_button:
            x, y, r = event.x, event.y, int(size)
            self.can.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)
            new_shape = Shape("circle", size="50px", color="black", location=(x, y))
            self.addToJSON(new_shape)

    def setup(self):
        #binding events
        self.active_button = self.rec_button
        self.rec_button.bind("<Button-1>", self.build_rec)
        self.circle_button.bind("<Button-1>", self.build_circle)
        self.can.bind("<Button-1>", self.create_shape)


    
    def activate_button(self, clicked_button):

        '''if self.active_button:
            self.active_button.config(relief=tk.RAISED)
        new_button.config(relief=tk.SUNKEN)
        self.active_button = new_button
        '''
        #rewrote to be able to togle between buttons(IJ)
        if self.active_button == clicked_button:
            current_relief = self.active_button.cget("relief")
            new_relief = tk.RAISED if current_relief == tk.SUNKEN else tk.SUNKEN
            self.active_button.config(relief= new_relief)
        else:
            if self.active_button:
                self.active_button.config(relief=tk.RAISED)
            clicked_button.config(relief=tk.SUNKEN)
            self.active_button = clicked_button

    def build_rec(self,event=None):
        self.activate_button(self.rec_button)

    def build_circle(self,event=None):
        self.activate_button(self.circle_button)

    def pick_size(self):
        pass
    
        


    #setup and loop stuff
        self.setup()
        self.root.mainloop()


if __name__ == "__main__":
    drawingBoard()