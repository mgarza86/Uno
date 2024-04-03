import json

class Card():
    
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.is_concealed = True
        self.card_name = f"{self.color}_{self.value}"
        
    def __str__(self):
        return f"{self.color} {self.value}"

    def __repr__(self):
        return f"Card('{self.color}', {self.value},{self.card_name})"
    
    def to_dict(self):
        return {
            'color': self.color,
            'value': self.value,
            'is_concealed': self.is_concealed,
            'card_name': self.card_name
        }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)
        
    def get_color(self):
        return self.color
    
    def get_value(self):
        return self.value
    
    def get_name(self):
        return self.card_name

class WildChanger(Card):
    
    def __init__(self, color, value) -> None:
        super().__init__( color, value)
        
    def pick_color(self, color):
        self.value = None
        self.color = color
        self.card_name = "black_wild"
        
class WildPickFour(WildChanger):
        
    def __init__(self, color, value) -> None:
        super().__init__( color, value)
        self.card_name = "black_pickfour"
        
    def perform_action(self, game):
        pass

class Skip(Card):
        
    def perform_action(self, game):
        pass

class DrawTwoCard(Card):
        
    def perform_action(self, game):
        pass
        
class Reverse(Card):
        
    def perform_action(self, game):
        pass
    
