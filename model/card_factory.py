from model.card import *

class CardFactory:
    @staticmethod
    def create_card(window, card_type, color, value):
        if card_type == 'normal':
            return Card(window, color, value)
        elif card_type == 'wild_pickfour':
            return WildPickFour(window, color, value)
        elif card_type == 'wild_changer':
            return WildChanger(window, color, value)
        elif card_type == 'skip':
            return Skip(window, color, value)
        elif card_type == 'reverse':
            return Reverse(window, color, value)
        elif card_type == 'draw_two':
            return DrawTwoCard(window, color, value)