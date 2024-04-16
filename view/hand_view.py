import pygame
import pygwidgets
from model.card_factory import CardFactory  

class HandView:
    def __init__(self, window, hand_data):
        self.window = window
        self.cards = []
        self.load_hand(hand_data)

    def load_hand(self, hand_data):
        ''' Parse the hand data and creates card objects'''
        self.cards = []
        
        if 'hand' in hand_data and isinstance(hand_data['hand'], list):
            for card_data in hand_data['hand']:
                card = self.create_card_from_json(card_data)
                self.cards.append(card)
        # for card_data in hand_data['hand']:
        #     card = self.create_card_from_json(card_data)
        #     self.cards.append(card)

    def update(self, hand_data):
        ''' Update the hand with new data '''
        self.load_hand(hand_data)

    def create_card_from_json(self, card_data):
        '''Determine the type of card to create based on card_data'''
        card_type = self.get_card_type(card_data['value'])
        return CardFactory.create_card(self.window, card_type, card_data['color'], card_data['value'])
    
    @staticmethod
    def get_card_type(value):
        if value in ['wild', 'wild_pickfour']:
            return 'wild_pickfour' if value == 'wild_pickfour' else 'wild_changer'
        elif value == 'reverse':
            return 'reverse'
        elif value == 'skip':
            return 'skip'
        elif value == 'draw_two':
            return 'draw_two'
        else:
            return 'normal'

    def draw(self):
        '''Draw all the cards in the hand'''
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        overlap_amount = 30
        
        hovered_index = None
        
        for i, card in enumerate(self.cards):
            if card.get_collide_point(mouse_x, mouse_y):
                hovered_index = i
                break
            
        for i, card in enumerate(self.cards):
            if i != hovered_index:
                if i == 0:
                    card_location = self.set_card_on_center(card)
                else:
                    card_location = self.next_card_location(self.cards[i-1], overlap_amount)
                card.set_location(card_location)
                card.reveal()
                card.set_scale(60)
                card.draw()
        if hovered_index is not None:        
            self.cards[hovered_index].set_scale(60)
            self.cards[hovered_index].draw()
    
    def calculate_hand_width(self, overlap):
        if not self.cards:
            return 0
        total_width = sum([card.get_size()[0] for card in self.cards]) - overlap * (len(self.cards) - 1)
        return total_width
    
    def adjust_first_card_position(self, overlap):
        window_width, _ = self.window.get_size()
        hand_width = self.calculate_hand_width(overlap)
        first_card_x = (window_width - hand_width) // 2
        return first_card_x
    
    def set_card_on_center(self, card):
        window_width, window_height = self.window.get_size()
        image_width, image_height = card.get_size()
        
        first_card_x = self.adjust_first_card_position(30)
        return (first_card_x, window_height - image_height)
    
    def next_card_location(self, previous_card, overlap=50):
        card_rect = previous_card.get_rect()
        new_x_coordinate = card_rect.x + card_rect.width - overlap
        return (new_x_coordinate, card_rect.y)
    
    