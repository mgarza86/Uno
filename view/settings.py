import pygame
import pygwidgets
import pyghelpers

# constants
window_width = 800
window_height = 600
yellow = (255, 255, 0)

# settings scene class
class SettingsScene(pyghelpers.Scene):
    def __init__(self, window):
        super().__init__()
        self.window = window

        # AI difficulty buttons
        self.title = pygwidgets.DisplayText(window, (350, 130), "Difficulty", fontSize=40, textColor="white")
        self.easy_button = pygwidgets.TextButton(window, (200, 200), "Easy", upColor=yellow, overColor=yellow, downColor=yellow)
        self.medium_button = pygwidgets.TextButton(window, (350, 200), "Medium", upColor=yellow, overColor=yellow, downColor=yellow)
        self.hard_button = pygwidgets.TextButton(window, (500, 200), "Hard", upColor=yellow, overColor=yellow, downColor=yellow)
        
        # SFX toggle button
        self.sfx_on = True
        self.sfx_toggle = pygwidgets.TextButton(window, (300, 320), "SFX: On", width=200, height=40)

    
    def toggle_sfx_button(self):
        # toggles the state and updates the button label
        self.sfx_on = not self.sfx_on
        new_label = "SFX: " + ("On" if self.sfx_on else "Off")
        self.sfx_toggle = pygwidgets.TextButton(self.window, (300, 320), new_label, width=200, height=40)

    def handleInputs(self, events, keyPressedList):
        for event in events:  # iterate over each event in the list of events
            # pass each individual event to the handleEvent method of each button
            if self.easy_button.handleEvent(event):
                print("Easy difficulty selected")
            elif self.medium_button.handleEvent(event):
                print("Medium difficulty selected")
            elif self.hard_button.handleEvent(event):
                print("Hard difficulty selected")
            elif self.sfx_toggle.handleEvent(event):
                self.toggle_sfx_button()  # Update SFX button label
                print("SFX " + ("on" if self.sfx_on else "off"))
                
    def draw(self):
        self.window.fill((255, 0, 0))  # red bckgd
        self.title.draw()
        self.easy_button.draw()
        self.medium_button.draw()
        self.hard_button.draw()
        self.sfx_toggle.draw()

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
