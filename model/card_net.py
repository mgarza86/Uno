import json
import pygwidgets
class Card():
    
    def __init__(self, color, value, window=None, filename=None):
        self.color = color
        self.value = str(value)
        self.card_name = f"{self.color}_{self.value}"
        
        if file_name is None:
            file_name = './images/' + self.card_name + '.png'
        
        if window is not None:
            self.images = pygwidgets.ImageCollection(window, (0,0), {'front': file_name}, 'back')
        
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
    
    def disable(self):
        self.images.disable()
    
    def enable(self):
        self.images.enable()
        
    def get_location(self):
        return self.images.getLoc()
    
    def set_location(self, location):
        self.images.setLoc(location)
    
    def set_centered_location(self, location):
        self.images.setCenteredLoc(location)
    
    def draw(self):
        self.images.draw()
    
    def rotate_card(self, angle):
        self.images.rotateTo(angle)
    
    def set_scale(self, scale, scaleFromCenter=False):
        self.images.scale(scale, scaleFromCenter)
        
    def get_rect(self):
        return self.images.getRect()
    
    def get_collide_point(self,mouse_x, mouse_y):
        return self.images.getRect().collidepoint(mouse_x, mouse_y)
    
    def get_size(self):
        return self.images.getSize()

    def move_x(self, pixels):
        self.images.moveX(pixels)
    
    def handle_event(self, event):
        if self.images.handleEvent(event):
            return True
        else:
            return False

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
            print(len(game.players))       
            if len(game.players) == 2:
                game.determine_next_player(skip=True)
            else:
                game.change_direction()
        elif online:
            if len(game.players) == 2:
                game.determine_next_player(skip=True)
            else:
                game.change_direction()
