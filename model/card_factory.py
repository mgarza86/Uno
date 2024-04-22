from model.card import *

class CardFactory:
    @staticmethod
    def create_card(window, color, value):
        if value == 'pickfour':
            return WildPickFour(window, color, value)
        elif value == 'wild':
            return WildChanger(window, color, value)
        elif value == 'skip':
            return Skip(window, color, value)
        elif value == 'reverse':
            return Reverse(window, color, value)
        elif value == 'picker':
            return DrawTwoCard(window, color, value)
        else:
            return Card(window, color, value)