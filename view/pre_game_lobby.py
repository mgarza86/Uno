import pygame
import pyghelpers
import pygwidgets
import socket
import threading
import sys
import queue
import json
from model.card_factory import CardFactory
from view.hand_view import HandView

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
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
        self.bg_color = BLACK
        self.client_hand = []
        self.hand_ready = False
        self.show_hand = None
        #self.window.fill((0, 0, 0))
        
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
        self.client_hand = self.create_cards_from_json(self.client_hand)        
        

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.play_button.handleEvent(event):
                self.bg_color = (0, 0, 255)
                
                if self.client:
                    try:
                        print("sending draw cards message to server")
                        self.client.send("draw_cards$".encode())
                    except Exception as e:
                        print(f"Error sending draw cards message: {e}")
                
    def draw(self):
        self.window.fill((self.bg_color))
        #print("Drawing scene, is_host:", self.is_host)
        if self.is_host:
            #self.notification.setValue("You are the host. Waiting for other players to join...")
            self.play_button.draw()
        self.notification.draw()
        if self.hand_ready:
            self.show_hand.draw()
    
    def connect(self):
        global client, HOST_ADDR, HOST_PORT
        
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST_ADDR, HOST_PORT))
            self.client.send(self.client_name.encode())  # Send name to server after connecting
            
            threading.Thread(target=self.receive_message_from_server, args=(self.client,), daemon=True).start()
        except Exception as e:
            print(f"Error connecting to server: {e}")
            
    def receive_message_from_server(self, sck):
        while True:
            from_server = sck.recv(4096).decode()
            
            if from_server.startswith("game_start$"):
                pyghelpers.goToScene('MultiplayerGameBoard')
            
            elif not from_server:
                break
            
            if from_server.startswith("hand$"):
                json_hand = from_server[5:]
                try:
                    hand_data = json.loads(json_hand)
                    #print(f"Received hand data: {hand_data}")

                    self.show_hand = HandView(self.window, hand_data)
                    self.hand_ready = True
                except json.JSONDecodeError as e:
                    print(f"Error decoding hand JSON: {e}")
                    continue
            
            if from_server.startswith("host_status$"):
                self.is_host = from_server.split("$")[1] == "yes"
                print(f"Received host status: {self.is_host}")
            else:
                self.message_queue.put(from_server)
                            
        sck.close()
        
        
    def create_cards_from_json(self, hand_data):
        cards = []
        for card_data in hand_data:
            card = CardFactory.create_card(self.window, card_data['card_type'], card_data['color'], card_data['value'])
            cards.append(card)
        return cards