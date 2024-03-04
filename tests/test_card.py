import unittest
from unittest.mock import Mock
import pygame
import pygwidgets
from ..model import Card 

class TestCard(unittest.TestCase):

    def setUp(self):
        # Mock the pygame window and ImageCollection
        self.mock_window = Mock()
        self.mock_image_collection = Mock()
        pygwidgets.ImageCollection = Mock(return_value=self.mock_image_collection)
        
        self.card = Card(self.mock_window, 'red', '5', 'test_file_name.png')

    def test_initialization(self):
        self.assertEqual(self.card.color, 'red')
        self.assertEqual(self.card.value, '5')
        self.assertEqual(self.card.card_name, 'red_5')
        # Test that the ImageCollection was initialized with the correct parameters
        pygwidgets.ImageCollection.assert_called_with(self.mock_window, (0, 0), {'front': 'test_file_name.png', 'back': Card.BACK_OF_CARD}, 'back')

    def test_conceal_reveal(self):
        self.card.conceal()
        self.mock_image_collection.replace.assert_called_with('back')

        self.card.reveal()
        self.mock_image_collection.replace.assert_called_with('front')

    def test_getters(self):
        self.assertEqual(self.card.get_color(), 'red')
        self.assertEqual(self.card.get_value(), '5')
        self.assertEqual(self.card.get_name(), 'red_5')

    def test_location(self):
        # Set a new location and verify it is updated
        new_location = (100, 200)
        self.card.set_location(new_location)
        self.mock_image_collection.setLoc.assert_called_with(new_location)

        # Mock the getLoc method to return the new location
        self.mock_image_collection.getLoc.return_value = new_location
        self.assertEqual(self.card.get_location(), new_location)

if __name__ == '__main__':
    unittest.main()
