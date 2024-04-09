import pygame
import pygwidgets 
import pyghelpers
import model.game

class EndScreen(pyghelpers.Scene):
    
    def __init__(self, window, settings) -> None:
        super().__init__()
        self.window = window
        self.settings = settings
        self.back_ground_color = (161, 59, 113)
        
    
    def enter(self, data):
        self.winner = data
        self.banner = self.winner + ' wins!'
        self.winner_banner = pygwidgets.DisplayText(self.window, (400,300), self.banner, fontSize=30)
        
    
    def handleInputs(self, events, keyPressedList):
        pass
        
    def draw(self):
        self.winner_banner.draw()