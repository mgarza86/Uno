import socket

def main():
    server = '127.0.0.1'
    port = 3000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
       
       client_socket.connect((server, port))
       
       welcome_message =  client_socket
       
       welcome_message = client_socket.recv(2048).decode()
       print(welcome_message)
       
       message = "Hello, server!"
       print(f"Sending: {message}")
       client_socket.send(str.encode(message))
       
       response = client_socket.recv(2048).decode()
       print(f"Received: {response}")
       
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()