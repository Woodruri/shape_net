import socket         
from shapes import drawingBoard
import threading


class client:

    def __init__(self):

        #creating our drawing board
        self.board = drawingBoard(self) 


        #initial everything
        serverHost= "127.0.0.1"
        serverPort = 5050
        #server socket stuff
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((serverHost, serverHost))


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
        message = f"DRAW|{shape.shapeType}|{shape.size}|{shape.color}|{shape.loc}"
        self.client_socket.send(message.encode('utf-8'))

    #function to add the shape to the current canvas
    def add_shape(self, shape):
        self.board.create_shape(shape)
        self.send_shape_info(shape)

if __name__ == "__main__":
    cli = client()