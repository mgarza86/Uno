import pygame
import pygwidgets

class CardView():
        
        BACK_OF_CARD = pygame.image.load('./images/card_back_alt.png')
        
        def __init__(self, window, card, file_name=None):
            self.window = window
            self.card = card
            
            if file_name is None:
                file_name = f'./images/{card.color}_{card.value}.png'
                
            self.images = pygwidgets.ImageCollection(window, (0,0), 
                                                    {'front': file_name,
                                                    'back': CardView.BACK_OF_CARD},'back')
        
        def conceal(self):
            self.images.replace('back')
            
        def reveal(self):
            self.images.replace('front')
        
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