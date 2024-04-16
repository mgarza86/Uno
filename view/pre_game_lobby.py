import pygame
import pyghelpers
import pygwidgets
import socket
import threading
import sys
import queue
import json
import logging
from model.card_factory import CardFactory
from view.hand_view import HandView
from view.view_opponent import ViewOpponent

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='app.log',  # Log to a file
                    filemode='w')  # Use 'a' to append; 'w' to overwrite each time

# Additional configuration for console logging
console_logger = logging.StreamHandler()
console_logger.setLevel(logging.ERROR)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_logger.setFormatter(console_formatter)
logging.getLogger('').addHandler(console_logger)

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
        
        self.show_hand = HandView(self.window, [])
        self.view_opponent = ViewOpponent(self.window)
        
        self.current_color = ""        
        self.current_value = ""
        
        self.current_player = None
        self.current_player_banner = pygwidgets.DisplayText(self.window, (100, 100), 
                                                            f"Current Player: {self.current_player}", 
                                                            fontSize=20, textColor=(255, 255, 255), width=600, justified='center')
        self.is_current_player = False
        self.notify_client = pygwidgets.DisplayText(self.window, (400, 200), "It's your turn.", fontSize=20, textColor=(255, 255, 255), width=100, justified='center')
        self.alert_player = False 

    def enter(self, data):
        self.client_name = data.get("player_name")
        self.client_id = data.get("client_id")
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
                # Handle host status 
                print(self.is_host)
                self.is_host = message.split("$")[1] == "yes"
            elif message.startswith("current_player$"):
                try:
                    data = message.split("$")[1]
                    # logging.debug(f"Current player data: {data}")
                    current_player = json.loads(data)
                    #print(current_player.client_id, self.client_id)
                    if current_player['client_id'] == self.client_id:
                        print("Current player is me")
                        self.is_current_player = True
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding current player JSON: {e}")
            
                    
        self.client_hand = self.create_cards_from_json(self.client_hand)
        
        # if self.is_current_player:
        #     self.alert_player = True
            
    def handleInputs(self, events, keyPressedList):
        
        for event in events:
            if self.play_button.handleEvent(event):
                self.bg_color = (0, 0, 255)
                if self.client:
                    try:
                        print("sending $start_game message to server")
                        self.client.send("start_game$".encode())
                    except Exception as e:
                        print(f"Error sending draw cards message: {e}")
            if self.is_current_player:
                for card in self.show_hand.cards:
                    if card.handle_event(event):
                        if self.check_conditions(card, self.current_color, self.current_value):
                            print("sending play card message to server")
                            self.client.send(f"play_card${card.to_json()}".encode())
                        
                        
                        
                        print(f"Card clicked: {card.get_name()}")
                        # try:
                        #     self.client.send(f"play_card${card.to_json()}".encode())
                        # except Exception as e:
                        #     print(f"Error sending play card message: {e}")
                        

            #current_player = self.game.players_list[self.game.current_player_index]
            
                
    def draw(self):
        self.window.fill((self.bg_color))
        #print("Drawing scene, is_host:", self.is_host)
        if self.is_host:
            self.play_button.draw()
        self.notification.draw()
        #self.current_player_banner.draw()
        self.view_opponent.draw()
        if self.is_current_player:
            self.notify_client.draw()
        if self.hand_ready:
            self.show_hand.draw()
    
    def connect(self):
        global client, HOST_ADDR, HOST_PORT
        
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST_ADDR, HOST_PORT))
            self.client.send(f"NAME:{self.client_name};".encode())  # Send name to server after connecting
            self.client.send(f"ID:{self.client_id};".encode())  # Send client ID to server after connecting
            
            
            threading.Thread(target=self.receive_message_from_server, args=(self.client,), daemon=True).start()
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def receive_message_from_server(self, sck):
        buffer = ""
        while True:
            try:
                data_received = sck.recv(4096).decode()
                if not data_received:  # Check for an empty string, which indicates a closed connection
                    break
                buffer += data_received
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    # logging.debug(f"Received message: {message}")
                    self.process_message(message)
                # logging.debug(f"Received message: {message}")
            except socket.error as e:
                logging.error(f"Error receiving message from server: {e}")
                break
            except Exception as e:
                logging.error(f"Unhandled error: {e}")
                break
                                
        sck.close()

    def process_message(self, message):
        if message.startswith("hand$"):
            json_hand = message[5:]
            try:
                hand_data = json.loads(json_hand)
                #logging.debug(f"Received hand data: {hand_data}")
                #! I think i need to create the object in the init and only update the hand data here
                self.show_hand.update(hand_data)
                self.hand_ready = True
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding hand JSON: {e}")
        elif message.startswith("opponent_cards_count$"):
            try:
                opponent_data = message.split("$")[1]
                #logging.debug(f"Received opponent data: {opponent_data}")
                self.view_opponent.update_opponent(opponent_data)
            except Exception as e:
                logging.error(f"Error updating opponent data: {e}")    
        elif message.startswith("host_status$"):
            self.is_host = message.split("$")[1] == "yes"
            #logging.debug(f"Host status: {self.is_host}")
        elif message.startswith("game_conditions$"):
            self.current_color, self.current_value = message.split("$")[1].split(",")
        else:
            self.message_queue.put(message)
  
  
    def create_cards_from_json(self, hand_data):
        cards = []
        for card_data in hand_data:
            card = CardFactory.create_card(self.window, card_data['card_type'], card_data['color'], card_data['value'])
            cards.append(card)
        return cards
    
    def check_conditions(self, card, color, value):
        if color == "":
            return True
        elif color == "black":
            return True
        elif card.get_color() == "black":
            return True
        elif card.get_color() == color:  
            return True
        elif card.get_value() == value: 
            return True
        return False
