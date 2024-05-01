import pygame
import pygwidgets
import pyghelpers

# constants
window_width = 800
window_height = 600
yellow = (255, 255, 0)

# settings scene class
class SettingsScene(pyghelpers.Scene):
    def __init__(self, window, settings):
        super().__init__()
        self.window = window
        self.settings = settings
        self.main_title = pygwidgets.DisplayText(window, (305, 40), "Settings", fontSize=75, textColor="black")

        # AI difficulty buttons
        self.title = pygwidgets.DisplayText(window, (345, 150), "Difficulty", fontSize=40, textColor="black")
        self.easy_button = pygwidgets.TextButton(window, (200, 200), "Easy", upColor=yellow, overColor=yellow, downColor=yellow)
        self.medium_button = pygwidgets.TextButton(window, (350, 200), "Medium", upColor=yellow, overColor=yellow, downColor=yellow)
        self.hard_button = pygwidgets.TextButton(window, (500, 200), "Hard", upColor=yellow, overColor=yellow, downColor=yellow)
        
        # SFX toggle button
        self.sfx_title = pygwidgets.DisplayText(window, (325, 290), "SFX Volume", fontSize=40, textColor="black")
        self.sfx_toggle = pygwidgets.TextButton(window, (300, 340), "SFX: On", width=200, height=40, upColor=yellow, overColor=yellow, downColor=yellow)
        
        # Music toggle button
        self.music_title = pygwidgets.DisplayText(window, (310, 430), "Music Volume", fontSize=40, textColor="black")
        self.music_toggle = pygwidgets.TextButton(window, (300, 480), "Music: On", width=200, height=40, upColor=yellow, overColor=yellow, downColor=yellow)
        
        # Back to Main Menu button
        self.backButton = pygwidgets.TextButton(window, (30, 550), "Back to Main Menu", upColor=yellow, overColor=yellow, downColor=yellow)

        
    def toggle_sfx_button(self):
        # toggles the state and updates the button label
        self.settings.toggle_sfx()
        new_label = "SFX: " + ("On" if self.settings.sfx_enabled else "Off")
        self.sfx_toggle = pygwidgets.TextButton(self.window, (300, 340), new_label, width=200, height=40, upColor=yellow, overColor=yellow, downColor=yellow)

        
        
    def toggle_music_button(self):
        # toggles the state and updates the button label
        self.settings.toggle_music()
        new_label = "Music: " + ("On" if self.settings.music_enabled else "Off")
        self.music_toggle = pygwidgets.TextButton(self.window, (300, 480), new_label, width=200, height=40, upColor=yellow, overColor=yellow, downColor=yellow)

    def handleInputs(self, events, keyPressedList):
        for event in events:  # iterate over each event in the list of events
            # pass each individual event to the handleEvent method of each button
            if self.easy_button.handleEvent(event):
                self.settings.set_difficulty('easy')
                print("Easy difficulty selected")
            elif self.medium_button.handleEvent(event):
                self.settings.set_difficulty('medium')
                print("Medium difficulty selected")
            elif self.hard_button.handleEvent(event):
                self.settings.set_difficulty('hard')
                print("Hard difficulty selected")
            elif self.sfx_toggle.handleEvent(event):
                self.toggle_sfx_button()  # toggle SFX and update button label
                print("SFX " + ("on" if self.settings.sfx_enabled else "off"))
            elif self.music_toggle.handleEvent(event):
                self.toggle_music_button()
                print("Music " + ("on" if self.settings.music_enabled else "off"))
            elif self.backButton.handleEvent(event):
                self.goToScene('main_menu')
                
                
    def draw(self):
        self.window.fill((255, 0, 0))  # red bckgd
        self.main_title.draw()
        self.title.draw()
        self.easy_button.draw()
        self.medium_button.draw()
        self.hard_button.draw()
        self.sfx_title.draw()
        self.sfx_toggle.draw()
        self.music_title.draw()
        self.music_toggle.draw()
        self.backButton.draw()

def main():
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Settings")

    settings_scene = SettingsScene(window)
    scenes_dict = {'Settings': settings_scene}
    scene_manager = pyghelpers.SceneMgr(scenes_dict)

    scene_manager.run()