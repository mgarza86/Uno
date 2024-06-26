import pygame
import pygwidgets
from model.card import *
from model.player import Player


class Game():
    def __init__(self,window,  players, deck, settings=None) -> None:
        super().__init__()
        self.window = window
        if settings is not None:
            self.settings = settings
        else:
            self.settings = None
        self.players_list = players
        self.discard_pile= []
        self.draw_pile = deck
        self.current_direction = 1
        self.current_color = ""
        self.current_value = ""
        self.current_player_index = 0
        self.window_width, self.window_height = self.window.get_size()
        
        # initializing the sound effects:
        self.card_flip_sound = pygwidgets.SoundEffect('sounds/cardFlip.wav')
        self.card_shuffle_sound = pygwidgets.SoundEffect('sounds/cardShuffle.wav')
        
        
                
    def initialize_players(self, number_of_cards=7):
        if self.settings is not None:
            if self.settings.sfx_enabled:
                self.card_shuffle_sound.play() # shuffle sound plays
        self.rotate_player_hands(self.players_list)
        for o_player in self.players_list:
            for _ in range(number_of_cards):
                o_player.draw_card(self.draw_pile)
            o_player.initialize_card_positions()
        
    def check_direction(self):
        return self.current_direction
    
    def check_hand(self, player):
        if len(self.discard_pile) == 0:
            print("No card in play yet")
            return True
        for i in range(len(player.hand)):
            if player.check_conditions(player.hand[i],self.current_color, self.current_value):
                return True
        #player.draw_card(self.draw_pile)
        #print(player, " drew a card")    
        return False
    
    def orientate_player(self):
        for i in range(len(self.players_list)):
            if i == 1:
                for card in self.players_list[i].hand:
                    card.flip_vertical()
    
    def rotate_player_hands(self, players):
        num_players = len(players)
        
        # For two players
        if num_players == 2:
            # Apply 180 degrees rotation to the second player's hand
            players[1].set_angle(180)
            players[1].rotate_hand(180)
            
        # For three players
        elif num_players == 3:
            players[1].set_angle(90)
            players[2].set_angle(180)
            
        # For four players
        elif num_players == 4:
            players[1].set_angle(90)
            players[2].set_angle(180)
            players[3].set_angle(270)
                
    def draw(self):
        if len(self.discard_pile) != 0:
            self.discard_pile[0].set_centered_location((self.window_width/2,self.window_height/2))
            self.discard_pile[0].draw()
        
        for i in range(len(self.players_list)):
            self.players_list[i].draw()            
        
    def discard(self, discard_pile, new_card):
        discard_pile.insert(0,new_card)

    def change_direction(self):
        self.current_direction *= -1
    
    def check_game_end(self, player):
        if len(player.hand) == 0:
            for card in self.discard_pile:
                        print(card)
            return True
        else:
            return False
    
    def determine_next_player(self, skip=False):
        self.current_player_index += self.current_direction
        self.current_player_index %= len(self.players_list)
        return self.current_player_index
    
    def play_card(self,player,card):
        if self.settings is not None:
            if self.settings.sfx_enabled:
                self.card_flip_sound.play() # flip card sound
        print(player.get_name(), " played: ", card.get_name() )
        self.discard(self.discard_pile,player.play_card(card))
        self.discard_pile[0].reveal()
        self.current_color = card.get_color()
        self.current_value = card.get_value()
        if isinstance(card,Skip):
            card.perform_action(self)
        if isinstance(card,DrawTwoCard):
            card.perform_action(self)
        if isinstance(card,Reverse):
            card.perform_action(self)
        if isinstance(card,WildPickFour):
            card.perform_action(self)
    
    def check_last_card_played(self, discard_pile):
        #print(discard_pile[0].get_name())
        return discard_pile[0]
    
    def set_current_color(self,color):
        self.current_color = color
    
    def get_player(self, index):
        return self.players_list[index]
    
    def start_game():
        pass
    
    def pick_card(self, player):
        self.sleep(1)
        if self.settings.difficulty == 'easy':
            return self.easy_ai_play_card(player)
        
        if self.settings.difficulty == 'medium':
            return self.medium_ai_play_card(player)
        
        if self.settings.difficulty == 'hard':
            return self.hard_ai_play_card(player)
    
    def find_matching_cards(self, hand):
        color_matches = {'red':0,'blue':0,'yellow':0,'green':0, 'black': 0}
        value_matches = 0 
        matching_cards= []
        
        for card in hand:
            if card.get_color() == self.current_color:
                color_matches[card.get_color()] += 1
                matching_cards.append(card)
            elif card.get_value() == self.current_value:
                value_matches += 1
                if card not in matching_cards:
                    matching_cards.append(card)
                    
        return matching_cards, color_matches, value_matches
    
    def easy_ai_play_card(self, player):
        matching_cards, color_matches, value_matches = self.find_matching_cards(player.hand)

        if not matching_cards:
            player.draw_card(self.draw_pile)
            return None
        
        return matching_cards[0]
        
    
    def medium_ai_play_card(self, player):
        matching_cards, color_matches, value_matches = self.find_matching_cards(player.hand)
        if not matching_cards:
            #no matching cards so the player needs to draw teehee
            player.draw_card(self.draw_pile)
            return None
        highest_count_color = max(color_matches, key=color_matches.get)
        
        print(f"{self.get_player}'s highest count is {highest_count_color}")
        #choose a card that helps to offload the most cards from hand
        best_card = None
        
        if color_matches[highest_count_color] > color_matches[self.current_color]:
            # pick the card that matches the highest count color
            for card in matching_cards:
                if card.color == highest_count_color:
                    best_card = card
                    break
        else:
            if not best_card:
                for card in matching_cards:
                    if card.color == self.current_color:
                        best_card = card
                        break
    
            if not best_card:
                best_card = matching_cards[0]
        
            return best_card
        
        
        
    def hard_ai_play_card(self, player):
        matching_cards, color_matches, value_matches = self.find_matching_cards(player.hand)
        if not matching_cards:
            #no matching cards, so the player needs to draw
            player.draw_card(self.draw_pile)
            return None

        #determine the next player in the sequence
        next_player_index = (self.players_list.index(player) + 1) % len(self.players_list)
        next_player = self.players_list[next_player_index]

        #prioritize action cards if the next player is human
        best_card = None
        if isinstance(next_player, Player):
            for card in matching_cards:
                if isinstance(card, (DrawTwoCard, Skip, Reverse, WildPickFour)):
                    best_card = card
                    break

        #if no action card is selected or next player is AI, goes back to medium mode
        elif not best_card:
            highest_count_color = max(color_matches, key=color_matches.get)
            if color_matches[highest_count_color] > color_matches[self.current_color]:
                for card in matching_cards:
                    if card.color == highest_count_color:
                        best_card = card
                        break

        else:
            if not best_card:
                for card in matching_cards:
                    if card.color == self.current_color:
                        best_card = card
                        break

        if not best_card:
            best_card = matching_cards[0]

        return best_card


    def sleep(self, seconds):
        # Sleep for a given number of seconds
        pygame.time.wait(seconds*500)