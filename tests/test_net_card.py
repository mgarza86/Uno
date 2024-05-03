import unittest
import json
from model.card_net import *

class TestCardSerialization(unittest.TestCase):
        
    def test_regular_uno_card_to_json(self):
        card = Card('red', '8')
        expected_json = '{"color": "red", "value": "8"}'
        self.assertEqual(json.loads(card.to_json()), json.loads(expected_json))

    def test_wild_pick_four_to_json(self):
        card = WildPickFour('black', 'pickfour')
        expected_json = '{"color": "black", "value": "pickfour"}'
        self.assertEqual(json.loads(card.to_json()), json.loads(expected_json))

    def test_uno_reverse_to_json(self):
        card = Reverse('blue', 'reverse')
        expected_json = '{ "color": "blue", "value": "reverse"}'
        self.assertEqual(json.loads(card.to_json()), json.loads(expected_json))
        
    def test_uno_skip_to_json(self):
        card = Skip('green', 'skip')
        expected_json = '{"color": "green", "value": "skip"}'
        self.assertEqual(json.loads(card.to_json()), json.loads(expected_json))
        
    def test_uno_draw_two_to_json(self):
        card = DrawTwoCard('yellow', 'drawtwo')
        expected_json = '{"color": "yellow", "value": "drawtwo"}'
        self.assertEqual(json.loads(card.to_json()), json.loads(expected_json))

if __name__ == '__main__':
    unittest.main()
