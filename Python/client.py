import socket
import tkinter as tk
from shapes import drawingBoard


class client:
    def client_host():

        #initial everything
        serverHost= "127.0.0.1"
        serverPort = 5050


        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((serverHost, serverHost))

        board = drawingBoard()

        

    def send_shape_info():
        pass



if __name__ == "__main__":
    client_host()