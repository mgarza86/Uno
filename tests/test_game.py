import unittest
from unittest.mock import MagicMock
from model.game import Game 
from model.player import Player
from model.deck import Deck
from model.card import Card

class TestGame(unittest.TestCase):
    def setUp(self):
        
        self.mock_window = MagicMock()
        # Assuming get_size might still be called, mock it to avoid errors.
        self.mock_window.get_size.return_value = (800, 600)
        self.deck = Deck(self.mock_window) 
        self.deck.shuffle = MagicMock()  # Mock shuffle if necessary
        # Mock the draw_card method to avoid actual deck logic
        self.players = [Player(self.mock_window, f"Player {i}") for i in range(4)]
        for player in self.players:
            player.draw_card = MagicMock()  # Avoid actual drawing logic
            # Optionally mock initialize_card_positions if it's not relevant
            player.initialize_card_positions = MagicMock()

        self.game = Game(self.mock_window, self.players, self.deck)# Initialize Game with Players and Deck

    def test_initialize_players(self):
        """Test that each player starts with the correct number of cards."""
        number_of_cards = 7
        self.game.initialize_players(number_of_cards=number_of_cards)
        for player in self.game.players_list:
            # Instead of mocking get_size, ensure draw_card is called the correct number of times
            self.assertEqual(player.draw_card.call_count, number_of_cards)

    def test_play_card(self):
        """Test that a player can play a card, and it moves to the discard pile."""
        self.game.initialize_players()
        # Assuming you want to test this on the first player in the list
        player = self.players[0]  # Define player by selecting from self.players
        card_to_play = Card(self.mock_window, "Red", "5")  
        player.hand.append(card_to_play)  # Now 'player' is defined, so this should work
        initial_discard_pile_size = len(self.game.discard_pile)

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
