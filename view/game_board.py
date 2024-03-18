import pygame
import pygwidgets 
import pyghelpers
import model.game
from model.player import Player, AIPlayer

X_COORDINATE, Y_COORDINATE = (0,0)

class GameBoard(pyghelpers.Scene):
    
    def __init__(self, window) -> None:
        self.window = window
        self.back_ground_color = (161, 59, 113)
        
        #self.enter()
        
    def enter(self,game):
        self.game = game
        self.game.initialize_players(7)
            
    def handleInputs(self, event_list, key_pressed_list):
        for event in event_list:
            current_player = self.game.players_list[self.game.current_player_index]
            
            if isinstance(current_player, AIPlayer):
                self.computer_move(current_player,event)            
            elif isinstance(current_player, Player):
                self.player_move(current_player,event)    
    
    def player_move(self, player, event):
        self.game.check_hand(player)
        for card in player.hand[:]:
            if card.handle_event(event):
                #if player.check_playable_card(card, self.game.discard_pile): #!change this
                if player.check_conditions(card, self.game.current_color, self.game.current_value):
                    #print(card.get_name())
                    self.game.play_card(player,card)
                    if self.game.check_game_end(player):
                        self.goToScene('end',player.get_name())
                    self.game.determine_next_player()
                    print(f"{self.game.players_list[self.game.current_player_index].get_name()}'s turn")
                    break
    
    def computer_move(self, player, event):
        if self.game.check_hand(player):
            matching_cards, color_matches, value_matches = self.find_matching_cards(player.hand, self.game.current_color, self.game.current_value)
            if matching_cards:  # Check if matching_cards is not empty
                self.game.play_card(player, matching_cards[0])
                if self.game.check_game_end(player):
                     
                    self.goToScene('end', player.get_name())
                self.game.determine_next_player()
            else:
                #! AI can't play anything after black is played. FIX LATER
                print(player.get_name(), ": No matching cards found. Drawing a card.")
                self.game.determine_next_player()
        else:
            self.game.determine_next_player()
    
    def find_matching_cards(self, hand, color, value):
        color_matches = {'red':0,'blue':0,'yellow':0,'green':0, 'black': 0}
        value_matches = 0 
        matching_cards= []
        
        for card in hand:
            if card.get_color() == self.game.current_color:
                color_matches[card.get_color()] += 1
                matching_cards.append(card)
            elif card.get_value() == self.game.current_value:
                value_matches += 1
                if card not in matching_cards:
                    matching_cards.append(card)
                    
        return matching_cards, color_matches, value_matches
    
    def draw(self):
        self.window.fill(self.back_ground_color)
        self.game.draw()
        
    def print_matching_cards(self, matching_cards):
        for card in matching_cards:
            print(card.get_name())    
