import pygame
import sys
import socket
import threading
import logging
import pygwidgets
import time
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


screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Server')

start_button = pygwidgets.TextButton(screen, (50, 50), "Start")
stop_button = pygwidgets.TextButton(screen, (160, 50), "Stop")
address_label = pygwidgets.DisplayText(screen, (20, 100), "Address: 127.0.0.1", fontSize=18)
port_label = pygwidgets.DisplayText(screen, (20, 130), "Port: 8080", fontSize=18)
client_list_label = pygwidgets.DisplayText(screen, (20, 160), "**********Client List**********", fontSize=18)

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
        heartbeat_thread = threading.Thread(target=send_heartbeat_to_clients, args=(clients,))
        heartbeat_thread.start()

        threading.Thread(target=handle_client, args=(client, player), daemon=True).start()
        
def handle_client(client, player):
    global players, deck
    while True:
        try:
            print(client)
            message = client.recv(4096).decode().strip()
            logging.debug(f"Received message from {player.get_name()}: {message}")
            print(f"Received message from {player.get_name()}: {message}")
            if "start_game$" in message:
                print("Start game message received")
                if player.is_host:  # Ensuring only the host can start the game
                    print("Starting the game...")
                    game_loop(message, players)
                else:
                    print(f"Player {player.get_name()} attempted to start the game, but is not the host.")
            elif message.startswith("play_card$"):
                print("Play card message received")
                # Here, process the play_card logic
                process_played_card(message, player)
            elif message.startswith("draw_card$"):
                # Handle draw card logic
                pass
                #process_draw_card(player)
            elif message.startswith("heartbeat$"):
                print("Heartbeat received from client.")
            else:
                print(f"Unhandled message: {message}")
        except Exception as e:
            print(f"Error handling client: {e}")
            logging.error(f"Error handling client: {e}")
            # Error handling and cleanup
            clients.remove(client)
            clients_names.remove(player.get_name())
            players.remove(player)
            print(f"Player {player.get_name()} has disconnected.")
            update_client_list_display()
            broadcast_client_list()  # Update all clients on disconnect
            client.close()
            break

        
def game_loop(message, players):
    global clients  
    deck = Deck()
    deck.shuffle()
    game = Game(players, deck)
    game.initialize_players(7)  # Initialize players with 7 cards each
    broadcast_opponent_card_count()
    
    for player in players:
        hand_json = player.to_json(include_hand=True)
        send_hand = f"hand${hand_json}\n"
        #logging.debug(f"Sending hand to {player.get_name()}: {send_hand}")
        client_index = players.index(player)  # Find the index of the player to match with the client list
        clients[client_index].send(send_hand.encode())  # Send the initial hand to the corresponding 
        #logging.debug(f"Sent hand to {player.get_name()}")
        broadcast_opponent_card_count()

    in_progress = True
    while in_progress:
        broadcast_current_player()
        #current_player = game.broadcast_current_player()
        
        # notify current player to all clients
        #broadcast(f"current_player${current_player}".encode())
        #logging.debug(f"Current player (server side): {current_player}")
        
        # wait for current player to play card or draw card
        if message.startswith("play_card$"):
            print("played card received")
            card_played = message.split("$")[1]
            player = game.get_current_player()
            game.play_card(player, card_played)
            
            #current_player.play_card(card_played)
            
        elif message.startswith("draw_card$"):
            pass
            #current_player.draw_card(deck)
        
        # check if current player has won
        if game.check_game_end(game.get_current_player()):
            broadcast("game_end$".encode())
            in_progress = False
            break
        
        # if current player has not won, check the card played
        # if card played is a special card, perform the action
        
        # determine next player
            
        # broadcast the updated card count to all clients
        # broadcast the updated discard pile to all clients
        # broadcast the updated current player to all clients
            
        # continue loop until game ends
        
    # if current player has won, notify all clients who won break out of loop
    #winner = current_player.get_name()
    notification = f"game_end BLANK has won!"
        
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

def broadcast_discard_pile():
    pass

def game_conditions():
    global game, last_current_color, last_current_value, clients
    current_color = game.get_current_color()
    current_value = game.get_current_value()
    if current_color != last_current_color or current_value != last_current_value:
        last_current_color = current_color
        last_current_value = current_value
        message = f"game_conditions${current_color},{current_value}\n"
        for client in clients:
            client.send(message.encode())

def send_heartbeat_to_clients(clients, interval=5):
    while True:
        for client in clients:
            try:
                client.send(b'heartbeat$\n')
            except socket.error as e:
                print(f"Error sending heartbeat: {e}")
                handle_disconnect(client)
        time.sleep(interval)
        
def handle_disconnect(client):
    # Remove the client from the list and close the socket
    clients.remove(client)
    client.close()
    print("Client disconnected and removed due to failed heartbeat.")

def start_server():
    global server, HOST_ADDR, HOST_PORT, clients, clients_names, players
    start_button.disable()
    stop_button.enable()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # Listen for connections
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
