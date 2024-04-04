import json

class Player():
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.angle = 0
        self.location = (0,0)
    
    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"Player('{self.name}')"
        
    def draw_card(self, deck):
        print(self.get_name(), "drew a card")
        self.hand.append(deck.draw_card())
     
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
    
    def to_dict(self, include_hand=False):
        player_dict = {
            'name': self.name,
        }
        if include_hand:
            # Use Card's to_dict() for each card in the hand
            player_dict['hand'] = [card.to_dict() for card in self.hand]
        return player_dict

    def to_json(self, include_hand=False):
        return json.dumps(self.to_dict(include_hand=include_hand))

    