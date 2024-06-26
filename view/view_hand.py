import pygame
import pygwidgets
from model.card_factory import CardFactory  

class ViewHand:
    def __init__(self, window, hand_data):
        self.window = window
        self.cards = []
        self.load_hand(hand_data)

    def __str__(self) -> str:
        return f"Hand: {self.hand_string()}"
    
    def hand_string(self):
        return ', '.join([str(card) for card in self.cards])
    
    def load_hand(self, hand_data):
        ''' Parse the hand data and creates card objects'''
        self.cards = []
        
        if 'hand' in hand_data and isinstance(hand_data['hand'], list):
            for card_data in hand_data['hand']:
                card = self.create_card_from_json(card_data)
                self.cards.append(card)

    def remove(self, card):
        ''' Remove a card from the hand '''
        self.cards.remove(card)
    
    def update(self, hand_data):
        ''' Update the hand with new data '''
        self.load_hand(hand_data)

    def create_card_from_json(self, card_data):
        '''Determine the type of card to create based on card_data'''
        return CardFactory.create_card(self.window, card_data['color'], card_data['value'])

    def draw(self):
        '''Draw all the cards in the hand'''
        mouse_x, mouse_y = pygame.mouse.get_pos()
        overlap_amount = 30
        hovered_index = None

        # Determine the hovered card index (check in reverse order)
        for i in range(len(self.cards) - 1, -1, -1):
            card = self.cards[i]
            if card.get_collide_point(mouse_x, mouse_y):
                hovered_index = i
                break  # Stop checking once the topmost hovered card is found

        # Draw all non-hovered cards
        for i, card in enumerate(self.cards):
            if i != hovered_index:
                if i == 0:
                    card_location = self.set_card_on_center(card)
                else:
                    card_location = self.next_card_location(self.cards[i-1], overlap_amount)
                card.set_location(card_location)
                card.reveal()
                card.set_scale(60)
                card.disable()
                card.draw()

        # Draw the hovered card last to make it appear on top
        if hovered_index is not None:
            self.cards[hovered_index].enable()
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
    
    