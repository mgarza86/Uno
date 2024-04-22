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
        self.settings = settings
        self.message_queue = queue.Queue()
        self.game_client = GameClient('127.0.0.1', 8080, self.message_queue)
        self.play_button = pygwidgets.TextButton(window, (100, 200), "Play", width=100, height=50)
        self.client_hand = ViewHand(self.window, [])
        self.opponent_hand = ViewOpponent(self.window)
        self.host_status = False
        self.game_started = False
        self.is_current_player = False
        self.discard_pile = []
        self.bg_color = (255, 255, 255)
        self.current_color = ""
        self.current_value = ""

    def enter(self, data):
        self.client_name = data.get('player_name')
        self.client_id = data.get('client_id')
        self.connect()

    def connect(self):
        self.game_client.connect()
        self.game_client.send_message(f"NAME:{self.client_name};ID:{self.client_id};")

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
        elif message.startswith("hand$"):
            json_hand = message[5:]
            print(f"Hand message received: {json_hand}")
            try: 
                data = json.loads(json_hand)
                print(f"Hand data: {data}")
                self.client_hand.update(data)
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
                self.current_color = color
                self.current_value = value
                card = CardFactory.create_card(self.window, color, value)
                print(f"Discard pile card AF: {card}")
                card.set_centered_location((self.window_width/2, self.window_height/2))
                card.reveal()
                card.set_scale(60)
                self.discard_pile.insert(0, card)
            except Exception as e:
                print(f"Error processing discard pile message: {e}")
        elif message.startswith("host_status$"):
            print("host_status message received")
            self.host_status = message.split('$')[1] == "yes"
            print(self.host_status)

        elif message.startswith("current_player$"):
            current_player_id = message.split('$')[1]
            current_player = json.loads(current_player_id)
            if current_player['client_id'] == self.client_id:
                self.is_current_player = True
            else:
                self.is_current_player = False

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.play_button.handleEvent(event):
                self.game_client.send_message("start_game$")
            elif self.is_current_player:
                for card in self.client_hand.cards:
                    if card.handle_event(event):
                        if self.check_conditions(card, self.current_color, self.current_value):
                            self.game_client.send_message(f"play_card${card.to_json()}\n")            
                        else:
                            print("Invalid card played")

    def draw(self):
        # Clear the screen first
        self.window.fill(self.bg_color)

        # Draw play button if the host status is True
        if not self.game_started:
            if self.host_status:
                self.play_button.draw()

        # Draw the client's hand if there are cards
        if len(self.client_hand.cards) != 0:
            self.client_hand.draw()

        # Draw the opponent's hand
        self.opponent_hand.draw()

        # Draw the discard pile if there are cards
        if len(self.discard_pile) != 0 and self.discard_pile[0] is not None:
            #sprint(f"Discard pile {self.discard_pile[0].card}")
            self.discard_pile[0].draw()


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