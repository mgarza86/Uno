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
        
    def __str__(self):
        return f"{self.color} {self.value}"

    def __repr__(self):
        return f"Card('{self.color}', {self.value},{self.card_name})"
    
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
    
    def set_centered_location(self, location):
        self.images.setCenteredLoc(location)
    
    def draw(self):
        self.images.draw()
    
    def rotate_card(self, angle):
        self.images.rotateTo(angle)
    
    def set_scale(self, scale, scaleFromCenter=False):
        self.images.scale(scale, scaleFromCenter)
        
    def get_rect(self):
        return self.images.getRect()
    
    def get_collide_point(self,mouse_x, mouse_y):
        return self.images.getRect().collidepoint(mouse_x, mouse_y)
    
    def get_size(self):
        return self.images.getSize()

    def move_x(self, pixels):
        self.images.moveX(pixels)
    
    def handle_event(self, event):
        if self.images.handleEvent(event):
            return True
        else:
            return False
        
    
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