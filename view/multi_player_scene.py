import pygame
import pygwidgets
import pyghelpers


class MultiPlayerLobbyScene(pyghelpers.Scene):
    def __init__(self, window):
        super().__init__()
        self.window = window