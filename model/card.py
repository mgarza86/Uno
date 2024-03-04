import pygame
import pygwidgets
import os

class Card():
    
    BACK_OF_CARD = pygame.image.load('./images/card_back_alt.png')
    
    def __init__(self, window, color, value, file_name=None):
        self.window = window
        self.color = color
        self.value = value
        self.card_name = color + '_' + value
        
        if file_name is None:
            file_name + '..images/' + self.card_name + '.png'
            
        self.images = pygwidgets.ImageCollection(window, (0,0), 
                                                 {'front': file_name,
                                                  'back': Card.BACK_OF_CARD},'back')
    
    def conceal(self):
        self.images.replace('back')
        
    def reveal(self):
        self.images.replace('front')
        
    def get_color(self):
        return self.color
    
    def get_value(self):
        return self.value
    
    def get_name(self):
        return self.card_name
    
    def get_location(self):
        return self.images.getLoc()
    
    def set_location(self, location):
        self.images.setLoc(location)
    
    def draw(self):
        # renders card
        self.images.draw()
        
class Skip(Card):
        
    def skip(self):
        pass
        

class DrawTwoCard(Card):
        
    def draw_two(self):
        pass
        
class Reverse(Card):
        
    def reverse(self):
        # function pending game class receation
        pass