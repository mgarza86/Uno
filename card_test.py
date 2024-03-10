import pygame
import pygwidgets
from model.card import Card, WildChanger, WildPickFour, Skip, DrawTwoCard, Reverse
from model.deck import Deck
from model.player import Player

def run_game():
    pygame.init()
    window_size = (800, 600)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Player Hand Test")

    clock = pygame.time.Clock()
    FRAMES_PER_SECOND = 30

    # Initialize the deck and player
    deck = Deck(window)
    deck.shuffle()  # Make sure to shuffle the deck
    player = Player(window, "Test Player",1)

    # Draw 5 cards for the player (or however many you want)
    for _ in range(5):
        player.draw_card(deck)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        window.fill((0, 100, 0))  # A green background to represent the table

        # Draw the player's hand
        player.draw()

        pygame.display.flip()
        clock.tick(FRAMES_PER_SECOND)

    pygame.quit()

if __name__ == "__main__":
    run_game()
