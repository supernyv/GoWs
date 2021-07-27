import pygame
import scripts.sound_effects as sfx

class Menu():
    """The main menu"""
    def __init__(self, s_game):
        """Initialize game and create resources."""
        self.screen = s_game.screen
        self.screen_rect = self.screen.get_rect()
        self.SCREENWIDTH = s_game.SCREENWIDTH
        self.buttons = s_game.buttons
        self.stats = s_game.stats
        self.game_run = False
        self.game_pause = False


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

        self._check_inputs()
    
    def _check_inputs(self):
        if self.new_game_rect.collidepoint(self.mouse_position):
            if self.buttons.pressed == True:
                self.game_pause = False
                self.game_run = True
                sfx.new_game_sound.play()
                pygame.mixer.music.stop()

                #Reset all game stats and scores here
                self.stats.reset_stats()
                self.stats.reset_news()
        
        if self.resume_game_rect.collidepoint(self.mouse_position):
            if self.buttons.pressed == True:
                self.game_pause = False

    
    def draw_main_menu(self):

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
        
    
    def draw_pause_menu(self):

        self.screen.blit(self.support_b, self.support_b_rect)
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
        

        if self.resume_game_rect.collidepoint(self.mouse_position):
            self.screen.blit(self.resume_game_selected, self.resume_game_rect)
        else:
            self.screen.blit(self.resume_game, self.resume_game_rect)
