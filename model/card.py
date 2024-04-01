import pygame
import pygwidgets
import os
from abc import ABC, abstractmethod

class Card():
    
    BACK_OF_CARD = pygame.image.load('./images/card_back_alt.png')
    
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.card_name = f"{self.color}_{self.value}"
        
    def __str__(self):
        return f"{self.color} {self.value}"

    def __repr__(self):
        return f"Card('{self.color}', {self.value},{self.card_name})"
    
    def perform_action(self):
        pass
        
    def get_color(self):
        return self.color
    
    def get_value(self):
        return self.value
    
    def get_name(self):
        return self.card_name

        
    
        
    
class WildChanger(Card):
    
    WILD_CARD = pygame.image.load('./images/black_wild.png')
    
    def __init__(self, window, color, value) -> None:
        super().__init__(window, color, value)
        self.images = pygwidgets.ImageCollection(window, (0,0), {'front': WildChanger.WILD_CARD, 'back': Card.BACK_OF_CARD}, 'back')
        
    def pick_color(self, color):
        self.value = None
        self.color = color
        

class WildPickFour(WildChanger):
    
    WILD_PICK_FOUR = pygame.image.load('./images/black_pickfour.png')
    
    def __init__(self, window, color, value) -> None:
        super().__init__(window, color, value)
        self.images = pygwidgets.ImageCollection(window, (0,0), 
                                                 {'front': WildPickFour.WILD_PICK_FOUR, 
                                                  'back': Card.BACK_OF_CARD}, 'back')
        
    def perform_action(self, game):
        victim_index =  game.current_player_index + game.current_direction
        
        
        if game.check_direction() == 1 and victim_index >= len(game.players_list):
            victim_index = 0
        elif game.check_direction() == -1 and victim_index < 0:
            victim_index = len(game.players_list) -1
            
        game.players_list[victim_index].draw_card(game.draw_pile)
        game.players_list[victim_index].draw_card(game.draw_pile)
        game.players_list[victim_index].draw_card(game.draw_pile)
        game.players_list[victim_index].draw_card(game.draw_pile)

class Skip(Card):
        
    def perform_action(self, game):
        game.determine_next_player(skip=True)

class DrawTwoCard(Card):
        
    def perform_action(self, game):
        victim_index =  game.current_player_index + game.current_direction
        
        
        if game.check_direction() == 1 and victim_index >= len(game.players_list):
            victim_index = 0
        elif game.check_direction() == -1 and victim_index < 0:
            victim_index = len(game.players_list) -1
        
        
        game.players_list[victim_index].draw_card(game.draw_pile)
        game.players_list[victim_index].draw_card(game.draw_pile)
class Reverse(Card):
        
    def perform_action(self, game):
        game.change_direction()