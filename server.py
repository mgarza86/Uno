import socket
from _thread import *
import sys
from dotenv import load_dotenv
import os

load_dotenv()

server = os.getenv('SERVER_IP')
port = int(os.getenv('PORT',3000))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
   
s.listen(4)
print("waiting for a connection, Server Started")
       
def threaded_client(conn):
    conn.send(str.encode("Welcome to the py-uno server!"))
    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                print("Disconnected")
                break
            print(f"Received: {data}")
            reply = f"Server echo: {data}"
            conn.sendall(str.encode(reply))
        except:
            break
        
    print("Lost connection")
    conn.close()
    
while True:
    conn, addr = s.accept()
    print(f"Conntected to: {addr}")
    
    start_new_thread(threaded_client,(conn,))
        