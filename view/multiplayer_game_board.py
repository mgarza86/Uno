import pygame
import pygwidgets
import pyghelpers
import socket
import threading
import queue

class MultiplayerGameBoard(pyghelpers.Scene):
    def __init__(self) -> None:
        super().__init__()