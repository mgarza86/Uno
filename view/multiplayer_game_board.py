import pygame
import pygwidgets
import pyghelpers
import socket
import threading
import queue

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
        self.settings = settings
        self.message_queue = queue.Queue()
        self.game_client = GameClient('127.0.0.1', '8080', self.message_queue)
        self.play_button = pygwidgets.TextButton(window, (100, 200), "Play", width=100, height=50)
        ...
        self.connect()

    def enter(self, data):
        self.client_name = data['player_name']
        self.client_id = data['client_id']

    def connect(self):
        self.game_client.connect()
        self.game_client.send_message(f"NAME:{self.client_name};ID:{self.client_id};")

    def update(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            self.process_message(message)

    def process_message(self, message):
        pass

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.play_button.handleEvent(event):
                self.game_client.send_message("start_game$")
            

    def draw(self):
        pass


