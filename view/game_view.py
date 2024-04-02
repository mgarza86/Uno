import pygame
import pygwidgets

class GameView():
    def __init__(self, window) -> None:
        pass
    
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