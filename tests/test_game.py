import unittest
from unittest.mock import Mock
from model.game import Game 
from model.player import Player
from model.deck import Deck
from model.card import Card

class TestGame(unittest.TestCase):
    def setUp(self):
        self.deck = Deck(window=None) 
        self.deck.shuffle()  
        self.players = [Player(f"Player {i}") for i in range(4)] 
        self.game = Game(self.players, self.deck)  # Initialize Game with Players and Deck

    def test_game_initialization(self):
        """Test that the game initializes correctly with the given players and deck."""
        self.assertEqual(len(self.game.players_list), 4)
        self.assertIsInstance(self.game.draw_pile.get_card(), Card)

    def test_initialize_players(self):
        """Test that each player starts with the correct number of cards."""
        self.game.initialize_players()
        for player in self.game.players_list:
            self.assertEqual(len(player.hand), 7)  # Assuming starting hand size of 7 cards
            self.assertTrue(all(isinstance(card, Card) for card in player.hand))

    def test_play_card(self):
        """Test that a player can play a card, and it moves to the discard pile."""
        self.game.initialize_players()
        initial_discard_pile_size = len(self.game.discard_pile)
        player = self.players[0]
        card_to_play = player.hand[0]  # Select the first card in player's hand to play
        self.game.play_card(player, card_to_play)
        self.assertIn(card_to_play, self.game.discard_pile)
        self.assertEqual(len(self.game.discard_pile), initial_discard_pile_size + 1)
        self.assertNotIn(card_to_play, player.hand)

    def test_determine_next_player(self):
        """Test that the game correctly determines the next player."""
        self.game.initialize_players()
        current_player_index = self.game.current_player_index
        self.game.determine_next_player()
        expected_next_player_index = (current_player_index + 1) % len(self.players)
        self.assertEqual(self.game.current_player_index, expected_next_player_index)

    def test_check_game_end(self):
        """Test that the game correctly identifies when a player has won (no cards left)."""
        self.game.initialize_players()
        winning_player = self.players[0]
        winning_player.hand = []  # Simulate the player playing all their cards
        self.assertTrue(self.game.check_game_end(winning_player))

if __name__ == '__main__':
    unittest.main()
