import pygame
import sys
import socket
import threading
import logging
import pygwidgets
import time
import json
from queue import Queue
from model.player_net import Player
from model.card_net import *
from model.game_net import Game
from model.deck_net import Deck

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



class ServerPlayer(Player):
    def __init__(self, name, client_id=None) -> None:
        super().__init__(name, client_id)
        self.is_host = False 
        
    def __str__(self) -> str:
        return f"{self.get_name()}"
    
    def __repr__(self) -> str:
        return f"player('{self.get_name()}')"
    
    def to_json(self, include_hand=False):
        return super().to_json(include_hand)
        
# Server setup
server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080
clients = []
players = []
clients_names = []
deck = Deck()
game = Game(players, deck)
pygame.init()
last_current_player = None
last_current_color = ""
last_current_value = ""
game_in_progress = False
game_actions = Queue()



screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Server')

start_button = pygwidgets.TextButton(screen, (50, 50), "Start")
stop_button = pygwidgets.TextButton(screen, (160, 50), "Stop")
address_label = pygwidgets.DisplayText(screen, (20, 100), "Address: 127.0.0.1", fontSize=18)
port_label = pygwidgets.DisplayText(screen, (20, 130), "Port: 8080", fontSize=18)
client_list_label = pygwidgets.DisplayText(screen, (20, 160), "**********Client List**********", fontSize=18)

def start_game():
    global game_in_progress, game_loop_thread
    if not game_in_progress:
        game_in_progress = True
        logging.info("Game started.")
    
def stop_game():
    global game_in_progress
    game_in_progress = False
    game_loop_thread.join()

def accept_connections():
    global server, clients, clients_names, players, deck, game
    while True:
        client, addr = server.accept()
        data_received = ""
        while 'NAME:' not in data_received or 'ID:' not in data_received:
            data_received += client.recv(1024).decode()
            #logging.debug(f"Data received: {data_received}")

        name_index = data_received.find("NAME:") + 5
        id_index = data_received.find("ID:") + 3
        name_end = data_received.find(";", name_index)
        id_end = data_received.find(";", id_index)

        client_name = data_received[name_index:name_end if name_end != -1 else None]
        client_id = data_received[id_index:id_end if id_end != -1 else None]

        clients.append(client)
        clients_names.append(client_name)

        # Create a ServerPlayer object with name and ID
        player = ServerPlayer(client_name, client_id)
        players.append(player)
        # Determine and send host status
        host_status_message = "host_status$no\n"
        if players[0] == player:
            player.is_host = True
            host_status_message = "host_status$yes\n"
        print(f"Player {player.get_name()} with ID {player.get_client_id()} has connected.")

        client.send(host_status_message.encode())

        update_client_list_display()
        broadcast_client_list()  # Update all clients with the new list
        
        # Assuming `clients` is a list of socket objects connected to the server
        #heartbeat_thread = threading.Thread(target=send_heartbeat_to_clients, args=(clients,))
        #heartbeat_thread.start()

        threading.Thread(target=handle_client, args=(client, player), daemon=True).start()
        
        
def game_loop():
    global current_color, current_value
    while True:            
        try:
            while not game_actions.empty():
                player, action = game_actions.get_nowait()
                if "start_game$" in action and not game_in_progress:
                    process_control_action(player, action)
                elif game_in_progress:
                    process_game_action(player, action)
                    
            if game_in_progress:
                broadcast_current_player()        
                
            # Other game logic here...
        except Exception as e:
                print(f"Error in game loop: {e}")
        time.sleep(0.1)  # Sleep to reduce CPU usage

def process_game_action(player, action):
    
    if "play_card$" in action:
        parts = action.split('$', 1)
        if len(parts) > 1:
            card_info = parts[1]
            print(f"JSON String before parsing: {card_info}")
            card = parse_card_info(card_info)
            #print(f"Card info: {card}")
            print(player.hand)
            game.play_card(player, card)
            print(player.hand)
            #print(game.discard_pile[0].to_json())
            broadcast_discard_pile(game.discard_pile[0])
            update_hands()
            game.determine_next_player()
            broadcast_current_player()
            game_conditions()
            
        else:
            print("No card data received.")

def update_hands():
    global players
    for player in players:
        hand_json = player.to_json(include_hand=True)
        send_hand = f"hand${hand_json}\n"
        client_index = players.index(player)  # Find the index of the player to match with the client list
        clients[client_index].send(send_hand.encode())  # Send the initial hand to the corresponding 
        broadcast_opponent_card_count()

def process_control_action(player, action):
    if "start_game$" in action:
        initialize_game()


