import random
from model.card import *

class CardFactory:
    @staticmethod
    def create_card(card_type, color, value):
        if card_type == 'wild':
            return WildChanger(color, value)
        elif card_type == 'draw_four':
            return WildPickFour(color, value)
        elif card_type == 'skip':
            return Skip(color, value)
        elif card_type == 'draw_two':
            return DrawTwoCard(color, value)
        else:
            return Card(color, value)
        
class Deck:
    COLOR_TUPLE = ('red', 'green', 'blue', 'yellow')
    STANDARD_DICT = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'skip': 'skip', 'reverse': 'reverse', 'picker': 'picker'}
    
    def __init__(self, card_dict=STANDARD_DICT):
        self.starting_deck = []
        self.build_deck(card_dict)
        
        
    def build_deck(self, card_dict):
        for color in Deck.COLOR_TUPLE:
            self.starting_deck.append(CardFactory.create_card('default', color, '0'))
            for value, count in card_dict.items():
                card_type = 'default' if value.isdigit() else value
                for _ in range(2 if value != '0' else 1):
                    self.starting_deck.append(CardFactory.create_card(card_type, color, value))
        for _ in range(4):
            self.starting_deck.append(CardFactory.create_card('wild', 'black', 'wild'))
            self.starting_deck.append(CardFactory.create_card('pickfour', 'black', 'pickfour'))
                
    def shuffle(self):
        random.shuffle(self.starting_deck)
        random.shuffle(self.starting_deck)
        random.shuffle(self.starting_deck)
        
    def get_card(self):
        return self.starting_deck.pop()