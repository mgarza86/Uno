import pygame
import pygwidgets
import pyghelpers
import socket
import threading
import queue
import json
from view.view_hand import ViewHand
from view.view_opponent import ViewOpponent
from view.view_discard import ViewDiscard
from model.card_factory import CardFactory
import logging


window_width = 800
window_height = 600
yellow = (255, 255, 0)
black = (0, 0, 0)
gray = (141, 141, 141)
bg = (191,49,0)

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
class GameClient:
    def __init__(self, host, port, message_queue):
        self.host = host
        self.port = port
        self.client_socket = None
        self.message_queue = message_queue
        self.is_connected = False

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.is_connected = True
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_message(self, message):
        if self.is_connected:
            try:
                self.client_socket.send(message.encode())
            except Exception as e:
                print(f"Error sending message: {e}")

    def receive_messages(self):
        buffer = ""
        while self.is_connected:
            try:
                data_received = self.client_socket.recv(4096).decode()
                if data_received:
                    buffer += data_received
                    while '\n' in buffer:
                        message, buffer = buffer.split('\n', 1)
                        self.message_queue.put(message)
            except Exception as e:
                print(f"Error receiving data: {e}")
                self.is_connected = False

    def close_connection(self):
        self.is_connected = False
        self.client_socket.close()

