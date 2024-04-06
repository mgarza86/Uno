from model.card_net import *

class Game():
    def __init__(self,  players, deck) -> None:
        self.players = players
        self.discard_pile= []
        self.draw_pile = deck
        self.current_direction = 1
        self.current_color = ""
        self.current_value = ""
        self.current_player_index = 0
                
    def initialize_players(self, number_of_cards=7):
        #self.rotate_player_hands(self.players)
        for o_player in self.players:
            for _ in range(number_of_cards):
                o_player.draw_card(self.draw_pile)
            #o_player.initialize_card_positions()
        
    def check_direction(self):
        return self.current_direction
    
    def check_hand(self, player):
        if len(self.discard_pile) == 0:
            print("No card in play yet")
            return True
        for i in range(len(player.hand)):
            if player.check_conditions(player.hand[i],self.current_color, self.current_value):
                return True
            
        return False
        
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
        self.current_player_index %= len(self.players)
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
        if isinstance(card,WildPickFour):
            card.perform_action(self)
    
    def check_last_card_played(self, discard_pile):
        return discard_pile[0]
    
    def set_current_color(self,color):
        self.current_color = color
    
    def get_player(self, index):
        return self.players[index]

    def game_state_to_dict(self):
        return {
            "players": [player.name for player in self.players],  # List of player names
            "current_direction": self.current_direction,
            "current_color": self.current_color,
            "current_value": self.current_value,
            "current_player_index": self.current_player_index,
            "current_player": self.players[self.current_player_index].name,
            "next_player": self.players[(self.current_player_index + self.current_direction) % 
                                        len(self.players)].name,
        }
        
    def game_state_to_json(self):
        return json.dumps(self.game_state_to_dict(), sort_keys=True, indent=4)
    
    def players_hand_to_dict(self):
        return {player.name: player.hand_to_dict() for player in self.players}
    
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    