import pygame
import pyghelpers
import pygwidgets
import socket
import threading
import sys
import queue


HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080

class PreGameLobby(pyghelpers.Scene):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.client = None
        self.message_queue = queue.Queue()
        self.play_button = pygwidgets.TextButton(window, (100, 200), "Play", width=100, height=50)
        self.is_host = False
        
    def enter(self, data):
        self.client_name = data.get("player_name")
        self.lobby_name = data.get("lobby_name")
        self.notification = pygwidgets.DisplayText(self.window, (100, 80), f"{self.client_name} has joined. Waiting for other players to join...", fontSize=20, textColor=(255, 255, 255), width=600, justified='center')
        self.connect()
     
    def update(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()

            if message.startswith("client_list$"):
                # Existing logic to handle client list updates
                client_names = message.split("$")[1]
                client_list = client_names.split(",")  # Parse the list of client names
                client_list_str = "\n".join(client_list)
                display_message = f"**********Client List**********\n{client_list_str}"
                self.notification.setValue(display_message)
            elif message.startswith("host_status$"):
                # Handle host status message
                self.is_host = message.split("$")[1] == "yes"

        
    def handleInputs(self, events, keyPressedList):
        for event in events:
            pass
        
    def draw(self):
        self.window.fill((0, 0, 0))
        print("Drawing scene, is_host:", self.is_host)
        if self.is_host:
            #self.notification.setValue("You are the host. Waiting for other players to join...")
            self.play_button.draw()
        self.notification.draw()
    
    def connect(self):
        global client, HOST_ADDR, HOST_PORT
        
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST_ADDR, HOST_PORT))
            client.send(self.client_name.encode())  # Send name to server after connecting
            
            threading.Thread(target=self.receive_message_from_server, args=(client,), daemon=True).start()
        except Exception as e:
            print(f"Error connecting to server: {e}")
            
    def receive_message_from_server(self, sck):
        while True:
            from_server = sck.recv(4096).decode()
            
            if not from_server:
                break
            if from_server.startswith("host_status$"):
                self.is_host = from_server.split("$")[1] == "yes"
                print(f"Received host status: {self.is_host}")
            else:
                self.message_queue.put(from_server)
                            
        sck.close()
        