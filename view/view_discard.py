import pygame
import json
from model.card_factory import CardFactory

class ViewDiscard:
    def __init__(self, window, color, value):
        self.window = window
        self.color = color
        self.value = value
        self.card_type = self.determine_card_type(self.value)
        #self.card = self.parse_and_create_card(json_data)
        self.card = CardFactory.create_card(self.window, self.card_type, self.color, self.value)

    def determine_card_type(self, value):
        # Mapping values to card types
        type_mapping = {
            'reverse': 'reverse',
            'skip': 'skip',
            'draw_two': 'draw_two',
            'wild_pickfour': 'wild_pickfour',
            'wild_changer': 'wild_changer'
        }
        # Default to 'normal' if specific type not found
        return type_mapping.get(value, 'normal')
