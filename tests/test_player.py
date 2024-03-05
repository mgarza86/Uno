import unittest
from model.deck import Deck 
import unittest
from unittest.mock import Mock
import pygame
import pygwidgets
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.card import Card

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player_name = "Test Player"
        self.player = Player(self.player_name)
        self.game_deck = Deck(MagicMock())  # Mocking the window parameter
        self.game_deck.shuffle = MagicMock()  # Mock shuffle method
        self.card_mock = MagicMock()
        self.card_mock.get_name.return_value = "blue_3"
        self.card_mock.get_color.return_value = "blue"
        self.card_mock.get_value.return_value = "3"
        self.discard_pile_card = MagicMock()
        self.discard_pile_card.get_color.return_value = "blue"
        self.discard_pile_card.get_value.return_value = "5"

    def test_player_initialization(self):
        self.assertEqual(self.player.name, self.player_name)
        self.assertEqual(len(self.player.hand), 0)

    def test_draw_card(self):
        self.game_deck.get_card = MagicMock(return_value=self.card_mock)
        self.player.draw_card(self.game_deck.get_card())
        self.assertEqual(len(self.player.hand), 1)
        self.assertIn(self.card_mock, self.player.hand)

    def test_play_card(self):
        self.player.hand.append(self.card_mock)
        played_card = self.player.play_card(self.card_mock)
        self.assertEqual(played_card.get_name(), self.card_mock.get_name())
        self.assertEqual(len(self.player.hand), 0)

    def test_get_player_name(self):
        self.assertEqual(self.player.get_player_name(), self.player_name)

    def test_check_playable_card_color_match(self):
        self.assertTrue(self.player.check_playable_card(self.card_mock, self.discard_pile_card))

    def test_check_playable_card_value_match(self):
        self.discard_pile_card.get_color.return_value = "red"  # Change color to ensure it's testing value
        self.assertTrue(self.player.check_playable_card(self.card_mock, self.discard_pile_card))

    def test_check_playable_card_no_match(self):
        self.discard_pile_card.get_color.return_value = "red"
        self.discard_pile_card.get_value.return_value = "1"
        self.assertFalse(self.player.check_playable_card(self.card_mock, self.discard_pile_card))

if __name__ == '__main__':
    unittest.main()