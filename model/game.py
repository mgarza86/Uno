

class Game():
    def __init__(self,  players, deck, window=None,) -> None:
        #self.window = window
        self.players_list = players
        self.discard_pile= []
        self.draw_pile = deck
        self.current_direction = 1
        self.current_color = ""
        self.current_value = ""
        
    
                
    def initialize_players(self, number_of_cards=7):
        for o_player in self.players_list:
            for _ in range(number_of_cards):
                o_player.draw_card(self.draw_pile)
        
    
    def check_direction(self):
        return self.change_direction
    
    def change_direction(self):
        if self.current_direction == 1:
            self.current_direction = -1
        else:
            self.current_direction = 1
        
    
    def check_game_end(self, player):
        if len(player.hand) == 0:
            return True
        else:
            return False
    
    def determine_next_player():
        pass
    
    def play_card(self,player,card):
        self.discard_pile.append(player.play_card(card))
        
    
    def check_last_card_played(self, discard_pile):
        print(discard_pile[0].get_name())
        return discard_pile[0]
    
    def set_current_color(self,color):
        pass
    
    def get_player(self, index):
        return self.players_list[index]
    
    def get_player_hand(self):
        return 
    
    def start_game():
        pass