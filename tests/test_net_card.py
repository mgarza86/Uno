import unittest
import json
from model.card_net import *

class TestCardSerialization(unittest.TestCase):
        
    def test_regular_uno_card_to_json(self):
        card = Card('red', '8')
        expected_json = '{"card_name": "red_8", "color": "red", "is_concealed": true, "value": "8"}'
        self.assertEqual(json.loads(card.to_json()), json.loads(expected_json))

    def test_wild_pick_four_to_json(self):
        card = WildPickFour('black', 'pickfour')
        expected_json = '{"card_name": "black_pickfour", "color": "black", "is_concealed": true, "value": "pickfour"}'
        self.assertEqual(json.loads(card.to_json()), json.loads(expected_json))

    def test_uno_reverse_to_json(self):
        card = Reverse('blue', 'reverse')
        expected_json = '{"card_name": "blue_reverse", "color": "blue", "is_concealed": true, "value": "reverse"}'
        self.assertEqual(json.loads(card.to_json()), json.loads(expected_json))
        
    def test_uno_skip_to_json(self):
        card = Skip('green', 'skip')
        expected_json = '{"card_name": "green_skip", "color": "green", "is_concealed": true, "value": "skip"}'
        self.assertEqual(json.loads(card.to_json()), json.loads(expected_json))
        
    def test_uno_draw_two_to_json(self):
        card = DrawTwoCard('yellow', 'drawtwo')
        expected_json = '{"card_name": "yellow_drawtwo", "color": "yellow", "is_concealed": true, "value": "drawtwo"}'
        self.assertEqual(json.loads(card.to_json()), json.loads(expected_json))

if __name__ == '__main__':
    unittest.main()
