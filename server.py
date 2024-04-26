import socketserver
import threading
import json
from model.game_net import Game
from model.deck_net import Deck, CardFactory
from model.player_net import Player 
from queue import Queue
from model.card_net import *
from enum import Enum, auto
import time

class ActionType(Enum):
    PLAY_CARD = auto()
    DRAW_CARD = auto()
    START_GAME = auto()
    PLAY_WILD = auto()
    COLOR_SELECTED = auto()
    END_TURN = auto()

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

class GameRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data_received = ""
        try:
            while True:
                part = self.request.recv(1024).decode()
                if not part:
                    break
                self.data_received += part
                if 'NAME:' in self.data_received and 'ID:' in self.data_received:
                    self.setup_player()
                if "start_game$" in self.data_received:
                    self.server.start_game()
                    self.data_received = ""
                if "play_card$" in self.data_received:
                    parts = self.data_received.split('$',1)
                    action = {"type": ActionType.PLAY_CARD, "data": parts[1]}
                    self.server.game_actions.put(action)
                    self.data_received = ""
                if "draw_card$" in self.data_received:
                    parts = self.data_received.split('$',1)
                    action = {"type": ActionType.DRAW_CARD, "data": parts[1]}
                    self.server.game_actions.put(action)
                    self.data_received = ""
                if "play_wild$" in self.data_received:
                    parts = self.data_received.split('$',1)
                    action = {"type": ActionType.PLAY_WILD, "data": parts[1]}
                    self.server.game_actions.put(action)
                    self.data_received = ""
                if "color_selected$" in self.data_received:
                    parts = self.data_received.split('$',1)
                    action = {"type": ActionType.COLOR_SELECTED, "data": parts[1]}
                    self.server.game_actions.put(action)
                    self.data_received = ""

        except Exception as e:
            print(f"Error: {e}")
            
        finally:
            print(f"Client disonnected: {self.client_address}")
            self.cleanup_client()
        
    def setup_player(self):
        name_index = self.data_received.find("NAME:") + 5
        id_index = self.data_received.find("ID:") + 3
        name_end = self.data_received.find(";", name_index)
        id_end = self.data_received.find(";", id_index)

        client_name = self.data_received[name_index:name_end if name_end != -1 else None]
        client_id = self.data_received[id_index:id_end if id_end != -1 else None]

        if client_name and client_id:
            player = ServerPlayer(client_name, client_id)
            self.server.game.add_player(player)
            self.server.clients.append(self.request)
            self.server.clients_names.append(client_name)
            
            if len(self.server.game.players) == 1:
                player.is_host = True
                host_status_message = "host_status$yes\n"
            else:
                host_status_message = "host_status$no\n"
        
            self.request.sendall(host_status_message.encode())
            print(f"Player {player.get_name()} with ID {player.get_client_id()} has connected.")
            
            self.data_received = self.data_received[id_end+1:]
            
    def cleanup_client(self):
        client_index = self.server.clients.index(self.request)
        self.server.clients.pop(client_index)
        self.server.clients_names.pop(client_index)
        print("Client disconnected.")
              
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.lock = threading.Lock()
        self.allow_reuse_address = True
        self.clients = []
        self.clients_names = []
        self.deck = Deck()
        self.game = Game([], self.deck)
        self.game_actions = Queue()
        self.game_started = False
        self.game_loop_thread = None
        self.last_current_player = ""

    def play_card(self, card_info):
        with self.lock:
            player = self.game.get_current_player()
            card = CardFactory.create_card(card_info['color'], card_info['value'])
            #print(f"hand before play: {player.hand}")
            print(f"Playing card: {card}")
            self.game.play_card(player, card)
            self.broadcast_opponent_card_count()
            self.broadcast_all_hands()
            #print(f"hand after play: {player.hand}")
            if isinstance(card, WildChanger) or isinstance(card, WildPickFour):

                self.request_color_selection(player)
            
            elif isinstance(card, Reverse) or isinstance(card, Skip):
                if not self.game.check_hand(self.game.get_current_player()):
                    self.send_draw_card(self.game.current_player_index)
            else:
    
                self.post_play_card(player)
            
    def post_play_card(self, player):
        if self.game.check_game_end(player):
            self.broadcast_game_end()
            self.game_started = False
        else:
            self.broadcast_game_state()


    def broadcast_game_conditions(self):
        message = f"game_conditions${self.game.condition_to_json()}\n"
        self.broadcast(message)

    def broadcast_game_end(self):
        player = self.game.get_current_player()
        message = f"game_end${player.get_name()}\n"
        for client in self.clients:
            client.send(message.encode())
    
    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message)
            except:
                self.clients.remove(client)

    def start_game(self):
        if not self.game_started:
            self.game.draw_pile.shuffle()
            self.game.initialize_players()
            self.game_started = True
            self.broadcast_start_game()
            if self.game_loop_thread is None:
                self.game_loop_thread = threading.Thread(target=self.game_loop)
                self.game_loop_thread.daemon = True
                self.game_loop_thread.start()
            self.broadcast_opponent_card_count()
            
    def broadcast_discard_pile(self, card):
        print(f"Broadcasting discard pile: {card}")
        try:
            message = f"discard_pile${card.color},{card.value}\n"
            print(f"Broadcasting discard pile message: {message}")
            for client in self.clients:
                client.send(message.encode())
        except Exception as e:
            print(f"Error broadcasting discard pile: {e}")
    
    def broadcast_all_hands(self):
        for player in self.game.players:
            try:
                hand_json = player.to_json(include_hand=True)
                send_hand = f"hand${hand_json}\n"
                client_index = self.game.players.index(player)
                self.clients[client_index].send(send_hand.encode())
            except Exception as e:
                print(f"Failed to send hand update to {player.get_name()}: {str(e)}")


    def broadcast_player_hand(self):
        player = self.game.get_current_player()
        hand_json = player.to_json(include_hand=True)
        send_hand = f"hand${hand_json}\n"
        client_index = self.game.players.index(player)
        self.clients[client_index].send(send_hand.encode())
        
    def broadcast_start_game(self):
        for client in self.clients:
            client.send("start_game$\n".encode())
    
    def broadcast_opponent_card_count(self):
        for index, client in enumerate(self.clients):
            message_parts = []
            for opponent_index, opponent in enumerate(self.game.players):
                if opponent_index != index:
                    message_parts.append(f"{opponent.get_name()},{opponent.get_card_count()}")
            message = "opponent_cards_count$" + ";".join(message_parts)+"\n"
            client.send(message.encode())
    
    def broadcast_current_player(self):
        current_player = self.game.get_current_player_client_id()
        if current_player != self.last_current_player:
            self.last_current_player = current_player
            message = "current_player$" + current_player + "\n"
            print(f"Current player: {current_player}")
            for client in self.clients:
                client.send(message.encode())
            if not self.game.check_hand(self.game.get_current_player()):
                self.send_draw_card(self.game.current_player_index)
            
    def send_draw_card(self, index):
        message = "draw_card$\n"
        print(f"Sending draw card message to {self.clients_names[index]}")
        self.clients[index].send(message.encode())

    def initialize_game(self):
        for player in self.game.players:
            hand_json = player.to_json(include_hand=True)
            send_hand = f"hand${hand_json}\n"
            client_index = self.game.players.index(player)
            self.clients[client_index].send(send_hand.encode())

    def broadcast_wild_color(self, color):
        for client in self.clients:
            client.send(f"wild_color${color}\n".encode())

    def broadcast_game_state(self):
        self.broadcast_discard_pile(self.game.check_last_card_played(self.game.discard_pile))
        self.broadcast_opponent_card_count()
        self.broadcast_player_hand()
        self.game.determine_next_player(skip=False)

    def game_loop(self):
        self.initialize_game()
        while self.game_started:
            if not self.game_actions.empty():
                action = self.game_actions.get()
                if action["type"] == ActionType.PLAY_CARD:
                    self.play_card(json.loads(action["data"]))
                if action["type"] == ActionType.DRAW_CARD:
                    self.game.get_current_player().draw_card(self.game.draw_pile)
                    self.broadcast_game_state()
                if action["type"] == ActionType.PLAY_WILD:
                    parts = action["data"].split(",")
                    color = parts[1]
                    message = f"wild_color${color}\n"
                    self.broadcast(message)
                if action["type"] == ActionType.COLOR_SELECTED:
                    parts = action["data"].split(",")
                    color = parts[0]
                    self.broadcast_wild_color(color)
                    print(f"the player: {self.game.get_current_player().get_name()} selected color: {color}")
                    self.post_play_card(self.game.get_current_player())

            self.broadcast_current_player()
            time.sleep(0.1)

    def request_color_selection(self, player):
        message = "select_color$\n"
        client_index = self.game.players.index(player)
        self.clients[client_index].send(message.encode())


def start_server():
    HOST, PORT = "127.0.0.1", 8080

    server = ThreadedTCPServer((HOST, PORT), GameRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print(f"Server started at {HOST}:{PORT}")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.shutdown()  # Shuts down the server
        server.server_close()  # Closes the server socket
        server_thread.join()  # Waits for the server thread to close
        print("Server has been shut down.")

    return server

if __name__ == "__main__":
    server = start_server()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()