class MultiplayerGameBoard(pyghelpers.Scene):
    def __init__(self, window, settings):
        super().__init__()
        self.window = window
        self.window_width, self.window_height = self.window.get_size()
        self.x_coord = (self.window_width - 200) / 2
        self.y_coord = (self.window_height - 80) / 2

        self.settings = settings
        self.message_queue = queue.Queue()
        self.game_client = GameClient('127.0.0.1', 8080, self.message_queue)
        self.play_button = pygwidgets.TextButton(window, (300, 380), "Play!", width=200, height=60, fontSize=30, upColor=yellow, overColor=yellow, downColor=yellow)
        self.client_hand = ViewHand(self.window, [])
        self.opponent_hand = ViewOpponent(self.window)
        
        self.host_status = False
        self.game_started = False
        self.is_current_player = False
        self.must_draw = False
        self.wild_played = False
        self.choose_color = False

        self.discard_pile = []
        self.bg_color = (0, 0, 0)
        self.current_color = ""
        self.current_value = ""
        self.winner = None
        
        self.winner_text = pygwidgets.DisplayText(self.window, (100, 80),  f"{self.winner}", fontSize=48, textColor=(0,0,0), width=600, justified='center')
        self.track_color = pygwidgets.DisplayText(self.window, (400, 210), f"Current color: {self.current_color}", fontSize=20, textColor=(0, 0, 0), width=200, justified='center')
        self.notify_client = pygwidgets.DisplayText(self.window, (400, 200), "It's your turn.", fontSize=20, textColor=(0, 0, 0), width=200, justified='center')
        self.draw_card_button = pygwidgets.TextButton(window, (100, 300), "Draw Card", width=100, height=50)
        
        self.red_button = pygwidgets.TextButton(self.window, loc=(self.x_coord, self.y_coord), text='Red', upColor=(255,0,0))
        self.green_button = pygwidgets.TextButton(self.window, loc=(self.x_coord + 100, self.y_coord), text='Green', upColor=(0,255,0))
        self.blue_button = pygwidgets.TextButton(self.window, loc=(self.x_coord, self.y_coord + 40), text='Blue', upColor=(0,0,255))
        self.yellow_button = pygwidgets.TextButton(self.window, loc=(self.x_coord + 100, self.y_coord + 40), text='Yellow', upColor=(255,255,0))
        
        # initializing the sound effects:
        self.card_flip_sound = pygwidgets.SoundEffect('sounds/cardFlip.wav')
        self.card_shuffle_sound = pygwidgets.SoundEffect('sounds/cardShuffle.wav')

    def enter(self, data):
        self.client_name = data.get('player_name')
        self.client_id = data.get('client_id')
        self.lobby_name = data.get('lobby_name')
        self.notification = pygwidgets.DisplayText(self.window, (100, 80), f"{self.client_name} has joined. Waiting for other players to join...", fontSize=20, textColor=(255, 255, 255), width=600, justified='center')
        self.connect()

    def connect(self):
        self.game_client.connect()
        self.game_client.send_message(f"LOBBY:{self.lobby_name};NAME:{self.client_name};ID:{self.client_id};")

    def update(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            self.process_message(message)

    def process_message(self, message):
        #print(f"Processing message: {message}")
        if message.startswith("start_game$"):
            print("Game started")
            
            self.game_started = True
            self.bg_color = (161, 59, 113)
            if self.settings.sfx_enabled:
                self.card_shuffle_sound = pygwidgets.SoundEffect('sounds/cardFlip.wav')
        elif message.startswith("hand$"):
            json_hand = message[5:]
            #print(f"Hand message received: {json_hand}")
            try: 
                data = json.loads(json_hand)
                #print(f"Hand data: {data}")
                self.client_hand.update(data)
                print(f"Client hand: {self.client_hand}")
            except Exception as e:
                print(f"Error processing hand message: {e}")
        elif message.startswith("opponent_cards_count$"):
            try:
                data = message.split('$')[1]
                self.opponent_hand.update(data)
            except Exception as e:
                print(f"Error processing opponent cards count message: {e}")
        elif message.startswith("discard_pile$"):
            try:
                data = message.split('$')[1]
                color, value = data.split(',')
                print(f"Discard pile message received: {color}, {value}")
                if color != "black":
                    self.current_color = color
                self.current_value = value
                self.track_color.setText(f"Current color: {self.current_color}")
                card = CardFactory.create_card(self.window, color, value)
                print(f"Discard pile card AF: {card}")
                card.set_centered_location((self.window_width/2, self.window_height/2))
                card.reveal()
                card.set_scale(60)
                self.discard_pile.insert(0, card)
            except Exception as e:
                print(f"Error processing discard pile message: {e}")
        elif message.startswith("game_end$"):
            print(f"{type(message)}")
            msg = message.split('$')[1]
            data = json.loads(msg)
            self.winner = data['name']
            self.winner_text.setText(f"{self.winner} wins!")
        if message.startswith("client_list$"):
                client_names = message.split("$")[1]
                client_list = client_names.split(",")  # Parse the list of client names
                client_list_str = "\n".join(client_list)
                display_message = f"**********Client List**********\n{client_list_str}"
                self.notification.setValue(display_message)
                
            
        elif message.startswith("host_status$"):
            print("host_status message received")
            self.host_status = message.split('$')[1] == "yes"
        elif message.startswith("draw_card$"):
            print("Must draw card")
            logging.debug(f"{self.client_name} received draw card notification.")
            if len(self.discard_pile) != 0:
                self.must_draw = True
        elif message.startswith("wild_color$"):
            self.current_color = message.split('$')[1]
            print(f"color changed to: {self.current_color}")
            self.track_color.setText(f"Current color: {self.current_color}")
            self.choose_color = False
        elif message.startswith("current_player$"):
            current_player_id = message.split('$')[1]
            current_player = json.loads(current_player_id)
            if current_player['client_id'] == self.client_id:
                self.is_current_player = True
            else:
                self.is_current_player = False
        elif message.startswith("select_color$"):
            self.choose_color = True
            
    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.play_button.handleEvent(event):
                self.game_client.send_message("start_game$")
            elif self.is_current_player:
                for card in self.client_hand.cards:
                    #print(f"Player:{self.client_name} hand: {self.client_hand}")
                    if card.handle_event(event):
                        print(f"Card clicked: {card.get_name()}")
                        print(f"current conditions: {self.current_color} {self.current_value}")
                        if self.check_conditions(card, self.current_color, self.current_value):
                            if self.settings.sfx_enabled:
                                self.card_flip_sound.play()
                            print(f"Card played: {card.get_name()}")
                            self.is_current_player = False
                            info = card.to_dict()
                            info['client_id'] = self.client_id
                            play_info = json.dumps(info)
                            logging.debug(f"{self.client_name} sent a play_card${play_info}\n  to the server.")
                            self.game_client.send_message(f"play_card${play_info}\n")
                            
                            #print(f"{self.client_name} played: {card.get_name()}")
                            logging.debug(f"{self.client_name} played: {card.get_name()}")
                        else:
                            print("Invalid card played")
                    elif self.must_draw and self.is_current_player:
                        if self.draw_card_button.handleEvent(event):
                            if self.settings.sfx_enabled:
                                self.card_flip_sound.play()
                            logging.debug(f"{self.client_name} sent a draw_card$ request to the server.")
                            client = {"client_id": self.client_id}
                            info = json.dumps(client)
                            
                            self.game_client.send_message(f"draw_card${info}\n")
                            self.must_draw = False
                if self.choose_color:
                    if self.red_button.handleEvent(event):
                        self.game_client.send_message(f"color_selected$red\n")
                    elif self.green_button.handleEvent(event):
                        self.game_client.send_message(f"color_selected$green\n")
                    elif self.blue_button.handleEvent(event):
                        self.game_client.send_message(f"color_selected$blue\n")
                    elif self.yellow_button.handleEvent(event):
                        self.game_client.send_message(f"color_selected$yellow\n")
                                    
    def draw(self):
        # Clear the screen first
        self.window.fill(self.bg_color)

        # Draw play button if the host status is True
        if not self.game_started:
            if self.host_status:
                self.play_button.draw()
            self.notification.draw()
        
        if self.winner is not None:
            self.winner_text.draw()
        
        self.track_color.draw()
        
        if self.is_current_player:
            self.notify_client.draw()

        # Draw the client's hand if there are cards
        if len(self.client_hand.cards) != 0:
            self.client_hand.draw()

        # Draw the opponent's hand
        self.opponent_hand.draw()

        # Draw the discard pile if there are cards
        if len(self.discard_pile) != 0 and self.discard_pile[0] is not None:
            #sprint(f"Discard pile {self.discard_pile[0].card}")
            self.discard_pile[0].draw()
        
        if self.must_draw and len(self.discard_pile) != 0:
            self.draw_card_button.draw()
        
        if self.is_current_player:
            if self.choose_color:
                self.red_button.draw()
                self.green_button.draw()
                self.blue_button.draw()
                self.yellow_button.draw()


    def check_conditions(self, card, color, value):
        if color == "":
            print("No color condition, therefore true")
            return True
        elif color == "black":
            print("Black condition, therefore wild and true")
            return True
        elif card.get_color() == "black":
            print("Card color is black, therefore wild and true")
            return True
        elif card.get_color() == color:  
            print("Color match, therefore true")
            return True
        elif card.get_value() == value: 
            print("Value match, therefore true")
            return True
        else:
            print("No match, therefore false")
            return False