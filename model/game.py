

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
        self.window_width, self.window_height = self.window.get_size()

        self.orientate_player()
        
                
    def initialize_players(self, number_of_cards=7):
        for o_player in self.players_list:
            for _ in range(number_of_cards):
                o_player.draw_card(self.draw_pile)
        
    def check_direction(self):
        return self.current_direction
    
    def check_hand(self, player):
        if len(self.discard_pile) == 0:
            print("No card in play yet")
            return True
        for i in range(len(player.hand)):
            if player.check_playable_card(player.hand[i], self.discard_pile):
                print("Hand has a playable card")
                return True
        print("print hand does not have a playable card, drawing card")
        player.draw_card(self.draw_pile)    
        return False
    
    def orientate_player(self):
        for i in range(len(self.players_list)):
            if i == 1:
                for card in self.players_list[i].hand:
                    card.flip_vertical()
                
    def draw(self):
        if len(self.discard_pile) != 0:
            self.discard_pile[0].set_centered_location((self.window_width/2,self.window_height/2))
            self.discard_pile[0].draw()
        
        for i in range(len(self.players_list)):
            self.players_list[i].draw()            
        
    def discard(self, discard_pile, new_card):
        discard_pile.insert(0,new_card)
        #discard_pile = discard_pile[1:] + discard_pile[:1]

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
        self.discard(self.discard_pile,player.play_card(card))
        #self.discard_pile.append(player.play_card(card))
    
    def check_last_card_played(self, discard_pile):
        print(discard_pile[0].get_name())
        return discard_pile[0]
    
    def set_current_color(self,color):
        self.current_color = color
    
    def get_player(self, index):
        return self.players_list[index]
    
    def start_game():
        pass