class lobby:
    def __init__(self, lobby_name, game):
        self.lobby_name = lobby_name
        self.game = game
        self.clients = []
        self.client_names = []
    
    def add_client(self, client):
        pass
    
    def remove_client(self, client):
        pass
    
    def broadcast(self, message):
        pass
    
    def broadcast_current_color(self, color):
        pass
    
    def broadcast_current_value(self, value):
        pass
    
    def broadcast_current_direction(self, direction):
        pass
    
    def broadcast_player_list(self, player_list):
        pass
    
    def broadcast_current_player_index(self, player):
        pass
    
    def start_game(self):
        pass
    
    def broadcast_game_state(self):
        self.broadcast_current_color()
        self.broadcast_current_value()
        self.broadcast_current_direction()
        self.broadcast_player_list()
        self.broadcast_current_player_index()
        