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
        return {"color": self.color, "value": self.value}

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
        
    def perform_action(self, game, online=False):
        victim_index =  game.current_player_index + game.current_direction
        if game.check_direction() == 1 and victim_index >= len(game.players):
            victim_index = 0
        elif game.check_direction() == -1 and victim_index < 0:
            victim_index = len(game.players) -1
        if not online:
            game.players[victim_index].draw_card(game.draw_pile)
            game.players[victim_index].draw_card(game.draw_pile)
            game.players[victim_index].draw_card(game.draw_pile)
            game.players[victim_index].draw_card(game.draw_pile)
        else:
            return victim_index
        

class Skip(Card):
        
    def perform_action(self, game, online=False):
        if not online:
            game.determine_next_player(skip=True)
        else:
            print("Skip card played, handling on server side.")

class DrawTwoCard(Card):
        
    def perform_action(self, game, online=False):
        victim_index =  game.current_player_index + game.current_direction
        if game.check_direction() == 1 and victim_index >= len(game.players):
            victim_index = 0
        elif game.check_direction() == -1 and victim_index < 0:
            victim_index = len(game.players) -1
        print(f"Online is {online}")
        if not online:
            print("SOMETHING WENT HORRIBLY WRONG")
            game.players[victim_index].draw_card(game.draw_pile)
            game.players[victim_index].draw_card(game.draw_pile)
        else:
            return victim_index
        
class Reverse(Card):
        
    def perform_action(self, game, online=False):
        if not online:        
            if len(game.players) == 2:
                game.determine_next_player(skip=True)
            else:
                game.change_direction()
        else:
            print("Reverse card played, handling on server side.")
