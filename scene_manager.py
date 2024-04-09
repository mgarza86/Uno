import pygame
import pyghelpers

# importing scenes from the view folder
from view.mainMenu import MainMenuScene
from view.settings import SettingsScene
from view.single_player_scene import SinglePlayerSetupScene
from view.multi_player_scene import MultiPlayerLobbyScene
from view.game_board import GameBoard
from view.end_screen import EndScreen
from view.pre_game_lobby import PreGameLobby
from model.settings_class import Settings


# constants
window_width = 800
window_height = 600
frames_per_second = 60

pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Py-UNO")

# Settings object
settings = Settings()

# scene creation: instantiating each scene
main_menu_scene = MainMenuScene(window, settings)
settings_scene = SettingsScene(window, settings)
single_player_scene = SinglePlayerSetupScene(window, settings)
multi_player_scene = MultiPlayerLobbyScene(window, settings)
game_board = GameBoard(window, settings)
end = EndScreen(window, settings)
pre_game_lobby = PreGameLobby(window, settings)


# scene management: store scenes in a dictionary
scenes_dict = {
        'main_menu': main_menu_scene,
        'settings': settings_scene,
        'single_player_setup': single_player_scene,
        'multi_player_lobby': multi_player_scene,
        'pre_game_lobby': pre_game_lobby,
        'game': game_board,
        'end': end
    }

# create an instance of pyghelpers.SceneMgr with the dictionary of scenes and frame rate
scene_manager = pyghelpers.SceneMgr(scenes_dict, frames_per_second)

# utilize the run method of SceneMgr to start and manage the application
scene_manager.run()