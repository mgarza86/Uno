import pygame
import pygwidgets
import pyghelpers
import socket
import threading
import queue

class MultiplayerGameBoard(pyghelpers.Scene):
    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        
    
    def enter(self):
        return super().enter()
        
    def handleInputs(self, events, keyPressedList):
        return super().handleInputs(events, keyPressedList)
      
    def draw(self):
        self.window.fill((255, 255, 255))