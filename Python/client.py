import socket  
import tkinter as tk       
from shapes import drawingBoard
import threading


##########################################

# IMPORTANT: message format is: "COMMAND|<shape_type>|<size>|<color>|<location>"
#Example: DRAW|"rectangle"|"50 px"|"black"|(150,150)

##########################################


class client:

    class clientDrawingBoard(drawingBoard):

        def __init__(self, client):
            super().__init__()
            self.client = client

            self.close_button = tk.Button(self.root, text='close connecion',command=self.close_connection)
            self.close_button.grid(row=0, column=4)

        #creates the parent shape object, meant to be worked on top of
        def create_shape(self, event):
            super().create_shape(event)

    def __init__(self):

        #creating our drawing board
        self.board = self.clientDrawingBoard(self)  


        #initial everything
        serverHost= "127.0.0.1"
        serverPort = 5050
        #server socket stuff
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((serverHost, serverPort))


    #function to start listening for new canvas updates
    def start_listening(self):
        listener = threading.Thread(target=self.recieve_shape_info)
        listener.start()  

    #function to take in the recieved shape info
    def recieve_shape_info(self):
        try:
            while True:
                shape_info = self.client_socket.recv(1024).decode('utf-8')
                # Handle the received shape information (update canvas, etc.)
                self.handle_received_shape(shape_info)
        except Exception as ex:
            print(f"Error receiving info from server: {ex}")

    def handle_received_shape(self, shape_info):
        pass

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
        except Exception as exc:
            print(f"error: {exc} - occured during closing connection")

if __name__ == "__main__":
    cli = client()
    cli.start_listening()