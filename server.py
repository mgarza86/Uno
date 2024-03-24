import pygame
import sys
import socket
import threading
import pygwidgets
from time import sleep

# Server setup
server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080
clients = []
clients_names = []

pygame.init()


screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Server')

start_button = pygwidgets.TextButton(screen, (50, 50), "Start")
stop_button = pygwidgets.TextButton(screen, (160, 50), "Stop")
address_label = pygwidgets.DisplayText(screen, (20, 100), "Address: 127.0.0.1", fontSize=18)
port_label = pygwidgets.DisplayText(screen, (20, 130), "Port: 8080", fontSize=18)
client_list_label = pygwidgets.DisplayText(screen, (20, 160), "**********Client List**********", fontSize=18)


# Create a thread for accepting connections
def accept_connections():
    global server, clients, clients_names
    while True:
        client, addr = server.accept()
        client.send("NAME".encode())
        client_name = client.recv(1024).decode()

        clients.append(client)
        clients_names.append(client_name)

        update_client_list_display()
        broadcast_client_list()  # Update all clients with the new list

        threading.Thread(target=handle_client, args=(client, client_name), daemon=True).start()
        
        
def handle_client(client, client_name):
    while True:
        try:
            message = client.recv(4096).decode()
            # Handle messages
        except Exception as e:
            clients.remove(client)
            clients_names.remove(client_name)
            update_client_list_display()
            broadcast_client_list()  # Update all clients on disconnect
            client.close()
            break
        
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

def start_server():
    global server, HOST_ADDR, HOST_PORT, clients, clients_names
    start_button.disable()
    stop_button.enable()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # Listen for connections
    print(f"Server started at {HOST_ADDR} on port {HOST_PORT}.")

    threading.Thread(target=accept_connections, daemon=True).start()

def stop_server():
    global server, clients, clients_names
    for client in clients:
        client.close()
    server.close()
    clients = []
    clients_names = []
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
