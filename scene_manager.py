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

def main():
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Py-UNO")

    # scene creation: instantiating each scene
    main_menu_scene = MainMenuScene(window)
    settings_scene = SettingsScene(window)
    single_player_setup_scene = SinglePlayerSetupScene(window)
    multi_player_lobby_scene = MultiPlayerLobbyScene(window)


    
if __name__ == "__main__":
    main()