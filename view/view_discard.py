import pygame
import json
from model.card_factory import CardFactory

class ViewDiscard:
    def __init__(self, window, initial_data=None):
        self.window = window
        if initial_data:
            self.update(initial_data)        
        self.card = None

    def update(self, data):
        color, value = data.split(',')
        
        self.card = CardFactory.create_card(self.window, color, value)
        self.card.flag_discarded()
    