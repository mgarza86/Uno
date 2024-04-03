import json

class Player():
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"Player('{self.name}')"
        
    def draw_card(self, deck):
        print(self.get_name(), "drew a card")
        self.hand.append(deck.draw())
     
    def play_card(self, card):
        for cards in self.hand:
            if cards.get_name() == card.get_name():
                card_index = self.hand.index(cards)
                self.hand.append(self.hand.pop(card_index))

        return self.hand.pop()   
    
    def get_name(self):
        return self.name
    
    def check_conditions(self, card, color, value):
        if color == "":
            return True
        elif color == "black":
            return True
        elif card.get_color() == "black":
            return True
        elif card.get_color() == color:  
            return True
        elif card.get_value() == value: 
            return True
        return False

    