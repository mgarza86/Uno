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
        print(self.get_name(), "drew a card")
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
    
    def set_angle(self, angle):
        self.angle = angle
    
    def rotate_hand(self, angle):
        for card in self.hand:
            card.rotate_card(angle)
        #self.angle = angle
    
    def scale_hand(self, scale):
        for i in range(len(self.hand)):
            self.hand[i].scale_card(scale)
   
    def draw(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if isinstance(self,AIPlayer):
            overlap_amount = 80    
        else:
            overlap_amount = 30
        hovered_index = None

        vertical_layout = self.angle == 90 or self.angle == 270

        for i, card in enumerate(self.hand):
            if card.get_collide_point(mouse_x, mouse_y):
                hovered_index = i
                break  

        for i, card in enumerate(self.hand):
            if i != hovered_index:
                if i == 0:
                    card_location = self.set_card_on_center(card)
                else:
                    card_location = self.next_card_location(self.hand[i-1], overlap=overlap_amount, vertical=vertical_layout)
                card.set_location(card_location)
                
                if isinstance(self, AIPlayer):
                    card.conceal()        
                elif isinstance(self, Player):
                    card.reveal()
                card.set_scale(60)
                card.draw()

        if hovered_index is not None:
            if vertical_layout:
                card_location = self.next_card_location(self.hand[hovered_index-1], overlap=overlap_amount, vertical=vertical_layout) if hovered_index > 0 else self.set_card_on_center(self.hand[hovered_index])
                self.hand[hovered_index].set_location(card_location)

            self.hand[hovered_index].set_scale(60)
            self.hand[hovered_index].draw()

    def calculate_hand_width(self, overlap):
        if not self.hand:
            return 0
        total_width = sum(card.get_size()[0] for card in self.hand) - overlap * (len(self.hand) - 1)
        return total_width
    
    def adjust_first_card_position(self, overlap):
        window_width, _ = self.window.get_size()
        hand_width = self.calculate_hand_width(overlap)

        first_card_x = (window_width - hand_width) / 2
        return first_card_x
    
    def initialize_card_positions(self):
        for i, card in enumerate(self.hand):
            if i == 0:
                card_location = self.set_card_on_center(card) 
            else:
                card_location = self.next_card_location(self.hand[i-1], overlap=50, vertical=(self.angle == 90 or self.angle == 270))
            card.set_location(card_location)
            
    def next_card_location(self, previous_card, overlap=50, vertical=False):
        card_rect = previous_card.get_rect()
        if vertical:
            new_y_coordinate = card_rect.y + card_rect.height - overlap
            return (card_rect.x, new_y_coordinate)
        else:
            new_x_coordinate = card_rect.x + card_rect.width - overlap
            return (new_x_coordinate, card_rect.y) 
            
    def set_card_on_center(self,card):
        window_width, window_height = self.window.get_size()
        image_width, image_height = card.get_size()
        
        # Center bottom
        if self.angle == 0:
            first_card_x = self.adjust_first_card_position(30)  # Assume overlap is 30 for player
            return (first_card_x, window_height - image_height)
        # Center right
        elif self.angle == 90:
            self.rotate_hand(90)   
            return (window_width - image_width, window_height / 2 - image_height / 2)
        # Center top
        elif self.angle == 180:
            self.rotate_hand(180)
            return (window_width / 2 - image_width / 2, 0)
        # Center left
        elif self.angle == 270:
            self.rotate_hand(270)
            return (0, window_height / 2 - image_height / 2)
    
    def check_conditions(self, card, color, value):
        if color == "":
            return True
        elif color == "black":
            return True
        elif card.get_color() == "black":
            return True
        elif card.get_color() == color:  
            return True
        elif card.get_value() == value: 
            return True
        return False

    
class AIPlayer(Player):
    
    def say_uno(self):
        pass
    
    # def play_card(self, card):
    #     pass
    
    
 