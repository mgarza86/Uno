import pygame
import pygwidgets

from model.card import Card
from model.deck import Deck
#from model.game import Game

class Player():
    def __init__(self, window ,name) -> None:
        self.window = window
        self.name = name
        self.hand = []
        self.angle = 0
        self.location = (0,0)
        
    def draw_card(self, game_deck):
        self.hand.append(game_deck.get_card())
     
    def play_card(self, card):
        for cards in self.hand:
            if cards.get_name() == card.get_name():
                card_index = self.hand.index(cards)
                self.hand.append(self.hand.pop(card_index))

        return self.hand.pop()   
    
    def get_player_name(self):
        return self.name
    
    def get_index(self):
        return self.position_index
    
    def check_playable_card(self, card, discard_pile_card):
            if card.get_color() == discard_pile_card.get_color():
                return True
            elif card.get_value() == discard_pile_card.get_value():
                return True
            
            return False
    
    def set_rotation(self, angle):
        self.angle = angle
    
    def rotate_hand(self, angle):
        for i in range(len(self.hand)):
            self.hand[i].rotate_card(angle)
        self.angle = angle
    
    def scale_hand(self, scale):
        for i in range(len(self.hand)):
            self.hand[i].scale_card(scale)
        
    def draw(self):
        for i in range(len(self.hand)):
            if i == 0:
                self.location = self.set_card_on_corner(self.hand[i])
                self.hand[i].set_location(self.location)
                self.hand[i].reveal()
                self.hand[i].draw()    
            else:
                self.location = self.next_card_location(self.hand[i-1])

                self.hand[i].set_location((self.location))
                self.hand[i].reveal()
                self.hand[i].draw()
        self.location = (0,0)        
    
    def next_card_location(self, card):
        width, height = card.get_size()
        card_rect = card.get_rect()
        return (card_rect.x+width,card_rect.y)   
            
    def set_card_on_corner(self,card):
        window_width, window_height = self.window.get_size()
        image_width, image_height = card.get_size()
        if self.angle == 0:
            return (0, window_height - image_height)
        elif self.angle == 90:
            
            return (window_width - image_width, window_height - image_height)
        elif self.angle == 180:
            return (0,0)
        elif self.angle == 270:
            return (window_width - image_width, 0)
    
    
class AIPlayer(Player):
    
    def say_uno(self):
        pass
    
    def choose_card(self, hand):
        pass
    
    
 