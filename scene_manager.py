import pygame
import pyghelpers

# importing scenes from the view folder
from view.mainMenu import MainMenuScene
from view.settings import SettingsScene
# from view.single_player import SinglePlayerSetupScene
# from view.multi_player import MultiPlayerLobbyScene

# constants
window_width = 800
window_height = 600
frames_per_second = 60

pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Py-UNO")

    # scene creation: instantiating each scene
main_menu_scene = MainMenuScene(window)
settings_scene = SettingsScene(window)
    # single_player_setup_scene = SinglePlayerSetupScene(window)
    # multi_player_lobby_scene = MultiPlayerLobbyScene(window)

    # scene management: store scenes in a dictionary
scenes_dict = {
        'main_menu': main_menu_scene,
        'settings': settings_scene,
        # 'single_player_setup': single_player_setup_scene,
        # 'multi_player_lobby': multi_player_lobby_scene
    }

    # create an instance of pyghelpers.SceneMgr with the dictionary of scenes and frame rate
scene_manager = pyghelpers.SceneMgr(scenes_dict, frames_per_second)

    # utilize the run method of SceneMgr to start and manage the application
scene_manager.run()