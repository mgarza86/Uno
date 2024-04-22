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

def test_deck():
    # Create a new deck
    deck = Deck()
    #deck.shuffle()  # Shuffle the deck to simulate randomness, although not necessary for counting

    # Create a counter to track the types of cards based on their class type
    card_types = Counter()

    # Count each card type based on its class
    for card in deck.cards:
        card_types[type(card).__name__] += 1

    # Print the count of each unique card type
    for card_type, count in card_types.items():
        print(f"{card_type}: {count}")

if __name__ == "__main__":
    test_deck()