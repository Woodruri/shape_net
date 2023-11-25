import socket         
from shapes import drawingBoard
import threading


##########################################

# IMPORTANT: message format is: "COMMAND|<shape_type>|<size>|<color>|<location>"
#Example: DRAW|"rectangle"|"50 px"|"black"|(150,150)

##########################################

class clientDrawingBoard(drawingBoard):

    def __init__(self):
        super().__init__()

    def format_shape_msg(self, shape_info):
        #splits the incoming message into all fields seperated by a "|"
        command, *data = shape_info.split("|")


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
            new_shape = self.shape("rectangle", size, color, (x0,y0))

        #create circle stuff
        elif self.active_button == self.circle_button:
            x, y, r = event.x, event.y, int(size)
            self.can.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)
            new_shape = self.Shape("circle", size, color, (int(x), int(y)))

        self.add_to_list(new_shape)
        self.format_and_send(new_shape)


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
        try:
            message = f"DRAW|{shape.shapeType}|{shape.size}|{shape.color}|{shape.loc}"
            self.client_socket.send(message.encode('utf-8'))
        except Exception as exc:
            print(f'error: {exc}')

    #function to add the shape to the current canvas
    def add_shape(self, shape):
        self.board.create_shape(shape)
        self.send_shape_info(shape)

if __name__ == "__main__":
    cli = client()