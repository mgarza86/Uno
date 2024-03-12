import pygame
import pygwidgets 
import pyghelpers
import model.game

X_COORDINATE, Y_COORDINATE = (0,0)

class GameBoard(pyghelpers.Scene):
    
    def __init__(self, window, game) -> None:
        self.window = window
        self.back_ground_color = (161, 59, 113)
        #self.draw_deck = game.draw_pile
        self.game = game
        self.enter()
        
        
    
    def enter(self):
        self.game.initialize_players(7)

            
    def handleInputs(self, event_list, key_pressed_list):
        for event in event_list:
            pass
    
    ''' all the components you want to draw are in the draw function'''
    def draw(self):
    
        self.window.fill(self.back_ground_color)
        self.game.draw()
        
        
            
        
    def initial_hand(self, deck):
        for _ in range(7):
            o_card = deck.get_card()
            o_card.reveal()
            self.player_hand.append(o_card)