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
        
    def draw(self):
        for i in range(len(self.hand)):
            self.hand[i].set_location((100 + i * 100, 400))
            self.hand[i].reveal()
            self.hand[i].draw()
       
            
        
class AIPlayer(Player):
    
    def say_uno(self):
        pass
    
    def choose_card(self, hand):
        pass
    
    
 