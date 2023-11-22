import socket
import tkinter as tk
from shapes import shape
import json as js

host = "127.0.0.1"
port = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))



def recieve():
    while True:
        try:
            message = client.recv(1024)
        
        except:
            pass