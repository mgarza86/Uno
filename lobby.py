from queue import Queue
import socket
from client_handler import ClientHandler
import threading

class Lobby:
    def __init__(self, host, port, max_players) -> None:
        self.host = host
        self.port = port
        self.max_players = max_players
        self.clients = []
        self.message_queue = Queue()
        self.game_started = False
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        
    def listen_for_clients(self):
        while len(self.clients) < self.max_players:
            conn, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            client_handler = ClientHandler(self.addr, self.message_queue)
            self.clients.append(client_handler)
            
            if len(self.clients) == self.max_players:
                self.start_game()
                
    def start_game(self):
        self.game_started = True
        for client in self.clients:
            client.send("Game is starting!")
            
            #! game initialization here
            
    def distribute_messages(self):
        while not self.game_started:
            sender, message = self.message_queue.get()
            for client in self.clients:
                if client is not sender:
                    client.send(message)
                    
    def run(self):
        threading.Thread(target=self.listen_for_clients).start()
        threading.Thread(target=self.distribute_messages).start()
        
if __name__ == "__main__":
    HOST ='127.0.0.1'
    PORT = 65432
    MAX_PLAYERS = 4
    
    lobby = Lobby(HOST, PORT, MAX_PLAYERS)
    lobby.run()