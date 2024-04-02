import pygame
import pygwidgets

from model.card import Card
from model.deck import Deck
class Player():
    def __init__(self, name) -> None:
        #self.window = window
        self.name = name
        self.hand = []
        self.angle = 0
        self.location = (0,0)
        
    def draw_card(self, game_deck):
        print(self.get_name(), "drew a card")
        self.hand.append(game_deck.get_card())
     
    def play_card(self, card):
        for cards in self.hand:
            if cards.get_name() == card.get_name():
                card_index = self.hand.index(cards)
                self.hand.append(self.hand.pop(card_index))

        return self.hand.pop()   
    
    def get_name(self):
        return self.name
    
    def get_index(self):
        return self.position_index
    
    def check_playable_card(self, card, discard_pile):
        if len(discard_pile) == 0:
            #print("No cards in play, all cards valid")
            return True
        elif card.get_color() == discard_pile[0].get_color():
            #print("color match, card is playable")
            return True
        elif card.get_value() == discard_pile[0].get_value():
            #print("value match, card is playable")
            return True
        #print("card not playable")
        return False
    
class AIPlayer(Player):
    
    def say_uno(self):
        pass
    
    # def play_card(self, card):
    #     pass
    
    
 