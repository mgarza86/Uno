import pygame
import pygwidgets
from model.card import Card

class Opponent_card(Card):
    BACK_OF_CARD = pygame.image.load('./images/card_back_alt.png')
    def __init__(self, window):
        self.window = window
        self.images = pygwidgets.ImageCollection(window, (0,0), {'back': Opponent_card.BACK_OF_CARD}, 'back')

class ViewOpponent:
        def __init__(self, window, initial_data=None):
            self.window = window
            self.opponents = {}
                    
        def update_opponent(self, data):
            ''' Helper function to update the opponent data from the server '''
            self.opponents={}
            for entry in data.split(';'):
                name, count = entry.split(',')
                self.opponents[name] = [Opponent_card(self.window) for _ in range(int(count))]

        def calculate_hand_widths(self, overlap_amount=80):
            ''' Calculate the width of each opponent's hand based on the number of cards and overlap amount '''
            hand_widths = {}
            for name, cards in self.opponents.items():
               if not cards:
                   hand_widths[name] = 0
               else:
                   card_width = cards[0].get_size()[0]
                   hand_width = card_width + (len(cards) - 1) * (card_width - overlap_amount)
                   hand_widths[name] = hand_width
                   return hand_widths 
        
        def adjust_first_card_position(self, opponent_name, overlap_amount=80, position='top'):
            ''' Adjust the position of the first card '''
            hand_widths = self.calculate_hand_widths(overlap_amount)
            hand_width = hand_widths.get(opponent_name, 0)
            
            window_width, window_height = self.window.get_size()
            
            if position in ['top', 'bottom']:
                # Center horizontally
                first_card_x = (window_width - hand_width) // 2
                if position == 'top':
                    first_card_y = 0  # Adjust this value for padding from the edge
                else:  # 'bottom'
                    first_card_y = window_height - self.card.images.getSize()[1] 
                
            elif position in ['left', 'right']:
                # Center vertically
                first_card_y = (window_height - hand_width) // 2  # Here, hand_width is used vertically
                if position == 'left':
                    first_card_x = 0  # Adjust this value for padding from the edge
                else:  
                    first_card_x = window_width - self.card.images.getSize()[0]  
            
            return first_card_x, first_card_y
   
        def next_card_location(self, previous_card_position, card_size, overlap=50, vertical=False):
            ''' Calculate the position of the next card based on the previous card's position and size '''
            if vertical:
                new_y_coordinate = previous_card_position[1] + card_size[1] - overlap
                return (previous_card_position[0], new_y_coordinate)
            else:
                new_x_coordinate = previous_card_position[0] + card_size[0] - overlap
                return (new_x_coordinate, previous_card_position[1])
     
        def set_card_on_center(self, opponent_name, overlap_amount=80, position='bottom'):
            ''' Set the first card of the opponent's hand at the center of the window '''
            window_width, window_height = self.window.get_size()
            hand_widths = self.calculate_hand_widths(overlap_amount)
            hand_width = hand_widths.get(opponent_name, 0)

            template_card = next(iter(next(iter(self.opponents.values()), [])), None)
            if not template_card:
                return (0, 0)  

            card_size = template_card.images.getSize()

            if position == 'bottom':
                x = (window_width - hand_width) // 2
                y = window_height - card_size[1]
            elif position == 'right':
                x = window_width - card_size[0]
                y = (window_height - hand_width) // 2
            elif position == 'top':
                x = (window_width - hand_width) // 2
                y = 0
            elif position == 'left':
                x = 0
                y = (window_height - hand_width) // 2
            return (x, y)

        def get_window_edges(self):
            # Divide window into sections based on number of opponents
            window_width, window_height = self.window.get_size()
            card_width, card_height = self.card.get_size()
            edges = [
                (window_width // 2, 0),  
                (0, window_height // 2),  
                (window_width // 2, window_height - card_height),  
                (window_width - card_width, window_height // 2),  
            ]
            return edges[:len(self.opponents)]
        
        def draw(self):
            ''' Draw the opponents' cards on the screen '''
            number_of_opponents = len(self.opponents)
            
            if number_of_opponents == 3:
                opponent_positions = ['right', 'top', 'left']
            elif number_of_opponents == 2:
                opponent_positions = ['top', 'right']
            else:
                opponent_positions = ['top']
            
            overlap_amount = 70  
            
            for opponent_name, cards in self.opponents.items():
                if not cards:
                    continue 
                
                # Determine the position for this opponent based on their name or index
                position_index = list(self.opponents.keys()).index(opponent_name)
                position = opponent_positions[position_index % len(opponent_positions)]
                
                first_card_pos = self.set_card_on_center(opponent_name, overlap_amount, position)
                for i, card in enumerate(cards):
                    if i == 0:
                        card_position = first_card_pos
                    else:
                        previous_card_position = cards[i - 1].get_location()
                        card_size = cards[i - 1].get_size()
                        card_position = self.next_card_location(previous_card_position, card_size, overlap_amount, vertical=(position in ['left', 'right']))
                    
                    card.set_location(card_position)
                    if position == 'top':
                        card.rotate_card(180)  
                    elif position == 'right':
                        card.rotate_card(270)
                    elif position == 'left':
                        card.rotate_card(90)
                        
                    card.set_scale(60)
                    card.draw()