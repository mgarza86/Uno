import random
from .card import *

class Deck():
    COLOR_TUPLE = ('blue', 'green', 'red', 'yellow')
    
    STANDARD_DICT = {'1':1, '2':2,'3': 3,'4':4,'5':5,
                     '6':6,'7':7,'8':8,'9':9,'skip':'skip',
                     'reverse':'reverse','picker':'picker'}
    
    def __init__(self, window=None, card_dict = STANDARD_DICT):
        self.starting_deck = []
        
        for color in Deck.COLOR_TUPLE:
            o_card = Card(window, color, '0')
            self.starting_deck.append(o_card)
        
            for key, value in card_dict.items():
                for _ in range(2):
                    if key == 'skip':
                        o_card = Skip(window, color, key)
                        self.starting_deck.append(o_card)
                    elif key == 'reverse':
                        o_card = Reverse(window, color, key)
                        self.starting_deck.append(o_card)
                    elif key == 'picker':
                        o_card = DrawTwoCard(window, color, key)
                        self.starting_deck.append(o_card)
                    else:
                        o_card = Card(window, color, key)
                        self.starting_deck.append(o_card)
                        
        for _ in range(4):
            o_card = WildChanger(window, 'black', 'wild')
            self.starting_deck.append(o_card)
            o_card = WildPickFour(window, 'black', 'pickfour')
            self.starting_deck.append(o_card)
        
    
    def shuffle(self):
        for o_card in self.starting_deck:
            o_card.conceal()
        random.shuffle(self.starting_deck)
        
    def get_card(self):
        if len(self.starting_deck) == 0:
            raise IndexError('No more cards in the deck')
        return self.starting_deck.pop()
    
    def return_card_to_deck(self, o_card):
        self.starting_deck.append(o_card)  
        
    def print_deck(self):
        print(len(self.starting_deck), ' cards in the deck')
        for o_card in self.starting_deck:
            print('Name: ', o_card.get_name(), '  Value:', o_card.get_value())
        