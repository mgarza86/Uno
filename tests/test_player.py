import unittest
from model.deck import Deck 
import unittest
from unittest.mock import MagicMock
import pygame
import pygwidgets
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.card import Card
from model.player import Player
from model.game import Game

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.mock_window = MagicMock()
        self.player_name = "Test Player"
        self.player = Player(self.mock_window, self.player_name)
        self.game_deck = Deck(MagicMock())  
        self.game_deck.shuffle = MagicMock()  
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
        ''' Test that player can draw a card, resulting in an increase in hand size by one and a decrease in deck size by one '''
        mock_window = MagicMock()
        mock_window.get_size.return_value = (800, 600)  
        # init
        player = Player(mock_window, "Test Player")
        game_deck = Deck(mock_window)  
        session = Game(mock_window, [player], game_deck)
        
        # initial len
        initial_hand_length = len(player.hand)
        initial_deck_length = len(game_deck.starting_deck) 

        player.draw_card(session.draw_pile) 

        # new len
        new_hand_length = len(player.hand)
        new_deck_length = len(game_deck.starting_deck) 
    
        self.assertEqual(new_hand_length, initial_hand_length + 1, "Hand length did not increase by one after drawing a card.")
        self.assertEqual(new_deck_length, initial_deck_length - 1, "Deck length did not decrease by one after drawing a card.")

    def test_play_card(self):
        '''Test that the a card is removed from the hand to the discard pile when played'''
        self.player.hand.append(self.card_mock)
        played_card = self.player.play_card(self.card_mock)
        self.assertEqual(played_card.get_name(), self.card_mock.get_name())
        self.assertEqual(len(self.player.hand), 0)

    def test_get_player_name(self):
        self.assertEqual(self.player.get_name(), self.player_name)

    def test_check_playable_card_color_match(self):
        self.assertTrue(self.player.check_playable_card(self.card_mock, self.discard_pile_card))

    def test_check_playable_card_value_match(self):
        player = Player(self.mock_window,"Test Player")
        card = Card(window=None, color='red', value='5')  
        discard_pile_card = Card(window=None, color='blue', value='5')
        current_color = discard_pile_card.get_color()
        current_value = discard_pile_card.get_value()  
        self.assertTrue(player.check_conditions(card, current_color,current_value))

    def test_check_playable_card_no_match(self):
        player = Player(self.mock_window,"Test Player")
        card = Card(window=None, color='red', value='5')  
        discard_pile_card = Card(window=None, color='blue', value='4')
        current_color = discard_pile_card.get_color()
        current_value = discard_pile_card.get_value()  
        self.assertFalse(player.check_conditions(card, current_color,current_value))

if __name__ == '__main__':
    unittest.main()