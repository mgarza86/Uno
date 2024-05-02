# Re-defining the required classes and running the tests again after the reset

import unittest
import json

from model.player_net import Player
from model.card_net import *

class TestPlayerSerialization(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestPlayer")
        self.card1 = Card("red", "5")
        self.card2 = Card("blue", "skip")
    
    def test_player_to_dict_without_hand(self):
        expected = {'name': "TestPlayer"}
        self.assertEqual(self.player.to_dict(), expected)
    
    def test_player_to_dict_with_hand(self):
        self.player.hand = [self.card1, self.card2]
        expected = {
            'name': "TestPlayer",
            'hand': [
                {
                    'color': "red",
                    'value': "5",
                    'is_concealed': True, 
                    'card_name': "red_5"
                },
                {
                    'color': "blue",
                    'value': "skip",
                    'is_concealed': True, 
                    'card_name': "blue_skip"
                }
            ]
        }
        self.assertEqual(self.player.to_dict(include_hand=True), expected)

    def test_player_to_json_without_hand(self):
        expected = json.dumps({'name': "TestPlayer"})
        self.assertEqual(self.player.to_json(), expected)
    
    def test_player_to_json_with_hand(self):
        self.player.hand = [self.card1, self.card2]
        expected = json.dumps({
            'name': "TestPlayer",
            'hand': [
                {'color': "red",
                'value': "5",
                'is_concealed': True, 
                'card_name': "red_5"},
                {'color': "blue",
                'value': "skip",
                'is_concealed': True, 
                'card_name': "blue_skip"}
            ]
        })
        self.assertEqual(self.player.to_json(include_hand=True), expected)


unittest.main(argv=[''], exit=False)