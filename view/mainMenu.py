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
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.title = pygwidgets.DisplayText(window, (200, 100), "Welcome to Py-UNO", fontSize=60, textColor="white")
        self.singlePlayerButton = pygwidgets.TextButton(window, (350, 250), "Single Player", upColor=yellow, overColor=yellow, downColor=yellow)
        self.multiplayerButton = pygwidgets.TextButton(window, (350, 350), "Multiplayer", upColor=yellow, overColor=yellow, downColor=yellow)
        self.settingsButton = pygwidgets.TextButton(window, (350, 450), "Settings", upColor=yellow, overColor=yellow, downColor=yellow)

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.singlePlayerButton.handleEvent(event):
                print("Single Player button was clicked")
            elif self.multiplayerButton.handleEvent(event):
                print("Multiplayer button was clicked")
            elif self.settingsButton.handleEvent(event):
                print("Settings button was clicked")

    def draw(self):
        self.window.fill((255, 0, 0))  # red bckgd
        self.title.draw()
        self.singlePlayerButton.draw()
        self.multiplayerButton.draw()
        self.settingsButton.draw()

# main pygame loop
def main():
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Main Menu")

    # main menu scene
    mainMenuScene = MainMenuScene(window)
    
    # created a scenes dictionary with just the main menu scene for now
    scenesDict = {scene_main_menu: mainMenuScene}

    # passing in the dictionary of scenes
    sceneManager = pyghelpers.SceneMgr(scenesDict, 60)

    # start
    sceneManager.run()

if __name__ == "__main__":
    main()
