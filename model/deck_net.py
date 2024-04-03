import random
from card_net import *

class CardFactory:
    @staticmethod
    def create_card(card_type, color, value):
        if card_type == 'normal':
            return Card(color, value)
        elif card_type == 'wild_pickfour':
            return WildPickFour(color, value)
        elif card_type == 'wild_changer':
            return WildChanger(color, value)
        elif card_type == 'skip':
            return Skip(color, value)
        elif card_type == 'reverse':
            return Reverse(color, value)
        elif card_type == 'draw_two':
            return DrawTwoCard(color, value)
        
class Deck:
    COLOR_TUPLE = ('red', 'blue', 'green', 'yellow')
    STANDARD_DICT = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'skip': 'skip', 'reverse': 'reverse', 'picker': 'picker'}
    
    def __init__(self):
        self.cards = self._create_uno_deck()
    
    def _create_uno_deck(self):
        self.cards = []
        
        for color in Deck.COLOR_TUPLE:
            self.cards.append(CardFactory.create_card('normal', color, 0))
            
            
            for key, value in Deck.STANDARD_DICT.items():
                for _ in range(2):               
                    if key == 'skip':
                        self.cards.append(CardFactory.create_card('skip', color, key))
                    elif key == 'reverse':
                        self.cards.append(CardFactory.create_card('reverse', color, key))
                    elif key == 'picker':
                        self.cards.append(CardFactory.create_card('draw_two', color, key))
                    else:
                        self.cards.append(CardFactory.create_card('normal', color, key))
        
        for _ in range(4):
            self.cards.append(CardFactory.create_card('wild_changer', 'black', 'wild'))
            self.cards.append(CardFactory.create_card('wild_pickfour', 'black', 'pickfour'))
            
        return self.cards
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    def draw_card(self):
        return self.cards.pop() if self.cards else None
    
    def __len__(self):
        return len(self.cards)
    
    def print_deck(self):
        for card in self.cards:
            print(f"{card.card_name}")

# # Usage
# deck = Deck()
# deck.shuffle()
# deck.shuffle()
# deck.shuffle()
# deck.print_deck() 
