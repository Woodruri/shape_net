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


    def __init__(self):

        #list of clients connected to server
        self.client_list = []
        self.shapes = []
        #self.board = self.serverDrawingBoard(self)

    def handle_received_shape(self, shape_info):
        print(shape_info)
        command, shape_type, size, color, location = shape_info.split("|")
        to_add = Shape(shape_type, size, color, location)
        self.add_to_list(to_add)

    def add_to_list(self, shape=Shape()):
        self.shapes.append(shape)
        print(f"shape: {shape} added to list")

    #basic function to send some "message" to all clients connected to the server
    def broadcast_message(self, message):
        print(f"broadcasting the message: {message}")
        for client in self.client_list:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error: {e} - while sending message to client: {client}")

    #how we handle the recieved client stuff
    def handle_client(self, client, address):
        print(f"inside handle_client func in server - Client: {client}, address: {address}")
        try:
            while True:

                #recieve the message
                client_message = client.recv(1024).decode('utf-8')
                print(client_message)

                #check if the client wants to close connection
                if client_message.lower() == "close":
                    client.send(("Disconnected from server").encode('utf-8'))
                    break

                #prints message (for now, it will be shapes later)
                #print(f"recieved message from {client} at address {address}: {client_message}")
                self.broadcast_message(client_message)

                '''#splits the incoming message into all fields seperated by a "|"
                command, *data = client_message.split("|")
                
                #drawing command AKA adding a shape to the canvas
                if command == "DRAW":
                    shape_info = "|".join(data)
                    self.broadcast_message(client_message)

                    #handle the recieved shape from the client and draw it
                    self.handle_received_shape(shape_info)'''

                #leaving this open for future commands that we want to add
                
                '''#response = "accepted"
                response = " message recieved"
                client.send(response.encode('utf-8'))'''

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