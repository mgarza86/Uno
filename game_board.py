import pygame
import pygwidgets 
import pyghelpers
import model.game

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
        #self.player_two = self.player[1]
        
        
        self.enter()
        
        
    
    def enter(self):
        self.game.initialize_players(7)

            
    def handleInputs(self, event_list, key_pressed_list):
        for event in event_list:
            for i in range(len(self.player_one.hand)):
                if self.player_one.hand[i].handle_event(event):
                    print(self.player_one.hand[i].get_name())
    
    ''' all the components you want to draw are in the draw function'''
    def draw(self):
    
        self.window.fill(self.back_ground_color)
        self.game.draw()
        
        
    def initial_hand(self, deck):
        for _ in range(7):
            o_card = deck.get_card()
            o_card.reveal()
            self.player_hand.append(o_card)