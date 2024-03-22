import socket
from _thread import *
import sys

server = ""
port = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    
def threaded_client():
    pass