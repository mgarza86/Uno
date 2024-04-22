import pygame
import pyghelpers
import pygwidgets
import socket
import threading
import sys
import queue
import json
import time
import logging
from model.card_factory import CardFactory
from model.card import *
from view.hand_view import HandView
from view.view_opponent import ViewOpponent
from view.view_discard import ViewDiscard

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
    def __init__(self, window, settings):
        super().__init__()
        self.window = window
        self.settings = settings
        self.client = None
        self.message_queue = queue.Queue()
        self.play_button = pygwidgets.TextButton(window, (100, 200), "Play", width=100, height=50)
        self.is_host = False
        self.bg_color = BLACK
        self.client_hand = []
        self.hand_ready = False
        self.discard_pile = []
        
        self.show_hand = HandView(self.window, [])
        self.view_opponent = ViewOpponent(self.window)
        
        self.current_color = ""        
        self.current_value = ""
        self.game_started = False
        
        self.winner = None
        self.winner_banner = pygwidgets.DisplayText(self.window, (100, 200), f"Winner: {self.winner}", fontSize=30, textColor=(0, 0, 0), width=600, justified='center')
        
        self.current_player = None
        self.current_player_banner = pygwidgets.DisplayText(self.window, (100, 100), 
                                                            f"Current Player: {self.current_player}", 
                                                            fontSize=20, textColor=(255, 255, 255), width=600, justified='center')
        self.is_current_player = False
        self.notify_client = pygwidgets.DisplayText(self.window, (400, 200), "It's your turn.", fontSize=20, textColor=(0, 0, 0), width=100, justified='center')
        self.alert_player = False
        self.window_width, self.window_height = self.window.get_size()

    def enter(self, data):
        self.client_name = data.get("player_name")
        self.client_id = data.get("client_id")
        self.lobby_name = data.get("lobby_name")
        self.notification = pygwidgets.DisplayText(self.window, (100, 80), f"{self.client_name} has joined. Waiting for other players to join...", fontSize=20, textColor=(255, 255, 255), width=600, justified='center')
        self.connect()

    def parse_card_info(self, card_info):
        try:
            info = json.loads(card_info)
            color = info['color']
            value = info['value']
            
        except json.JSONDecodeError as e:
            print(f"Error parsing card info: {e}")
            return None
        except KeyError as e:
            print(f"Invalid card data: {e}")
            return None

    def update(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            print(f"Processing message: {message}")
            
            if message.startswith("client_list$"):
                client_names = message.split("$")[1]
                client_list = client_names.split(",")  # Parse the list of client names
                client_list_str = "\n".join(client_list)
                display_message = f"**********Client List**********\n{client_list_str}"
                self.notification.setValue(display_message)
            elif message.startswith("host_status$"):
                print(self.is_host)
                self.is_host = message.split("$")[1] == "yes"
            elif message.startswith("game_end$"):
                parts = message.split('$', 1)
                if len(parts) > 1:
                    winner = parts[1]
                    self.winner = winner
                    self.winner_banner.setValue(f"Winner: {winner}")
                    print(f"Game over! Winner: {winner}")
            elif message.startswith("start_game$"):
                print("Game started")
                self.game_started = True
                self.bg_color = (161, 59, 113)
            elif message.startswith("current_player$"):
                try:
                    data = message.split("$")[1]
                    current_player = json.loads(data)
                    if current_player['client_id'] == self.client_id:
                        print("Current player is me")
                        self.is_current_player = True             
            
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding current player JSON: {e}")            

        self.client_hand = self.create_cards_from_json(self.client_hand)

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.play_button.handleEvent(event):
                if self.client:
                    try:
                        print("sending $start_game message to server")
                        message = "start_game$".encode()
                        try:
                            bytes_sent = self.client.send(message)
                        except Exception as e:
                            print(f"Error sending start_game message: {e}")       
                    except Exception as e:
                        print(f"Error sending draw cards message: {e}")
            if self.is_current_player:
                for card in self.show_hand.cards:
                    if card.handle_event(event):  # Assuming handle_event method checks for some interaction like a mouse click
                        print(f"condition: {self.check_conditions(card, self.current_color, self.current_value)}")
                        if self.check_conditions(card, self.current_color, self.current_value):
                            card_data = card.to_json()
                            try:
                                print("Sending 'play_card' message to server")
                                self.client.send(f"play_card${card_data}\n".encode())
                                self.is_current_player = False
                            except Exception as e:
                                print(f"Error sending 'play_card' message: {e}")
                
    def draw(self):
        self.window.fill((self.bg_color))
        if not self.game_started:
            if self.is_host:
                self.play_button.draw()
            self.notification.draw()
        self.view_opponent.draw()
        if self.is_current_player:
            self.notify_client.draw()
        if len(self.show_hand.cards) != 0:
            self.show_hand.draw()
        if len(self.discard_pile) != 0:
            self.discard_pile[0].card.set_centered_location((self.window_width/2,self.window_height/2))
            self.discard_pile[0].card.reveal()
            self.discard_pile[0].card.draw()
        if self.winner is not None:
            self.winner_banner.draw()
    
    def connect(self):
        global client, HOST_ADDR, HOST_PORT
        
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST_ADDR, HOST_PORT))
            self.client.send(f"NAME:{self.client_name};".encode())  
            self.client.send(f"ID:{self.client_id};".encode())  
            
            threading.Thread(target=self.receive_message_from_server, args=(self.client,), daemon=True).start()
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def receive_message_from_server(self, sck):
        buffer = ""
        while True:
            try:
                data_received = sck.recv(4096).decode()
                #print(f"Received data: {data_received}")
                if data_received:
                    if data_received.startswith("discard_pile"):
                        self.process_message(data_received)
                    else:
                        buffer += data_received
                        while '\n' in buffer:
                            message, buffer = buffer.split('\n', 1)
                            self.process_message(message)

                    time.sleep(0.1)  
            except BlockingIOError:
               
                time.sleep(0.1) 
            except Exception as e:
                logging.error(f"Unhandled error: {e}")
                break
                                    
        sck.close()

    def parse_card_info(self, card_info):
        try:
            info = json.loads(card_info)
            color = info['color']
            value = info['value']
            card = ViewDiscard(self.window, color, value)
            return card
        except json.JSONDecodeError as e:
            print(f"Error parsing card info: {e}")
            return None
        except KeyError as e:
            print(f"Invalid card data: {e}")
            return 
    
    import json

    def extract_game_conditions(self, message):
        prefix, json_part = message.split('$', 1)
        try:
            data = json.loads(json_part)
            current_color = data['current_color']
            current_value = data['current_value']
            return current_color, current_value
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return None, None
        except KeyError as e:
            print(f"Missing a required key in JSON data: {e}")
            return None, None
    
    def process_message(self, message):
        #print(f"Processing message: {message}")
        print(f"host status: {self.is_host}")
        if message.startswith("hand$"):
            json_hand = message[5:]
            try:
                hand_data = json.loads(json_hand)
         
                self.show_hand.update(hand_data)
                self.hand_ready = True
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding hand JSON: {e}")
        elif message.startswith("opponent_cards_count$"):
            try:
                opponent_data = message.split("$")[1]
                self.view_opponent.update_opponent(opponent_data)
            except Exception as e:
                logging.error(f"Error updating opponent data: {e}")    
        elif message.startswith("host_status$"):
            self.is_host = message.split("$")[1] == "yes"
        elif message.startswith("game_conditions$"):
            color, value = self.extract_game_conditions(message)
            print(f"Current color: {color}, Current value: {value}")
            
        elif message.startswith("discard_pile$"):
            
            parts = message.split('$', 1)
                
            if len(parts) > 1:
                card_info = parts[1]
                print(f"JSON String before parsing: {card_info}")
                card = self.parse_card_info(card_info)
               
                self.discard_pile = [card]
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
            print(f"Card color: {card.get_color()}, Current color: {color}")
            return True
        elif card.get_value() == value: 
            print(f"Card value: {card.get_value()}, Current value: {value}")
            return True
        print(f"Card color: {card.get_color()}, Current color: {color}")
        print(f"Card value: {card.get_value()}, Current value: {value}")
        return False
