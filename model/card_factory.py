from model.card_net import *

class CardFactory:
    @staticmethod
    def create_card(color, value, window):
        if value == 'pickfour':
            return WildPickFour(color, value, window)
        elif value == 'wild':
            return WildChanger(color, value, window)
        elif value == 'skip':
            return Skip(color, value,window)
        elif value == 'reverse':
            return Reverse(color, value, window)
        elif value == 'picker':
            return DrawTwoCard(color, value, window)
        else:
            return Card( color, value, window)