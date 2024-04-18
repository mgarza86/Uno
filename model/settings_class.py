class Settings:
    def __init__(self):
        self.sfx_enabled = True
        self.music_enabled = True
        self.difficulty = 'medium'
        
    def toggle_sfx(self):
        self.sfx_enabled = not self.sfx_enabled

    def toggle_music(self):
        self.music_enabled = not self.music_enabled

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
