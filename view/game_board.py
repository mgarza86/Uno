import pygame
import pygwidgets 
import pyghelpers
import model.game
from model.player import Player, AIPlayer

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
X_COORDINATE, Y_COORDINATE = (0,0)
blue = (0, 9, 255)
white = (255, 255, 255)

class GameBoard(pyghelpers.Scene):
    
    def __init__(self, window) -> None:
        self.window = window
        self.back_ground_color = (161, 59, 113)
        self.window_width, self.window_height = self.window.get_size()
        
        self.x_coord = (self.window_width - 200) / 2
        self.y_coord = (self.window_height - 80) / 2
        
        self.red_button = pygwidgets.TextButton(window, loc=(self.x_coord, self.y_coord), text='Red', upColor=RED)
        self.green_button = pygwidgets.TextButton(window, loc=(self.x_coord + 100, self.y_coord), text='Green', upColor=GREEN)
        self.blue_button = pygwidgets.TextButton(window, loc=(self.x_coord, self.y_coord + 40), text='Blue', upColor=BLUE)
        self.yellow_button = pygwidgets.TextButton(window, loc=(self.x_coord + 100, self.y_coord + 40), text='Yellow', upColor=YELLOW)
        
        self.show_color_picker = False
        
        #self.enter()
        # initializing the "Call Uno", "Draw Card" and "Call Out buttons
        self.callUnoButton = pygwidgets.TextButton(window, (360, 390), "Call Uno", textColor=white, width=100, height=35, upColor=blue, overColor=blue, downColor=blue)
        self.drawCardButton = pygwidgets.TextButton(window, (270, 435), "Draw Card", textColor=white, width=100, height=35, upColor=blue, overColor=blue, downColor=blue)
        self.callOutButton = pygwidgets.TextButton(window, (380, 435), "Call out", textColor=white, width=200, height=35, upColor=blue, overColor=blue, downColor=blue)
        
                
    def enter(self,game):
        self.game = game
        self.game.initialize_players(7)
    
    def update(self):
        if self.game.current_color == 'black':
            self.show_color_picker = True
        else:
            self.show_color_picker = False
            
    def handleInputs(self, event_list, key_pressed_list):
        for event in event_list:
            current_player = self.game.players_list[self.game.current_player_index]
            
            # dynamically create the "Call out player" button with the current player's name
            callOutButtonText = f"{current_player.get_name()} didn't call Uno"
            self.callOutButton = pygwidgets.TextButton(self.window, (380, 435), callOutButtonText, textColor=white, width=200, height=35, upColor=blue, overColor=blue, downColor=blue)
                   
            if isinstance(current_player, AIPlayer):
                self.computer_move(current_player,event)            
            elif isinstance(current_player, Player):
                self.player_move(current_player,event)
                
            if self.red_button.handleEvent(event):
                self.game.current_color = "red"
                self.show_color_picker = False
            if self.blue_button.handleEvent(event):
                self.game.current_color = "blue"
                self.show_color_picker = False
            if self.green_button.handleEvent(event):
                self.game.current_color = "green"
                self.show_color_picker = False
            if self.yellow_button.handleEvent(event):
                self.game.current_color = "yellow"
                self.show_color_picker = False   
                self.player_move(current_player,event)    
            # checks if Call Uno, Draw card and Call out buttons have been clicked
            if self.callUnoButton.handleEvent(event):
                print("Call Uno button was clicked!")
            if self.drawCardButton.handleEvent(event):
                print("Draw Card button was clicked!")
            if self.callOutButton.handleEvent(event):
                print(f"Calling out {current_player.get_name()} for not saying Uno!")
    
    def player_move(self, player, event):
        if self.game.check_hand(player):
            for card in player.hand[:]:
                if card.handle_event(event):
                    #if player.check_playable_card(card, self.game.discard_pile): #!change this
                    if player.check_conditions(card, self.game.current_color, self.game.current_value):
                        #print(card.get_name())
                        self.game.play_card(player,card)
                        if self.game.check_game_end(player):
                            self.goToScene('end',player.get_name())
                        self.game.determine_next_player()
                        print(f"{self.game.players_list[self.game.current_player_index].get_name()}'s turn")
                        break
        else:
            player.draw_card(self.game.draw_pile)
            self.game.determine_next_player()        
    
    def computer_move(self, player, event):
        if self.game.check_hand(player):
            matching_cards, color_matches, value_matches = self.find_matching_cards(player.hand, self.game.current_color, self.game.current_value)
            if matching_cards:  # Check if matching_cards is not empty
                self.game.play_card(player, matching_cards[0])
                if self.game.check_game_end(player):
                     
                    self.goToScene('end', player.get_name())
                self.game.determine_next_player()
            else:
                #! AI can't play anything after black is played. FIX LATER
                print(player.get_name(), ": No matching cards found. Drawing a card.")
                self.game.determine_next_player()
        else:
            self.game.determine_next_player()
    
    def find_matching_cards(self, hand, color, value):
        color_matches = {'red':0,'blue':0,'yellow':0,'green':0, 'black': 0}
        value_matches = 0 
        matching_cards= []
        
        for card in hand:
            if card.get_color() == self.game.current_color:
                color_matches[card.get_color()] += 1
                matching_cards.append(card)
            elif card.get_value() == self.game.current_value:
                value_matches += 1
                if card not in matching_cards:
                    matching_cards.append(card)
                    
        return matching_cards, color_matches, value_matches
    
    def draw(self):
        self.window.fill(self.back_ground_color)
        self.game.draw()
        if self.show_color_picker:
            self.red_button.draw()
            self.blue_button.draw()
            self.green_button.draw()
            self.yellow_button.draw()
        self.callUnoButton.draw() # call uno button
        self.drawCardButton.draw() # draw card button
        self.callOutButton.draw() # call out button
        
    def print_matching_cards(self, matching_cards):
        for card in matching_cards:
            print(card.get_name())    
            
