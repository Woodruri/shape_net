import socket
import threading

import tkinter as tk
from shapes import shape


#list of clients connected to server
client_list = []

#basic function to send some "message" to all clients connected to the server
def broadcast_message(message):
    for client in client_list:
        client.send(message)

def handle_client(client, address):
    try:
        while True:
            client_message = client.recv(1024) #might need to include decode?

            if client_message.lower() == "close":
                client.send("Disconnected from server")
                break
            print(f"{client_message} recieved")

            #response = "accepted"
            client.send("accepted")

    except Exception as exc:
        print(f"Error occured: {exc}")
    
    finally:
        client.close()
        print(f"Connection to {address[1]} was closed")


#function to create server instance and start running
def server():
    host_ip = '127.0.0.1' 
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

            client_list.append(client)

            thread = threading.Thread(target=handle_client, args=(client, address,))
            thread.start()

    except Exception as ex:
        print(f"Error: {ex}")
    finally:
        server.close()


server()







