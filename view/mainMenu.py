import pygame
import pygwidgets
import pyghelpers

# constants
scene_main_menu = "Main Menu"
yellow = (255, 255, 0)

# adding this to buttons later
buttonWidth = 150 
buttonHeight = 50  

class MainMenuScene(pyghelpers.Scene):
    def __init__(self, window, settings):
        super().__init__()
        self.window = window
        self.settings = settings
        self.title = pygwidgets.DisplayText(window, (200, 100), "Welcome to Py-UNO", fontSize=60, textColor="white")
        self.singlePlayerButton = pygwidgets.TextButton(window, (350, 250), "Single Player", upColor=yellow, overColor=yellow, downColor=yellow)
        self.multiplayerButton = pygwidgets.TextButton(window, (350, 350), "Multiplayer", upColor=yellow, overColor=yellow, downColor=yellow)
        self.settingsButton = pygwidgets.TextButton(window, (350, 450), "Settings", upColor=yellow, overColor=yellow, downColor=yellow)

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.singlePlayerButton.handleEvent(event):
                self.goToScene('single_player_setup')
            elif self.multiplayerButton.handleEvent(event):
                self.goToScene('multi_player_lobby')
            elif self.settingsButton.handleEvent(event):
                self.goToScene('settings')

    def draw(self):
        self.window.fill((255, 0, 0))  # red bckgd
        self.title.draw()
        self.singlePlayerButton.draw()
        self.multiplayerButton.draw()
        self.settingsButton.draw()
