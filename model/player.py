import pygame
import pygwidgets

from model.card import Card
from model.deck import Deck
class Player():
    def __init__(self, window ,name) -> None:
        self.window = window
        self.name = name
        self.hand = []
        self.angle = 0
        self.location = (0,0)
        
    def draw_card(self, game_deck):
        self.hand.append(game_deck.get_card())
     
    def play_card(self, card):
        for cards in self.hand:
            if cards.get_name() == card.get_name():
                card_index = self.hand.index(cards)
                self.hand.append(self.hand.pop(card_index))

        return self.hand.pop()   
    
    def get_name(self):
        return self.name
    
    def get_index(self):
        return self.position_index
    
    def check_playable_card(self, card, discard_pile):
        if len(discard_pile) == 0:
            #print("No cards in play, all cards valid")
            return True
        elif card.get_color() == discard_pile[0].get_color():
            #print("color match, card is playable")
            return True
        elif card.get_value() == discard_pile[0].get_value():
            #print("value match, card is playable")
            return True
        #print("card not playable")
        return False
    
    def set_rotation(self, angle):
        self.angle = angle
    
    def rotate_hand(self, angle):
        for i in range(len(self.hand)):
            self.hand[i].rotate_card(angle)
        self.angle = angle
    
    def scale_hand(self, scale):
        for i in range(len(self.hand)):
            self.hand[i].scale_card(scale)
   
    def draw(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        overlap_amount = 60
        hovered_index = None

        for i, card in enumerate(self.hand):
            if card.get_collide_point(mouse_x, mouse_y):
                hovered_index = i
                break  # Found the hovered card

        # Draw all cards except the hovered one
        for i, card in enumerate(self.hand):
            if i != hovered_index:
                if i == 0:
                    card_location = self.set_card_on_corner(card)
                else:
                    card_location = self.next_card_location(self.hand[i-1], overlap=overlap_amount)
                card.set_location(card_location)
                card.reveal()
                card.draw()

        # Draw the hovered card last so it appears on top
        if hovered_index is not None:
            hovered_card = self.hand[hovered_index]
            hovered_card.draw()  # Assuming location was already set
    
    def initialize_card_positions(self):
        for i, card in enumerate(self.hand):
            if i == 0:
                card_location = self.set_card_on_corner(card)
            else:
                card_location = self.next_card_location(self.hand[i-1], overlap=50)
            card.set_location(card_location)
            
    def next_card_location(self, card, overlap=50):
        card_rect = card.get_rect()
        new_x_coordinate = card_rect.x + card_rect.width - overlap
        return (new_x_coordinate, card_rect.y)   
            
    def set_card_on_corner(self,card):
        window_width, window_height = self.window.get_size()
        image_width, image_height = card.get_size()
        if self.angle == 0:
            return (0, window_height - image_height)
        elif self.angle == 90:    
            return (window_width - image_width, window_height - image_height)
        elif self.angle == 180:
            return (0,0)
        elif self.angle == 270:
            return (window_width - image_width, 0)
    
    def check_conditions(self, card, color, value):
        if color == "":
            return True
        elif card.get_color() == color:  # Fixed: added parentheses to call the method
            return True
        elif card.get_value() == value:  # Fixed: added parentheses to call the method
            return True
        return False

    
class AIPlayer(Player):
    
    def say_uno(self):
        pass
    
    # def play_card(self, card):
    #     pass
    
    
 