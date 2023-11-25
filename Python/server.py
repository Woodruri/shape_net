import socket
import threading
import tkinter as tk
from shapes import drawingBoard


##########################################

# IMPORTANT: message format is: "COMMAND|<shape_type>|<size>|<color>|<location>"
#Example: DRAW|"rectangle"|"50 px"|"black"|(150,150)

##########################################

class server:

    class serverDrawingBoard(drawingBoard):
        def __init__(self):
            super().__init__()
            #drop down to disconnect clients
            self.client_to_rem = tk.StringVar(self.root)
            self.client_to_rem.set("select client to remove")
            self.client_drop = tk.OptionMenu(self.root, self.client_to_rem, *server.client_list)
            self.client_drop.grid(row=0, column=4)


    def __init__(self):
        #list of clients connected to server
        self.client_list = []
        self.board = drawingBoard()

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







