import socket  
import tkinter as tk       
from shapes import Shape
from shapes import colors
import threading

##########################################

# IMPORTANT: message format is: "COMMAND|<shape_type>|<size>|<color>|<location>"
#Example: DRAW|"rectangle"|50|"black"|(150,150)

##########################################

class client:

    class clientDrawingBoard():

        DEFAULT_COLOR = 'black'
        DEFAULT_SIZE = 25
        COLUMN_NO = 5

        def __init__(self, client_instance):

            #saving out client stuff
            self.client_inst = client_instance
            #Root is our base window
            self.root = tk.Tk()
            self.root.title("Drawing Board Networking App: client side")

            #setting which client we are going to be using

            #create array to store shapes being "drawn" on canvas
            self.shapes = []
            self.active_button = None

            #build the canvas
            self.can = tk.Canvas(self.root, width=800, height=800, bg='beige')
            self.can.grid(row=1, columnspan = self.COLUMN_NO)

            #create buttons
            #rectangle
            self.rec_button = tk.Button(self.root, text='Rectangle.', command=self.build_rec)
            self.rec_button.grid(row=0, column=0)

            #circle
            self.circle_button = tk.Button(self.root, text='Circle.',command=self.build_circle)
            self.circle_button.grid(row=0, column=1)

            #initially activates the rectangle button
            self.active_button = self.rec_button
            self.activate_button(self.rec_button)

            #the stuff to make the color drop down work
            self.color_selected = tk.StringVar(self.root)
            self.color_selected.set("select color")
            self.color_drop = tk.OptionMenu(self.root, self.color_selected, *colors)
            self.color_drop.grid(row=0, column=2,padx=5,pady=5)

            #size slider stuff
            self.size_var = tk.DoubleVar()
            self.size_button = tk.Scale(self.root, from_=10, to=200, orient="horizontal", 
                                        label="shape size", variable=self.size_var)
            self.size_button.grid(row=0, column=3)

            #the close connection button
            self.close_button = tk.Button(self.root, text='close connection', command=client_instance.close_connection)
            self.close_button.grid(row=0, column=4)

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

        #bulk of the initiation work
        def setup(self):
            #binding events
            self.active_button = self.rec_button
            self.rec_button.bind("<Button-1>", self.build_rec)
            self.circle_button.bind("<Button-1>", self.build_circle)
            self.can.bind("<Button-1>", self.create_shape)

        #this is a bitch of a function and I hate it, can't get both the disabling and raising to work
        #they seem to be mutually exclusive
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

        #lil helper guys
        def build_rec(self,event=None):
            self.activate_button(self.rec_button)

        def build_circle(self,event=None):
            self.activate_button(self.circle_button)

        def build_shape(self, shape = Shape()):
            try:
                if shape.shapeType == "rectangle":
                    x0, y0 = shape.loc
                    x1, y1 = x0 + int(shape.size), y0 + int(shape.size)
                    self.can.create_rectangle(x0, y0, x1, y1, fill=shape.color, outline=shape.color)
                elif shape.shapeType == "circle":
                    x, y = shape.loc
                    r = int(shape.size)
                    self.can.create_oval(x - r, y - r, x + r, y + r, fill=shape.color, outline=shape.color)
                else:
                    print(f"Unsupported shape type: {shape.shapeType}")

                self.add_to_list(shape)

            except Exception as exc:
                print(f"Error: {exc} occurred while adding shape: {shape}")


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


    def __init__(self):
        #initial everything
        serverHost= "127.0.0.1"
        serverPort = 5050
        #server socket stuff
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((serverHost, serverPort))
        #creating our drawing board
        self.board = self.clientDrawingBoard(self)


    #function to start listening for new canvas updates
    def start_listening(self):
        try:

            #open up new threads that listen for server
            listening_thread = threading.Thread(target=self.recieve_shape_info)
            listening_thread.start()
        except Exception as ex:
            print(f"Error receiving info from server: {ex}")  

    #function to take in the recieved shape info
    def recieve_shape_info(self):
        try:
            while True:
                shape_info = self.client_socket.recv(1024).decode('utf-8')
                # Handle the received shape information (update canvas, etc.)
                self.handle_received_shape(shape_info)
        except Exception as ex:
            print(f"Error receiving info from server: {ex}")

    #this will split the incoming string message recieved into a shape object and return that object
    def handle_received_shape(self, shape_info):
        #command isn't used but it's required to decode the message
        command, shape_type, size, color, location = shape_info.split("|")
        to_add = self.board.Shape(shape_type, size, color, location)
        self.board.build_shape(to_add)

    #function to send the shape info to the server
    def send_shape_info(self, shape):
        try:
            message = f"DRAW|{shape.shapeType}|{shape.size}|{shape.color}|{shape.loc}"
            self.client_socket.send(message.encode('utf-8'))
        except Exception as exc:
            print(f'error: {exc}')

    #function to add the shape to the current canvas
    def add_shape(self, shape):
        self.board.create_shape(shape)
        self.send_shape_info(shape)

    def close_connection(self):
        try:
            self.client_socket.send("close".encode('utf-8'))
            self.client_socket.close()
            self.board.root.destroy()
        except Exception as exc:
            print(f"error: {exc} - occured during closing connection")

if __name__ == "__main__":
    cli = client()
    cli.start_listening()