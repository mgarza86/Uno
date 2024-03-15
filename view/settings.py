import pygame
import pygwidgets
import pyghelpers

# constants
window_width = 800
window_height = 600

# settings scene class
class SettingsScene(pyghelpers.Scene):
    def __init__(self, window):
        super().__init__()
        self.window = window

        # AI Difficulty Buttons
        self.title = pygwidgets.DisplayText(window, (350, 130), "Difficulty", fontSize=40, textColor="white")
        self.easy_button = pygwidgets.TextButton(window, (200, 200), "Easy")
        self.medium_button = pygwidgets.TextButton(window, (350, 200), "Medium")
        self.hard_button = pygwidgets.TextButton(window, (500, 200), "Hard")
        

    def handleInputs(self, events, keyPressedList):
        for event in events:  # iterate over each event in the list of events
            # pass each individual event to the handleEvent method of each button
            if self.easy_button.handleEvent(event):
                print("Easy difficulty selected")
            elif self.medium_button.handleEvent(event):
                print("Medium difficulty selected")
            elif self.hard_button.handleEvent(event):
                print("Hard difficulty selected")

    def draw(self):
        self.window.fill((255, 0, 0))  # red bckgd
        self.title.draw()
        self.easy_button.draw()
        self.medium_button.draw()
        self.hard_button.draw()

def main():
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Settings")

    settings_scene = SettingsScene(window)
    scenes_dict = {'Settings': settings_scene}
    scene_manager = pyghelpers.SceneMgr(scenes_dict)

    scene_manager.run()

if __name__ == "__main__":
    main()
