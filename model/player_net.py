import json
import uuid

class Player():
    def __init__(self, name, client_id=None):
        self.name = name
        self.hand = []
        self.angle = 0
        self.location = (0,0)
        self.client_id = client_id
    
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
    
    def get_client_id(self):
        return self.client_id
    
    def get_name(self):
        return self.name
    
    def check_conditions(self, card, color, value):
        print(f"parameters passed: card: {card} color: {color} value: {value}")
        print(f"card color: {card.get_color()} card value: {card.get_value()}")
        card_color = card.get_color().strip().lower()
        input_color = color.strip().lower()
        print(f"Comparing card color: '{card_color}' with input color: '{input_color}'")
        print(f"Data types - card color: {type(card_color)}, input color: {type(input_color)}")

        if color == "":
            print("No color condition, therefore true")
            return True
        elif color == "black":
            print("Black condition, therefore wild and true")
            return True
        elif card.get_color() == "black":
            print("Card color is black, therefore wild and true")
            return True
        elif card_color == input_color:

            print("Color match, therefore true")
            return True
        elif card.get_value() == value: 
            print("Value match, therefore true")
            return True
        else:
            print(f"card types: color {type(card.get_color())}; value {type(card.get_value())}")
            print(f"parameter types: color {type(color)}; value {type(value)}")
            print("No match, therefore false")
            return False
    
    def to_dict(self, include_hand=False):
        player_dict = {
            'name': self.name,
        }
        if include_hand:
            player_dict['hand'] = [card.to_dict() for card in self.hand]
        return player_dict

    def to_json(self, include_hand=False):
        return json.dumps(self.to_dict(include_hand=include_hand))
    
    def get_card_count(self):
        return len(self.hand)