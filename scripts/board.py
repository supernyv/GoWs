import pygame
import pygame.font

class Board():
    """A class to manage the game board"""

    def __init__(self, game):
        """Initialize board attributes."""

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.letters = game.let

        self.color_1 = (255, 255, 255)
        self.color_2 = (135, 206, 235)
        self.color_3 = (0, 0, 0)
        self.font_1 = pygame.font.Font("fonts/Antonio-Regular.ttf", 30)
        self.font_2 = pygame.font.Font("fonts/JosefinSans-Regular.ttf", 12)
        self.font_3 = pygame.font.Font("fonts/Antonio-Regular.ttf", 32)

        self.player_1 = True
        self.player_2 = False

        #Board
        self.board = pygame.image.load("img/GoWs_Board.png").convert()
        self.board_rect = self.board.get_rect()
        self.board_rect.center = self.screen_rect.center

        #HUD
        self.hud_player_1 = pygame.image.load("img/HUD_Player_1.png").convert()
        self.hud_player_2 = pygame.image.load("img/HUD_Player_2.png").convert()
        self.hud_rect = self.hud_player_1.get_rect()
        self.hud_rect.midtop = self.screen_rect.midtop
        self.hud_rect.y += 30

        #Rack
        self.rack = pygame.image.load("img/rack.bmp").convert()
        self.rack_rect = self.rack.get_rect()
        self.rack_rect.midtop = self.board_rect.midbottom
        self.rack_rect.y += 10

        #Replace Zone
        self.replace_zone = pygame.image.load("img/Replace_board.png").convert()
        self.replace_zone_rect = self.replace_zone.get_rect()
        self.replace_zone_rect.midright = self.board_rect.midleft
        self.replace_zone_rect.x -= 30

        #Golden letters
        self.golden_draw = pygame.image.load("img/Golden_draw.png").convert_alpha()
        self.golden_draw_rect = self.golden_draw.get_rect()
        self.golden_draw_rect.center = self.replace_zone_rect.center
        self.golden_draw_rect.y += 200
    
        #News Panel
        self.panel = pygame.image.load("img/panel.png").convert()
        self.panel.set_alpha(200)
        self.panel_rect = self.panel.get_rect()
        self.panel_rect.midleft = self.board_rect.midright
        self.panel_rect.x += 20

        #Sack
        self.sack = pygame.image.load("img/sack.png").convert_alpha()
        self.sack_rect = self.sack.get_rect()
        self.sack_rect.center = self.panel_rect.center
        self.sack_rect.y += 200

        self.reset_scores()

        self.prep_news()
        self.prep_scores()
        self.prep_sack()

    def reset_scores(self):
        self.player_1_score = 00
        self.player_2_score = 00
        self.news = ""

    def prep_news(self):
        """Initialize texts that are displayed during the game."""
        self.news_image = self.font_2.render(self.news, True, self.color_2)
        self.news_image_rect = self.news_image.get_rect()
        self.news_image_rect.center = self.panel_rect.center

    def prep_sack(self, sack_size="Full"):
        """Keep Record of the size of the sack"""
        
        self.sack_size_image = self.font_3.render(sack_size, True, self.color_3)
        self.sack_size_rect = self.sack_size_image.get_rect()
        self.sack_size_rect.center = self.news_image_rect.center
        self.sack_size_rect.y += 220
        self.sack_size_rect.x += 20
    
    def prep_scores(self):
        """Turn the score into a rendered image."""
        #Render Player 1 score
        player_1_score_str = "{:,}".format(self.player_1_score)
        self.player_1_score_image = self.font_1.render(player_1_score_str, True, self.color_1)

        #Display player 1 score.
        self.player_1_score_rect = self.player_1_score_image.get_rect()
        self.player_1_score_rect.center = self.hud_rect.center
        self.player_1_score_rect.x -= 60
    
        #Render Player 2 score
        player_2_score_str = "{:,}".format(self.player_2_score)
        self.player_2_score_image = self.font_1.render(player_2_score_str, True, self.color_1)

        #Display player 1 score.
        self.player_2_score_rect = self.player_2_score_image.get_rect()
        self.player_2_score_rect.center = self.hud_rect.center
        self.player_2_score_rect.x += 60

    def draw_board(self):
        """Draw the board on the game screen."""

        self.screen.blit(self.board, self.board_rect)
        if self.player_1:
            self.screen.blit(self.hud_player_1, self.hud_rect)
        elif self.player_2:
            self.screen.blit(self.hud_player_2, self.hud_rect)
        self.screen.blit(self.player_1_score_image, self.player_1_score_rect)
        self.screen.blit(self.player_2_score_image, self.player_2_score_rect)
        self.screen.blit(self.rack, self.rack_rect)
        self.screen.blit(self.golden_draw, self.golden_draw_rect)
        self.screen.blit(self.panel, self.panel_rect)
        self.screen.blit(self.sack, self.sack_rect)
        self.screen.blit(self.news_image, self.news_image_rect)
        self.screen.blit(self.sack_size_image, self.sack_size_rect)
        self.screen.blit(self.replace_zone, self.replace_zone_rect)

        
