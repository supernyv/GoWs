import pygame
import scripts.sound_effects as sfx
import webbrowser as wb

class Menu():
    """The main menu"""
    def __init__(self, game):
        """Initialize game and create resources."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.SCREENWIDTH = game.SCREENWIDTH
        self.buttons = game.buttons
        self.new_game = False
        self.game_paused = False
        self.main_menu_on = True

        self.like_active = False
        self.like_event = False
        self.like_counter = 0
        self.watcher = 0



    def get_menu(self):

        self.mouse_position = pygame.mouse.get_pos()

        self.options = pygame.image.load("img/options.png").convert_alpha()
        self.options_selected = pygame.image.load("img/options_selected.png").convert_alpha()
        self.options_rect = self.options.get_rect()
        self.options_rect.center = self.screen_rect.center


        self.new_game = pygame.image.load("img/new_game.png").convert_alpha()
        self.new_game_selected = pygame.image.load("img/new_game_selected.png").convert_alpha()
        self.new_game_rect = self.new_game.get_rect()
        self.new_game_rect.center = self.options_rect.center
        self.new_game_rect.y = self.options_rect.y - 65

        self.resume_game = pygame.image.load("img/resume.png").convert_alpha()
        self.resume_game_selected = pygame.image.load("img/resume_selected.png").convert_alpha()
        self.resume_game_rect = self.resume_game.get_rect()
        self.resume_game_rect.center = self.options_rect.center
        self.resume_game_rect.y = self.new_game_rect.y - 65

        self.credits = pygame.image.load("img/credits.png").convert_alpha()
        self.credits_selected = pygame.image.load("img/credits_selected.png").convert_alpha()
        self.credits_rect = self.credits.get_rect()
        self.credits_rect.center = self.options_rect.center
        self.credits_rect.y = self.options_rect.y + 65

        self.support = pygame.Surface((350, 215))
        self.support.set_alpha(10)
        self.support.fill((255, 255, 255))
        self.support_rect = self.support.get_rect()
        self.support_rect.center = self.options_rect.center

        self.support_b = pygame.Surface((350, 250))
        self.support_b.set_alpha(10)
        self.support_b.fill((255, 255, 255))
        self.support_b_rect = self.support_b.get_rect()
        self.support_b_rect.center = self.screen_rect.center
        self.support_b_rect.y -= 40

        #Logo
        self.logo = pygame.image.load("img/logo.png").convert_alpha()
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (self.screen_rect.x + self.SCREENWIDTH/2, self.screen_rect.y + 100)

        self.logo_support = pygame.Surface((200, 120))
        self.logo_support.set_alpha(10)
        self.logo_support.fill((255, 255, 255))
        self.logo_support_rect = self.logo_support.get_rect()
        self.logo_support_rect.center = self.logo_rect.center

        #Like button
        self.like = pygame.image.load("img/Like.png").convert_alpha()
        self.like_pressed = pygame.image.load("img/Like_pressed.png").convert_alpha()
        self.like_rect = self.like.get_rect()
        self.like_rect.center = self.logo_rect.center
        self.like_rect.y = 500 

        self._check_inputs()
    
    def _check_inputs(self):
        if self.new_game_rect.collidepoint(self.mouse_position):
            if self.buttons.pressed == True:
                self.watcher = 0
                self.game_paused = False
                self.main_menu_on = False
                self.new_game = True
                sfx.new_game_sound.play()
                pygame.mixer.music.stop()

        
        if self.resume_game_rect.collidepoint(self.mouse_position):
            if self.buttons.pressed == True:
                self.main_menu_on = False
                self.game_paused = False    #Game continuing

        
        if self.buttons.pressed:
            if self.like_rect.collidepoint(self.mouse_position):
                self.like_counter = 1
                self.like_event = True
                self.like_active = True

            else:
                self.play_event = False
                self.play_active = False
        else:
            if self.like_counter == 1:
                wb.get("windows-default").open("http://facebook.com/congo3d/")
                self.like_counter = 0
            self.like_active = False


    
    def draw_menu(self):

        self.screen.blit(self.support, self.support_rect)
        self.screen.blit(self.logo_support, self.logo_support_rect)
        self.screen.blit(self.logo, self.logo_rect)


        if self.new_game_rect.collidepoint(self.mouse_position):
            self.screen.blit(self.new_game_selected, self.new_game_rect)
        else:
            self.screen.blit(self.new_game, self.new_game_rect)
        
        if self.options_rect.collidepoint(self.mouse_position):
            self.screen.blit(self.options_selected, self.options_rect)
        else:
            self.screen.blit(self.options, self.options_rect)
        
        if self.credits_rect.collidepoint(self.mouse_position):
            self.screen.blit(self.credits_selected, self.credits_rect)
        else:
            self.screen.blit(self.credits, self.credits_rect)

        if self.like_active:
            self.screen.blit(self.like_pressed, self.like_rect)
        elif not self.like_active:
            self.screen.blit(self.like, self.like_rect)


        if self.game_paused:
            if self.resume_game_rect.collidepoint(self.mouse_position):
                self.screen.blit(self.resume_game_selected, self.resume_game_rect)
            else:
                self.screen.blit(self.resume_game, self.resume_game_rect)
