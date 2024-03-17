from model.card import *

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
                
    def initialize_players(self, number_of_cards=7):
        self.rotate_player_hands(self.players_list)
        for o_player in self.players_list:
            for _ in range(number_of_cards):
                o_player.draw_card(self.draw_pile)
            o_player.initialize_card_positions()
        
    def check_direction(self):
        return self.current_direction
    
    def check_hand(self, player):
        if len(self.discard_pile) == 0:
            print("No card in play yet")
            return True
        for i in range(len(player.hand)):
            if player.check_conditions(player.hand[i],self.current_color, self.current_value):
                return True
        player.draw_card(self.draw_pile)
        #print(player, " drew a card")    
        return False
    
    def orientate_player(self):
        for i in range(len(self.players_list)):
            if i == 1:
                for card in self.players_list[i].hand:
                    card.flip_vertical()
    
    def rotate_player_hands(self, players):
        num_players = len(players)
        
        # For two players
        if num_players == 2:
            # Apply 180 degrees rotation to the second player's hand
            players[1].set_angle(180)
            players[1].rotate_hand(180)
            
        # For three players
        elif num_players == 3:
            players[1].set_angle(90)
            players[2].set_angle(180)
            
        # For four players
        elif num_players == 4:
            players[1].set_angle(90)
            players[2].set_angle(180)
            players[3].set_angle(270)
                
    def draw(self):
        if len(self.discard_pile) != 0:
            self.discard_pile[0].set_centered_location((self.window_width/2,self.window_height/2))
            self.discard_pile[0].draw()
        
        for i in range(len(self.players_list)):
            self.players_list[i].draw()            
        
    def discard(self, discard_pile, new_card):
        discard_pile.insert(0,new_card)

    def change_direction(self):
        self.current_direction *= -1
    
    def check_game_end(self, player):
        if len(player.hand) == 0:
            for card in self.discard_pile:
                        print(card)
            return True
        else:
            return False
    
    def determine_next_player(self, skip=False):
        
        self.current_player_index += self.current_direction
        self.current_player_index %= len(self.players_list)
        return self.current_player_index
    
    def play_card(self,player,card):
        print(player.get_name(), " played: ", card.get_name() )
        self.discard(self.discard_pile,player.play_card(card))
        self.discard_pile[0].reveal()
        self.current_color = card.get_color()
        self.current_value = card.get_value()
        if isinstance(card,Skip):
            card.perform_action(self)
        if isinstance(card,DrawTwoCard):
            card.perform_action(self)
        if isinstance(card,Reverse):
            card.perform_action(self)
    
    def check_last_card_played(self, discard_pile):
        #print(discard_pile[0].get_name())
        return discard_pile[0]
    
    def set_current_color(self,color):
        self.current_color = color
    
    def get_player(self, index):
        return self.players_list[index]
    
    def start_game():
        pass