

class Game():
    def __init__(self,window,  players, deck) -> None:
        self.window = window
        self.players_list = players
        self.discard_pile= []
        self.draw_pile = deck
        self.current_direction = 1
        self.current_color = ""
        self.current_value = ""
        self.current_player_index = 0
        self.orientate_player()
        
                
    def initialize_players(self, number_of_cards=7):
        for o_player in self.players_list:
            for _ in range(number_of_cards):
                o_player.draw_card(self.draw_pile)
        
    def check_direction(self):
        return self.current_direction
    
    def orientate_player(self):
        for i in range(len(self.players_list)):
            if i == 1:
                for card in self.players_list[i].hand:
                    card.flip_vertical()
                
    def draw(self):
        for i in range(len(self.players_list)):
            self.players_list[i].draw()            
        
        
    def change_direction(self):
        self.check_direction *= -1
    
    def check_game_end(self, player):
        if len(player.hand) == 0:
            return True
        else:
            return False
    
    def determine_next_player(self):
        self.current_player_index += self.current_direction
        if  self.current_direction == 1 and self.current_player_index >= len(self.players_list):
            self.current_player_index = 0
            return self.current_player_index
        elif self.current_direction == -1 and self.current_player_index < 0:
            self.current_player_index = len(self.players_list) - 1
            return self. current_player_index
        return self.current_player_index
    
    def play_card(self,player,card):
        self.discard_pile.append(player.play_card(card))
        
    
    def check_last_card_played(self, discard_pile):
        print(discard_pile[0].get_name())
        return discard_pile[0]
    
    def set_current_color(self,color):
        self.current_color = color
    
    def get_player(self, index):
        return self.players_list[index]
    
    def start_game():
        pass