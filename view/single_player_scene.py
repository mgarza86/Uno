import pygame
import pygwidgets
import pyghelpers
from model.game import Game
from model.deck import Deck
from model.player import Player, AIPlayer

# constants
window_width = 800
window_height = 600
yellow = (255, 255, 0)
black = (0, 0, 0)

class SinglePlayerSetupScene(pyghelpers.Scene):
    def __init__(self, window):
        super().__init__()
        self.window = window
        
        # text instruction for the player
        self.instructions_text = pygwidgets.DisplayText(window, (75, 60), 
                                                        "Please choose the number of NPCs you would like to play against:",
                                                        fontSize=30, textColor=black, justified='center')

        # NPC selection buttons
        self.npc1_button = pygwidgets.TextButton(window, (150, 200), "1", fontSize=25, upColor=yellow, overColor=yellow, downColor=yellow)
        self.npc2_button = pygwidgets.TextButton(window, (350, 200), "2", fontSize=25, upColor=yellow, overColor=yellow, downColor=yellow)
        self.npc3_button = pygwidgets.TextButton(window, (550, 200), "3", fontSize=25, upColor=yellow, overColor=yellow, downColor=yellow)

        # play button
        self.play_button = pygwidgets.TextButton(window, (295, 340), "Play!", fontSize=30, width=200, height=60, upColor=yellow, overColor=yellow, downColor=yellow)
        
        # back to Main Menu button
        self.backButton = pygwidgets.TextButton(window, (30, 550), "Back to Main Menu", upColor=yellow, overColor=yellow, downColor=yellow)

        # variable to keep track of selected NPC count
        self.selected_npc_count = None
        self.deck = Deck()
        self.deck.shuffle()
        self.pc = Player(self.window,"Player One")
        self.npc1 = AIPlayer(self.window,"Player Two")
        self.npc2 = AIPlayer(self.window,"Player Three")
        self.npc3 = AIPlayer(self.window,"Player Four")
        self.player_list = [self.pc,self.npc1]
        
        
        
    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.npc1_button.handleEvent(event):
                self.selected_npc_count = 1
                print("Selected to play against 1 NPC")
                while len(self.player_list) > 2:
                    self.player_list.pop()
            elif self.npc2_button.handleEvent(event):
                self.selected_npc_count = 2
                print("Selected to play against 2 NPCs")
                while len(self.player_list) > 3:
                    self.player_list.pop()
                while len(self.player_list) < 3:
                    self.player_list.append(self.npc2)
            elif self.npc3_button.handleEvent(event):
                self.selected_npc_count = 3
                print("Selected to play against 3 NPCs")
                while len(self.player_list) > 4:
                    self.player_list.pop()
                if len(self.player_list) == 2:
                    self.player_list.append(self.npc2)
                    self.player_list.append(self.npc3)
                elif len(self.player_list) == 3:
                    self.player_list.append(self.npc3)
            elif self.play_button.handleEvent(event):
                if self.selected_npc_count is not None:
                    print(f"Starting game with {self.selected_npc_count} NPCs")
                    # Then afterwards, you would go to the game scene
                    game = Game(self.window,self.player_list, self.deck)
                    self.goToScene('game', game)
                else:
                    print("Please select the number of NPCs before playing")
            elif self.backButton.handleEvent(event):
                self.goToScene('main_menu')


    def draw(self):
        self.window.fill((255, 0, 0)) # background
        self.instructions_text.draw()
        self.npc1_button.draw()
        self.npc2_button.draw()
        self.npc3_button.draw()
        self.play_button.draw()
        self.backButton.draw()

