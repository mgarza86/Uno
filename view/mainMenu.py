import pygwidgets
import pygame, sys

# constants
WIDTH, HEIGHT = (800, 600)
WHITE = (255, 255, 255)
RED = (255,0,0)  # red for the background
YELLOW = (255, 255, 0) # this yellow is for the buttons
BLACK = (0, 0, 0) # the text font
WINDOW_TITLE = "Main Menu"

# pygame initialization
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
mainClock = pygame.time.Clock()

# this is where the title and buttons are created
title = pygwidgets.DisplayText(window, (0, 60), "Welcome to Py-UNO", fontSize=50, textColor=WHITE)
titleRect = title.getRect()
title.setLoc((WIDTH // 2 - titleRect.width // 2, 60))
singlePlayerButton = pygwidgets.TextButton(window, ((WIDTH // 2) - 100, (HEIGHT // 2) - 60), "Single Player", width=200, height=50, fontName='Arial', fontSize=24, textColor=BLACK, upColor=YELLOW, overColor=YELLOW, downColor=YELLOW)
multiplayerButton = pygwidgets.TextButton(window, ((WIDTH // 2) - 100, (HEIGHT // 2) + 20), "Multiplayer", width=200, height=50, fontName='Arial', fontSize=24, textColor=BLACK, upColor=YELLOW, overColor=YELLOW, downColor=YELLOW)
settingsButton = pygwidgets.TextButton(window, ((WIDTH // 2) - 100, (HEIGHT // 2) + 100), "Settings", width=200, height=50, fontName='Arial', fontSize=24, textColor=BLACK, upColor=YELLOW, overColor=YELLOW, downColor=YELLOW)

# The main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # handle button events
        if singlePlayerButton.handleEvent(event):
            print("Single Player button was clicked")
        elif multiplayerButton.handleEvent(event):
            print("Multiplayer button was clicked")
        elif settingsButton.handleEvent(event):
            print("Settings button was clicked")

    # draw everything here
    window.fill(RED)
    title.draw()
    singlePlayerButton.draw()
    multiplayerButton.draw()
    settingsButton.draw()

    # update the display
    pygame.display.update()
    mainClock.tick(60)

# in order to quit the program
pygame.quit()
sys.exit()
