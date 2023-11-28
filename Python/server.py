import socket
import threading
import tkinter as tk
from shapes import Shape
from shapes import colors


##########################################

# IMPORTANT: message format is: "COMMAND|<shape_type>|<size>|<color>|<location>"
#Example: DRAW|"rectangle"|50|"black"|(150,150)

##########################################

class server:

    class serverDrawingBoard():

        DEFAULT_COLOR = 'black'
        DEFAULT_SIZE = 25
        COLUMN_NO = 5

        def __init__(self, server_instance):

            self.server_inst = server_instance
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

            #size slider stuff
            self.size_var = tk.DoubleVar()
            self.size_button = tk.Scale(self.root, from_=10, to=200, orient="horizontal", 
                                        label="shape size", variable=self.size_var)
            self.size_button.grid(row=0, column=3)

            #drop down to disconnect clients
            self.client_to_rem = tk.StringVar(self.root)
            self.client_to_rem.set("select client to remove")
            self.client_drop = tk.OptionMenu(self.root, self.client_to_rem, *self.server_inst.client_list, value="remove")
            self.client_drop.grid(row=0, column=4)

            #setup and loop stuff
            self.setup()
            self.root.mainloop()

        def handle_received_shape(self, shape_info):
            command, shape_type, size, color, location = shape_info.split("|")

            to_add = self.Shape(shape_type, size, color, location)
            self.build_shape(to_add)

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
                new_shape = self.Shape("rectangle", size, color, (x0,y0))
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

        #list of clients connected to server
        self.client_list = []
        #self.board = self.serverDrawingBoard(self)

    def handle_received_shape(self, shape_info):
        command, shape_type, size, color, location = shape_info.split("|")
        to_add = Shape(shape_type, size, color, location)
        self.build_shape(to_add)

    #basic function to send some "message" to all clients connected to the server
    def broadcast_message(self, message):
        for client in self.client_list:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error: {e} - while sending message to client:client_list {client}")

    #how we handle the recieved client stuff
    def handle_client(self, client, address):
        try:
            while True:

                #recieve the message
                client_message = client.recv(1024).decode('utf-8')

                #check if the client wants to close connection
                if client_message.lower() == "close":
                    client.send(("Disconnected from server").encode('utf-8'))
                    break

                #prints message (for now, it will be shapes later)
                print(f"recieved message from {client} at address {address}: {client_message}")

                #splits the incoming message into all fields seperated by a "|"
                command, *data = client_message.split("|")
                
                #drawing command AKA adding a shape to the canvas
                if command == "DRAW":
                    shape_info = "|".join(data)
                    self.broadcast_message(f"{address}: {shape_info}")

                    #handle the recieved shape from the client and draw it
                    self.board.handle_received_shape(shape_info)

                #leaving this open for future commands that we want to add
                
                #response = "accepted"
                response = "message recieved"
                client.send(response.encode('utf-8'))

        except Exception as exc:
            print(f"Error occured: {exc}")
        
        finally:
            client.close()
            self.client_list.remove(client)
            print(f"Connection to {address} was closed")


    #function to create server instance and start running
    def start(self):
        host_ip = ''
        port = 5050

        try:
            #create socket object
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((host_ip, port))

            #set up server to listen for incoming client connections
            server.listen()
            print(f"Host IP: {host_ip} listening on Port: {port}")

            while True:
                client, address = server.accept()
                print(f"Client connected from {address[0]} at {address[1]}")

                self.client_list.append(client)

                thread = threading.Thread(target=self.handle_client, args=(client, address,))
                thread.start()

        except Exception as ex:
            print(f"Error: {ex}")
        finally:
            server.close()


if __name__ == "__main__":

    serv = server()
    serv.start()