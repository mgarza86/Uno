import pygame
import pyghelpers

# importing scenes from the view folder
from view import mainMenu as MainMenuScene 
from view import settings as SettingsScene
from view import single_player as SinglePlayerSetupScene
from view import multi_player as MultiPlayerLobbyScene

# constants
window_width = 640
window_height = 480
frames_per_second = 60


    
if __name__ == "__main__":
    main()