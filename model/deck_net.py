import random
from model.card_net import *
from collections import Counter

class CardFactory:
    
    @staticmethod
    def create_card(color, value):
        if value == 'pickfour':
            return WildPickFour(color, value)
        elif value == 'wild':
            return WildChanger(color, value)
        elif value == 'skip':
            return Skip(color, value)
        elif value == 'reverse':
            return Reverse(color, value)
        elif value == 'picker':
            return DrawTwoCard(color, value)
        else:
            return Card(color, value)
        
class Deck:
    COLOR_TUPLE = ('red', 'blue', 'green', 'yellow')
    STANDARD_DICT = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
                     '9': 9, 'skip': 'skip', 'reverse': 'reverse', 'picker': 'picker'}
    
    def __init__(self):
        self.cards = self._create_uno_deck()
    
    def _create_uno_deck(self):
        self.cards = []
        
        for color in Deck.COLOR_TUPLE:
            self.cards.append(CardFactory.create_card(color, 0))
            
            
            for key, value in Deck.STANDARD_DICT.items():
                for _ in range(2):               
                    if key == 'skip':
                        self.cards.append(CardFactory.create_card(color, key))
                    elif key == 'reverse':
                        self.cards.append(CardFactory.create_card(color, key))
                    elif key == 'picker':
                        self.cards.append(CardFactory.create_card(color, key))
                    else:
                        self.cards.append(CardFactory.create_card(color, key))
        
        for _ in range(4):
            self.cards.append(CardFactory.create_card('black', 'wild'))
            self.cards.append(CardFactory.create_card('black', 'pickfour'))
            
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
class NormalCardDeck(Deck):
    def _create_uno_deck(self):
        self.cards = []
        for color in self.COLOR_TUPLE:
            # Includes only number cards
            for number in range(1, 10):  # Excluding 0 for simplicity
                self.cards.append(CardFactory.create_card(color, str(number)))
                self.cards.append(CardFactory.create_card(color, str(number)))
        return self.cards

class SpecialCardDeck(Deck):
    def _create_uno_deck(self):
        self.cards = []
        for color in self.COLOR_TUPLE:
            # Increase the frequency of special cards
            for _ in range(3):  # Increasing the count of special cards
                self.cards.append(CardFactory.create_card(color, 'skip'))
                self.cards.append(CardFactory.create_card(color, 'reverse'))
                self.cards.append(CardFactory.create_card(color, 'picker'))
        for _ in range(12):  # More wild and pick four cards
            self.cards.append(CardFactory.create_card('black', 'wild'))
            self.cards.append(CardFactory.create_card('black', 'pickfour'))
        return self.cards

class CustomMixDeck(Deck):
    def __init__(self, num_normal, num_special):
        self.num_normal = num_normal
        self.num_special = num_special
        super().__init__()

    def _create_uno_deck(self):
        self.cards = []
        for color in self.COLOR_TUPLE:
            for _ in range(self.num_normal):
                number = random.randint(1, 9)
                self.cards.append(CardFactory.create_card(color, str(number)))
            for _ in range(self.num_special):
                special_type = random.choice(['skip', 'reverse', 'picker'])
                self.cards.append(CardFactory.create_card(color, special_type))
        for _ in range(self.num_special):  # Assuming an equal number of wild cards
            self.cards.append(CardFactory.create_card('black', 'wild'))
            self.cards.append(CardFactory.create_card('black', 'pickfour'))
        return self.cards

# Usage Example
# normal_deck = NormalCardDeck()
# special_deck = SpecialCardDeck()
# custom_deck = CustomMixDeck(num_normal=5, num_special=2)