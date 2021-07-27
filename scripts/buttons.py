import pygame

import scripts.sound_effects as sfx

class Buttons():
    """A class to manage all game buttons."""

    def __init__(self, s_game):
        """Create and Initialize buttons positions"""

        self.screen = s_game.screen
        self.screen_rect = self.screen.get_rect()
        self.board = s_game.board

        self.play_active = False
        self.play_event = False

        #Play Button, not clicked
        self.play_button = pygame.image.load("img/Play_Button.png").convert_alpha()
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.center = self.screen_rect.center
        self.play_button_rect.x += 200
        self.play_button_rect.y += 295
        #Play Button, clicked
        self.play_button_active = pygame.image.load("img/Play_Button_active.png").convert_alpha()
        self.play_button_active_rect = self.play_button_rect

        self.undo_active = False
        self.undo_event = False

        #Undo Button, when not clicked on
        self.undo_button = pygame.image.load("img/Undo_Button.png").convert_alpha()
        self.undo_button_rect = self.undo_button.get_rect()
        self.undo_button_rect.center = self.screen_rect.center
        self.undo_button_rect.x -= 200
        self.undo_button_rect.y = self.play_button_rect.y
        #Undo Button, when clicked on
        self.undo_button_active = pygame.image.load("img/Undo_Button_active.png").convert_alpha()
        self.undo_button_rect_active = self.undo_button_rect

        self.replace_active = False
        self.replace_event = False

        #Replace Letters Button, when not clicked on
        self.replace_button = pygame.image.load("img/Replace_off.png").convert()
        self.replace_button_rect = self.replace_button.get_rect()
        self.replace_button_rect.midtop = self.board.replace_zone_rect.midtop
        self.replace_button_rect.y += 7
        #Replace Letters Button, when clicked on
        self.replace_button_on = pygame.image.load("img/Replace_on.png").convert()
        self.replace_button_on_rect = self.replace_button_rect

        #Pressing Flag
        self.pressed = False

    def check_undo_event(self):
        """When the mouse is clicked on the undo button, 
        trigger undo events, else set them to false"""

        mouse_pos = pygame.mouse.get_pos()
        undo_collision = self.undo_button_rect.collidepoint(mouse_pos)

        if self.pressed:
            if undo_collision:
                self.undo_event = True
                self.undo_active = True
                sfx.undo_sound.play()

            if not undo_collision:
                self.undo_event = False
                self.undo_active = False
                
        else:
            self.undo_active = False

    def check_play_event(self):
        """When the play button is pressed, set play fonctions to true."""
        mouse_pos = pygame.mouse.get_pos()
        play_collision = self.play_button_rect.collidepoint(mouse_pos)

        if self.pressed:
            if play_collision:
                self.play_event = True
                self.play_active = True
            if not play_collision:
                self.play_event = False
                self.play_active = False
        else:
            self.play_active = False

    def check_replace_event(self):
        """When the mouse is clicked on the replace button, 
        trigger replace events, else set them to false"""

        mouse_pos = pygame.mouse.get_pos()
        replace_collision = self.replace_button_rect.collidepoint(mouse_pos)

        if self.pressed:
            if replace_collision:
                sfx.replace_sound.play()
                self.replace_event = True
                self.replace_active = True
            if not replace_collision:
                self.replace_event = False
                self.replace_active = False
        else:
            if replace_collision:
                self.replace_active = False

    def draw_buttons(self):
        """Draw all the buttons on the game screen."""

        if self.play_active:
            self.screen.blit(self.play_button_active, self.play_button_active_rect)
        elif not self.play_active:
            self.screen.blit(self.play_button, self.play_button_rect)
    
        if self.undo_active:
            self.screen.blit(self.undo_button_active, self.undo_button_rect_active)
        elif not self.undo_active:
            self.screen.blit(self.undo_button, self.undo_button_rect)
        
        if self.replace_active:
            self.screen.blit(self.replace_button_on, self.replace_button_on_rect)
        elif not self.replace_active:
            self.screen.blit(self.replace_button, self.replace_button_rect)
