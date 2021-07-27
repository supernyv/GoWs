import pygame
import pygame.font

class Board():
    """A class to manage the game board"""

    def __init__(self, s_game):
        """Initialize board attributes."""

        self.screen = s_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = s_game.stats

        self.color_1 = (255, 255, 255)
        self.color_2 = pygame.Color((135, 206, 235))
        self.font_1 = pygame.font.Font("fonts/Antonio-Regular.ttf", 30)
        self.font_2 = pygame.font.Font("fonts/JosefinSans-Regular.ttf", 12)

        self.player_1 = True
        self.player_2 = False

        #These functions return nothing and do not modify any class attribute
        #So they need to be called now ?
        self.prep_board()
        self.prep_hud()
        self.prep_rack()
        self.prep_replace_zone()
        self.prep_news_panel()
        self.prep_golden_draw()
        self.prep_scores()
        self.prep_news()

    def prep_board(self):
        self.board = pygame.image.load("img/GoWs_Board.png")
        self.board_rect = self.board.get_rect()
        self.board_rect.center = self.screen_rect.center

    def prep_hud(self):
        self.hud_player_1 = pygame.image.load("img/HUD_Player_1.png")
        self.hud_player_2 = pygame.image.load("img/HUD_Player_2.png")
        self.hud_rect = self.hud_player_1.get_rect()
        self.hud_rect.midtop = self.screen_rect.midtop
        self.hud_rect.y += 30

    def prep_rack(self):
        self.rack = pygame.image.load("img/rack.bmp")
        self.rack_rect = self.rack.get_rect()
        self.rack_rect.midtop = self.board_rect.midbottom
        self.rack_rect.y += 10
    
    def prep_golden_draw(self):
        """The golden letters drawer."""
        self.golden_draw = pygame.image.load("img/Golden_draw.png")
        self.golden_draw_rect = self.golden_draw.get_rect()
        self.golden_draw_rect.center = self.replace_zone_rect.center
        self.golden_draw_rect.y += 200

    def prep_replace_zone(self):
        """Create the replace rack"""
        self.replace_zone = pygame.image.load("img/Replace_board.png")
        self.replace_zone_rect = self.replace_zone.get_rect()
        self.replace_zone_rect.midright = self.board_rect.midleft
        self.replace_zone_rect.x -= 30
    
    def prep_news_panel(self):
        """Create the game info panel."""
        self.panel = pygame.image.load("img/panel.png")
        self.panel.set_alpha(200)
        self.panel_rect = self.panel.get_rect()
        self.panel_rect.midleft = self.board_rect.midright
        self.panel_rect.x += 20
    
    def prep_news(self):
        """Initialize texts that are displayed during the game."""
        news = self.stats.news
        self.news_image = self.font_2.render(news, True, self.color_2)
        self.news_image_rect = self.news_image.get_rect()
        self.news_image_rect.center = self.panel_rect.center
    
    def prep_scores(self):
        """Turn the score into a rendered image."""
        #Render Player 1 score
        player_1_score = self.stats.player_1_score
        player_1_score_str = "{:,}".format(player_1_score)
        self.player_1_score_image = self.font_1.render(player_1_score_str, True, self.color_1)

        #Display player 1 score.
        self.player_1_score_rect = self.player_1_score_image.get_rect()
        self.player_1_score_rect.center = self.hud_rect.center
        self.player_1_score_rect.x -= 60
    
        #Render Player 2 score
        player_2_score = self.stats.player_2_score
        player_2_score_str = "{:,}".format(player_2_score)
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
        self.screen.blit(self.news_image, self.news_image_rect)
        self.screen.blit(self.replace_zone, self.replace_zone_rect)

        
