import socket
import tkinter as tk
from shapes import shape





def clientHost():

    serverHost= "127.0.0.1"
    serverPort = 5050

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((serverHost, serverHost))
    client.sendData()
    





def sendData():
    pass



