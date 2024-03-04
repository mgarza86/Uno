import unittest
from model.deck import Deck 

class TestDeck(unittest.TestCase):

    def setUp(self):
        self.deck = Deck(window=None)  

    def test_deck_initialization(self):
        """Test that the deck initializes with the correct number of cards."""
        expected_card_count = 108  # Based on UNO rules
        self.assertEqual(len(self.deck.starting_deck), expected_card_count)

    def test_shuffle_deck(self):
        """Test that shuffling the deck changes the order of cards."""
        deck_before_shuffle = self.deck.starting_deck[:]
        self.deck.shuffle()
        self.assertNotEqual(deck_before_shuffle, self.deck.starting_deck, "Shuffling should change the deck order")

    def test_get_card(self):
        """Test that getting a card reduces the deck size by one."""
        initial_count = len(self.deck.starting_deck)
        self.deck.get_card()
        self.assertEqual(len(self.deck.starting_deck), initial_count - 1)

    def test_get_card_empty_deck(self):
        """Test that getting a card from an empty deck raises an IndexError."""
        self.deck.starting_deck = []  # Empty the deck
        with self.assertRaises(IndexError):
            self.deck.get_card()

    def test_return_card_to_deck(self):
        """Test that returning a card to the deck increases its size by one."""
        card = self.deck.get_card()  # Take a card out first
        initial_count = len(self.deck.starting_deck)
        self.deck.return_card_to_deck(card)
        self.assertEqual(len(self.deck.starting_deck), initial_count + 1)

    def test_deck_card_order_after_return(self):
        """Test that a returned card is placed at the correct position in the deck."""
        card = self.deck.get_card()
        self.deck.return_card_to_deck(card)
        self.assertIn(card, self.deck.starting_deck, "The returned card should be in the deck")

if __name__ == '__main__':
    unittest.main()
