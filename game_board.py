import pygame
import pygwidgets 
import pyghelpers
import model.game
from model.player import Player, AIPlayer

X_COORDINATE, Y_COORDINATE = (0,0)

class GameBoard(pyghelpers.Scene):
    
    def __init__(self, window, game) -> None:
        self.window = window
        self.back_ground_color = (161, 59, 113)
        self.game = game
        self.player = self.game.players_list
        self.discard_pile = self.game.discard_pile
        self.draw_pile = self.game.draw_pile
        self.current_color = self.game.current_color
        self.current_value = self.game.current_value
        self.current_direction = self.game.current_direction
        self.player_one = self.player[0]
        self.player_two = self.player[1]
        self.current_index = game.current_player_index
        self.enter()
        self.player_two.rotate_hand(180)
        self.player_one.scale_hand(50)
        
    def enter(self):
        self.game.initialize_players(7)
            
    def handleInputs(self, event_list, key_pressed_list):
        for event in event_list:
            current_player = self.player[self.current_index]
            print(current_player.get_player_name(), "'s turn ")
            if isinstance(current_player, AIPlayer):
                print("Player 2 move!!!")
                self.computer_move(current_player,event)            
            elif isinstance(current_player, Player):
                self.player_move(current_player,event)    
    
    def player_move(self, player, event):
        self.game.check_hand(player)
        for card in player.hand[:]:
            if card.handle_event(event):
                if player.check_playable_card(card, self.discard_pile):
                    print(card.get_name())
                    self.game.play_card(player,card)
                    self.current_index = self.game.determine_next_player()
                    
                    break
    
    def computer_move(self, player, event):
        if self.game.check_hand(player):
            pass
        else:
            self.current_index = self.game.determine_next_player()
        
    
    def draw(self):
    
        self.window.fill(self.back_ground_color)
        self.game.draw()
        
        
    def initial_hand(self, deck):
        for _ in range(7):
            o_card = deck.get_card()
            o_card.reveal()
            self.player_hand.append(o_card)