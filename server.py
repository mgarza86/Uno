import socketserver
import threading
import json
from model.game_net import Game
from model.deck_net import *
from model.player_net import Player 
from queue import Queue
from model.card_net import *
from enum import Enum, auto
import time
import logging

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
                print(f"Received data (part): {part}")
                if not part:
                    break
                self.data_received += part
                print(f"Received data: {self.data_received}")
                
                if 'NAME:' in self.data_received and 'ID:' in self.data_received:
                    logging.info(f"Received data: {self.data_received}")
                    self.setup_player()
                if "start_game$" in self.data_received:
                    logging.info("Game starting...")
                    self.server.start_game()
                    self.data_received = ""
                if "play_card$" in self.data_received:
                    parts = self.data_received.split('$',1)
                    print(f"Playing card: {parts[1]}")
    
                    data = json.loads(parts[1])
                    print(f"Data: {data}")
                    action = {"type": ActionType.PLAY_CARD, "data": data}
                    self.server.game_actions.put(action)
                    self.data_received = ""
                if "draw_card$" in self.data_received:
                    parts = self.data_received.split('$', 1)
                    try:
                        data_dict = json.loads(parts[1])  # Parse JSON string into a Python dictionary
                        action = {"type": ActionType.DRAW_CARD, "data": data_dict}
                        self.server.game_actions.put(action)
                        self.data_received = ""
                    except json.JSONDecodeError as e:
                        print("Failed to decode JSON:", e)
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
        self.deck = NormalCardDeck()
        self.game = Game([], self.deck)
        self.game_actions = Queue()
        self.game_started = False
        self.game_loop_thread = None
        self.last_current_player = ""

    def player_from_uuid(self, uuid):
        for player in self.game.players:
            if player.get_client_id() == uuid:
                return player
        return None
    
    def play_card(self, card_info):
        with self.lock:
            player = self.player_from_uuid(card_info['client_id'])
            
            card = CardFactory.create_card(card_info['color'], card_info['value'])
            print(f"Playing card: {card}")
            logging.info(f"{player} played: {card}")
            self.game.play_card(player, card, online=True)
            self.broadcast_opponent_card_count()
            self.broadcast_all_hands()
            
            if isinstance(card, WildChanger) or isinstance(card, WildPickFour):
                logging.info(f"{player.get_name()} played a wild card")
                logging.info(f"Requesting color selection from {player.get_name()}")
                self.request_color_selection(player)
                if isinstance(card, WildPickFour):
                    
                    victim_index = card.perform_action(self.game, online=True)
                    logging.info(f"{self.game.players[victim_index].get_name()} will draw 4 cards")
                    self.game.players[victim_index].draw_card(self.game.draw_pile)
                    self.game.players[victim_index].draw_card(self.game.draw_pile)
                    self.game.players[victim_index].draw_card(self.game.draw_pile)
                    self.game.players[victim_index].draw_card(self.game.draw_pile)
                    self.broadcast_all_hands()
                
                print("check hand")    
                if not self.game.check_hand(player):
                    print("hand checked")
                    logging.info(f"sending draw card to {player.get_name()}")
                    self.send_draw_card(self.game.current_player_index)
            elif isinstance(card, Reverse):
                if len(self.game.players) == 2:
                    card.perform_action(self.game, online=True)
                    self.post_play_card(player)
                    if not self.game.check_hand(self.game.get_current_player()):
                        logging.info(f"sending draw card to {player.get_name()}")
                        self.send_draw_card(self.game.current_player_index)
                else:
                    card.perform_action(self.game, online=True)
                    self.post_play_card(player)
                
            elif isinstance(card, DrawTwoCard):
                victim_index = card.perform_action(self.game, online=True)
                logging.info(f"{self.game.players[victim_index].get_name()} will draw 2 cards")
                self.game.players[victim_index].draw_card(self.game.draw_pile)
                self.game.players[victim_index].draw_card(self.game.draw_pile)
                self.broadcast_all_hands()
                print("LINE 220 - player change")
                self.game.determine_next_player(skip=False)
                self.post_play_card(player)

            elif isinstance(card, Skip):
                card.perform_action(self.game, online=True)

                logging.info(f"Skipping opponent's turn.")
                if not self.game.check_hand(self.game.get_current_player()):
                    logging.info(f"sending draw card to {player.get_name()}")
                    self.send_draw_card(self.game.current_player_index)
                else:
                    logging.info(f"player {player.get_name()} has a card to play") 
                self.post_play_card(player)
            elif isinstance(card, Card): #! this doesn't appear to be right
                print("LINE 234 - DETERMINING NEXT PLAYER")
                self.game.determine_next_player(skip=False)
                self.post_play_card(player)
            else:
                logging.info(f"{player.get_name()} played {card}")
                print("LINE 240 - DETERMINING NEXT PLAYER")
                self.game.determine_next_player(skip=False)
                self.post_play_card(player)
            
    def post_play_card(self, player):
        if self.game.check_game_end(player):
            self.broadcast_game_end(player)
            self.game_started = False
        else:
            self.broadcast_game_state()

    def broadcast_game_conditions(self):
        message = f"game_conditions${self.game.condition_to_json()}\n"
        self.broadcast(message)

    def broadcast_game_end(self, player):
        name = player.get_name()
        uuid = player.get_client_id()
        data = {"name": name, "uuid": uuid}
        json_data = json.dumps(data)
        message = f"game_end${json_data}\n"
        print(f"Broadcasting game end message: {message}")
        print(f"Type: {type(message)}")
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
            self.game.draw_pile.shuffle()
            self.game.draw_pile.shuffle()
            self.game.initialize_players(number_of_cards=7)
            self.game_started = True
            self.broadcast_start_game()
            if self.game_loop_thread is None:
                self.game_loop_thread = threading.Thread(target=self.game_loop)
                self.game_loop_thread.daemon = True
                self.game_loop_thread.start()
            self.broadcast_opponent_card_count()
            self.broadcast_current_player() 
            
    def broadcast_discard_pile(self, card):
        print(f"LINE 251 - Broadcasting current player: {self.game.get_current_player()}")
        print(f"Broadcasting discard pile: {card}")
        try:
            message = f"discard_pile${card.color},{card.value}\n"
            print(f"Broadcasting discard pile message: {message}")
            print(f"Broadcasting current player: {self.game.get_current_player()}")
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
        message = "current_player$" + current_player + "\n"

        for client in self.clients:
            client.send(message.encode())
        if not self.game.check_hand(self.game.get_current_player()):
            self.send_draw_card(self.game.current_player_index)
            
    def send_draw_card(self, index):
        message = "draw_card$\n"
        print(f"Sending draw card message to {self.clients_names[index]}")
        logging.info(f"Sending draw card message to {self.clients_names[index]}")
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

    def broadcast_game_state(self, card=None):
        if card is not None:
            self.broadcast_discard_pile(card)
            logging.info(f"Broadcasting discard pile: {card}")
        else:
            self.broadcast_discard_pile(self.game.check_last_card_played(self.game.discard_pile))
            logging.info(f"Broadcasting discard pile: {self.game.check_last_card_played(self.game.discard_pile)}")
        self.broadcast_opponent_card_count()
        self.broadcast_all_hands()

    def game_loop(self):
        self.initialize_game()
        notified_turn_start = False
        while self.game_started:
            if not notified_turn_start:
                self.broadcast_current_player()
                notified_turn_start = True
            if not self.game_actions.empty():
                action = self.game_actions.get()
                if action["type"] == ActionType.PLAY_CARD:
                    self.play_card(action["data"])
                    notified_turn_start = False
                if action["type"] == ActionType.DRAW_CARD:
                    player = self.player_from_uuid(action["data"]["client_id"])
                    player.draw_card(self.game.draw_pile)
                    logging.info(f"recieved draw card action from {player.get_name()}")
                    logging.info(f"{player.get_name()} drew a card...")
                    print("LINE 379 - DETERMINING NEXT PLAYER")
                    self.game.determine_next_player(skip=False)
                    self.broadcast_game_state()
                    notified_turn_start = False
                if action["type"] == ActionType.PLAY_WILD:
                    logging.info(f"{self.game.get_current_player().get_name()} played a wild card...")
                    parts = action["data"].split(",")
                    color = parts[1]
                    message = f"wild_color${color}\n"
                    logging.info(f"Broadcasting wild color: {color}")
                    self.broadcast(message)
                if action["type"] == ActionType.COLOR_SELECTED:
                    parts = action["data"].split(",")
                    color = parts[0]
                    logging.info(f"{self.game.get_current_player().get_name()} selected color: {color}")
                    self.broadcast_wild_color(color)
                    self.game.set_current_color(color)
                    print(f"the player: {self.game.get_current_player().get_name()} selected color: {color}")
                    self.post_play_card(self.game.get_current_player())
                    logging.info(f"Determining next player...")
                    print("LINE 399 - DETERMINING NEXT PLAYER")
                    self.game.determine_next_player(skip=False)
                    if not self.game.check_hand(self.game.get_current_player()):
                        print("LINE 385 - checking hand")
                        logging.info(f"sending draw card to {self.game.get_current_player().get_name()}")
                        self.send_draw_card(self.game.current_player_index)    
                    logging.info(f"Next player is {self.game.get_current_player().get_name()}")
                    notified_turn_start = False

            
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
