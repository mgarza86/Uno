import pygame
import pyghelpers
from game_board import GameBoard
from model.card import *
from model.deck import Deck
from model.game import Game
from model.player import *
from end_screen import EndScreen

# 2 - Define constants
FRAMES_PER_SECOND = 30
WINDOW_WIDTH, WINDOW_HEIGHT = (1000,1000)

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

deck = Deck(window)
deck.shuffle()
pc = Player(window,"Player One")
npc1 = AIPlayer(window,"Player Two")
npc2 = AIPlayer(window,"Player Three")
npc3 = AIPlayer(window,"Player Four")
player_list = [pc, npc1, npc2, npc3]

session = Game(window,player_list,deck)


# Instantiate all scenes and store them in a dictionary (as of pyghelpers 1.1)
scenes_dict = {'game': GameBoard(window, session),
               'end': EndScreen(window) 
               }

# Create the Scene Manager, passing in the scenes list, and the FPS
o_scene_manager = pyghelpers.SceneMgr(scenes_dict, FRAMES_PER_SECOND)

# Tell the Scene Manager to start running
o_scene_manager.run()