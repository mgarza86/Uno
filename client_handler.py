import socket
import threading
from queue import Queue

class ClientHandler:
    def __init__(self, conn, addr, message_queue) -> None:
        self.conn = conn
        self.addr = addr
        self.message_queue = message_queue
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        
    def run(self):
        while True:
            try:
                data = self.conn.recv(1024).decode()
                if not data:
                    break
                self.message_queue.put((self,data))
            except ConnectionResetError:
                self.conn.close()
    
    def send(self, message):
        try:
            self.conn.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message to a {self.addr}: {e}")
            