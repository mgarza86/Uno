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
            file_name = './images/' + self.card_name + '.png'
            
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
        
class WildChanger(Card):
    
    WILD_CARD = pygame.image.load('./images/black_wild.png')
    
    def __init__(self, window, color, value) -> None:
        super().__init__(window, color, value)
        self.images = pygwidgets.ImageCollection(window, (0,0), {'front': WildChanger.WILD_CARD, 'back': Card.BACK_OF_CARD}, 'back')
        
    def pick_color(self, color):
        self.value = None
        self.color = color
        

class WildPickFour(WildChanger):
    
    WILD_PICK_FOUR = pygame.image.load('./images/black_pickfour.png')
    
    def __init__(self, window, color, value) -> None:
        super().__init__(window, color, value)
        self.images = pygwidgets.ImageCollection(window, (0,0), 
                                                 {'front': WildPickFour.WILD_PICK_FOUR, 
                                                  'back': Card.BACK_OF_CARD}, 'back')
    
    def draw_four(self):
        pass    
        
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