def parse_card_info(card_info):
    try:
        info = json.loads(card_info)
        #print(f" line 166: {info}")
        color = info['color']
        value = info['value']
        #print(f"Color info: {color}, Value info: {value}")
        card = Card(color, value)
        return card
    except json.JSONDecodeError as e:
        print(f"Error parsing card info: {e}")
        return None
    except KeyError as e:
        print(f"Invalid card data: {e}")
        return None
        

def handle_client(client, player):
    while True:
        try:
            message = client.recv(4096).decode().strip()
            # Enqueue the player action along with identifying who made it
            game_actions.put((player, message))
        except Exception as e:
            print(f"Error with client {player.get_name()}: {e}")
            break  # Or handle disconnection and cleanup here

        
def process_played_card(message,player):
    card_info = message.split("$")[1]
    print(f"Card played: {card_info}")
        
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            clients.remove(client)

def broadcast_client_list():
    clients_list_str = "client_list$" + ",".join(clients_names)+"\n"  # Create a string that holds all client names
    broadcast(clients_list_str.encode())
    
def update_client_list_display():
    global client_list_label, clients_names
    display_text = "**********Client List**********\n" + "\n".join(clients_names)
    client_list_label.setValue(display_text)

def broadcast_current_player():
    global players, clients, last_current_player, game
    current_player = game.get_current_player_client_id()
    if current_player != last_current_player:
         last_current_player = current_player
         message = "current_player$" + current_player + "\n"
         for client in clients:
             client.send(message.encode()) 
    # for index, client in enumerate(clients):
    #     message = "current_player$" + current_player + "\n"
    #     client.send(message.encode())
    
def broadcast_opponent_card_count():
    global players, clients
    for index, client in enumerate(clients):
        message_parts = []
        for opponent_index, opponent in enumerate(players):
            if opponent_index != index:
                message_parts.append(f"{opponent.get_name()},{opponent.get_card_count()}")
        message = "opponent_cards_count$" + ";".join(message_parts)+"\n"
        client.send(message.encode())

def broadcast_discard_pile(card):
    global clients, players, game
    message = f"discard_pile${card.to_json()}\n"
    print(f"(line 254){message}")
    for client in clients:
        client.send(message.encode())
        

def game_conditions():
    global game, last_current_color, last_current_value, clients
    current_color = game.current_color
    current_value = game.current_value
    if current_color != last_current_color or current_value != last_current_value:
        last_current_color = current_color
        last_current_value = current_value
        
        message = f"game_conditions${game.condition_to_json()}\n"
        print(f"(line 268) {message}")
        
        for client in clients:
            client.send(message.encode())

def handle_disconnect(client):
    # Remove the client from the list and close the socket
    clients.remove(client)
    client.close()
    print("Client disconnected and removed due to failed heartbeat.")

def start_server():
    global server, HOST_ADDR, HOST_PORT, clients, clients_names, players, game_loop_thread
    start_button.disable()
    stop_button.enable()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(20)  # Listen for connections
    game_loop_thread = threading.Thread(target=game_loop, daemon=True)
    game_loop_thread.start()
    print(f"Server started at {HOST_ADDR} on port {HOST_PORT}.")

    threading.Thread(target=accept_connections, daemon=True).start()

def stop_server():
    global server, clients, clients_names, players
    for client in clients:
        client.close()
    server.close()
    clients = []
    clients_names = []
    players = []
    update_client_list_display()
    start_button.enable()
    stop_button.disable()
    print("Server stopped.")

def initialize_game():
    global players, deck, game, game_in_progress
    deck = Deck()
    deck.shuffle()
    game = Game(players, deck)
    game.initialize_players(7)
    for player in players:
        hand_json = player.to_json(include_hand=True)
        send_hand = f"hand${hand_json}\n"
        #logging.debug(f"Sending hand to {player.get_name()}: {send_hand}")
        client_index = players.index(player)  # Find the index of the player to match with the client list
        clients[client_index].send(send_hand.encode())  # Send the initial hand to the corresponding 
        #logging.debug(f"Sent hand to {player.get_name()}")
        broadcast_opponent_card_count()

    game_in_progress = True
    print("Game initialized.")

def update_clients():
    global clients, players
    for index, client in enumerate(clients):
        player = players[index]
        hand_json = player.to_json(include_hand=True)
        send_hand = f"hand${hand_json}\n"
        client.send(send_hand.encode())

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            
        if start_button.handleEvent(event):
            start_server()
        
        if stop_button.handleEvent(event):
            stop_server()

    screen.fill(GRAY)

    start_button.draw()
    stop_button.draw()
    address_label.draw()
    port_label.draw()
    client_list_label.draw()

    pygame.display.flip()
