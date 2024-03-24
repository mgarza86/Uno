import pygame
import pygwidgets
import pyghelpers

# Constants
window_width = 800
window_height = 600
yellow = (255, 255, 0)
black = (0, 0, 0)
gray = (141, 141, 141)


class MultiPlayerLobbyScene(pyghelpers.Scene):
    def __init__(self, window):
        super().__init__()
        self.window = window
        
        # title and instructions
        self.lobby_title = pygwidgets.DisplayText(window, (100, 80), "Lets play Py-Uno with friends!", fontSize=48, textColor=black, width=600, justified='center')
        self.lobby_instructions = pygwidgets.DisplayText(window, (100, 130), "To get started, enter your player name and a game room. \n Other players can join your game with the same room name \n on their device.", 
                                                         fontSize=28, textColor=black, width=600, justified='center')

        # input fields
        self.player_name_field = pygwidgets.InputText(window, (100, 250), 
                                                      value='', 
                                                      width=600, fontSize=22, textColor=gray)
        self.lobby_name_field = pygwidgets.InputText(window, (100, 300), 
                                                     value='lobby-1', 
                                                     width=600, fontSize=22, textColor=gray)

        # play button
        self.play_button = pygwidgets.TextButton(window, (300, 380), "Play!", width=200, height=60, fontSize=30, upColor=yellow, overColor=yellow, downColor=yellow)
        
        # back to Main Menu button
        self.backButton = pygwidgets.TextButton(window, (30, 550), "Back to Main Menu", upColor=yellow, overColor=yellow, downColor=yellow)
        
        # drawing white rectangles behind the input fields for visual effect
        padding = 10
        self.player_name_rect = pygame.Rect(100 - padding, 250 - padding, 600 + (padding * 2), 12 + (padding * 2))
        self.lobby_name_rect = pygame.Rect(100 - padding, 300 - padding, 600 + (padding * 2), 12 + (padding * 2))
        
        
    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.play_button.handleEvent(event):
                player_name = self.player_name_field.getValue()
                lobby_name = self.lobby_name_field.getValue()
                print(f"Player Name: {player_name}, Lobby Name: {lobby_name}")
                # here the players would go to the game, passing along these values
            elif self.player_name_field.handleEvent(event):
                    self.player_name_field.setValue()    
            elif self.lobby_name_field.handleEvent(event):
                    self.lobby_name_field.setValue()
                
            elif self.backButton.handleEvent(event):
                self.goToScene('main_menu')
                
                
    def draw(self):
        self.window.fill((255, 0, 0))  # red background
        
        pygame.draw.rect(self.window, (255, 255, 255), self.player_name_rect)  # drawing white rectangle for player name field
        pygame.draw.rect(self.window, (255, 255, 255), self.lobby_name_rect)  # drawing white rectangle for lobby name field


        self.lobby_title.draw()
        self.lobby_instructions.draw()
        self.player_name_field.draw()
        self.lobby_name_field.draw()
        self.play_button.draw()
        self.backButton.draw()