import pygame
import sys
import socket
import threading
import pygwidgets
from time import sleep
from model.player_net import Player
from model.card_net import *
from model.game_net import Game
from model.deck_net import Deck
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
        while len(data_received.split(':')) < 3:  # Ensure both NAME: and ID: are received
            data_received += client.recv(1024).decode()
        
        data_parts = data_received.split(':')
        client_name = data_parts[1] if "NAME" in data_parts[0] else data_parts[3]
        client_id = data_parts[3] if "ID" in data_parts[2] else data_parts[1]
        
        clients.append(client)
        clients_names.append(client_name)

        # Create a ServerPlayer object with name and ID
        player = ServerPlayer(client_name, client_id)
        players.append(player)

        # Determine and send host status
        host_status_message = "host_status$no"
        if players[0] == player:
            player.is_host = True
            host_status_message = "host_status$yes"
        print(f"Player {player.get_name()} with ID {player.get_client_id()} has connected.")

        client.send(host_status_message.encode())

        update_client_list_display()
        broadcast_client_list()  # Update all clients with the new list
        
        threading.Thread(target=handle_client, args=(client, player), daemon=True).start()

        
def handle_client(client, player):
    global players, deck
    while True:
        try:
            message = client.recv(4096).decode()
            if message == "start_game$":
                if player.is_host:  # Ensuring only the host can start the game
                    print("Starting the game...")
                    game_loop(message, players)
                else:
                    print(f"Player {player.get_name()} attempted to start the game, but is not the host.")
                
        except Exception as e:
            print(f"Error handling client: {e}")
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
        send_hand = f"hand${hand_json}"
        client_index = players.index(player)  # Find the index of the player to match with the client list
        clients[client_index].send(send_hand.encode())  # Send the initial hand to the corresponding client
    
    while not game.check_game_end():
        current_player = game.broadcast_current_player()
        
        # notify current player to all clients
        broadcast(f"current_player${current_player}".encode())
        
        # wait for current player to play card or draw card
        if message.startswith("play_card$"):
            card_played = message.split("$")[1]
            current_player.play_card(card_played)
            
        elif message.startswith("draw_card$"):
            current_player.draw_card(deck)
        
        # check if current player has won
        if game.check_game_end(current_player):
            broadcast("game_end$".encode())
            break
        
        # if current player has not won, check the card played
        # if card played is a special card, perform the action
        
        # determine next player
            
        # broadcast the updated card count to all clients
        # broadcast the updated discard pile to all clients
        # broadcast the updated current player to all clients
            
        # continue loop until game ends
        
    # if current player has won, notify all clients who won break out of loop
    winner = current_player.get_name()
    notification = f"game_end${winner} has won!"
        
    
        
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            clients.remove(client)

def broadcast_client_list():
    clients_list_str = "client_list$" + ",".join(clients_names)  # Create a string that holds all client names
    broadcast(clients_list_str.encode())
    
def update_client_list_display():
    global client_list_label, clients_names
    display_text = "**********Client List**********\n" + "\n".join(clients_names)
    client_list_label.setValue(display_text)
    
def broadcast_opponent_card_count():
    global players, clients
    for index, client in enumerate(clients):
        message_parts = []
        for opponent_index, opponent in enumerate(players):
            if opponent_index != index:
                message_parts.append(f"{opponent.get_name()},{opponent.get_card_count()}")
        message = "opponent_cards_count$" + ";".join(message_parts)
        client.send(message.encode())

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
