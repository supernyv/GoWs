import pygame
from random import choice
import scripts.sound_effects as sfx


class Letters():
    """A class to manage all the letters."""

    def __init__(self, game):
        """Create and Initialize letters position."""

        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.reset_rack()

        self.rack_x = 318
        self.rack_y = 630

        #Movement Flag
        self.selected = False
        #Sound flag
        self.played = True


    def reset_rack(self):
        self.letters = {"A" : [1, 9], "B" : [3, 2], "C" : [3, 3], "D" : [2, 3], "E" : [1, 15], 
                "F" : [4, 2], "G" : [2, 2], "H" : [4, 2], "I" : [1, 8], "J" : [8, 1], 
                "K" : [10, 1], "L" : [1, 5], "M" : [2, 4], "N" : [1, 6], "O" : [1, 6], 
                "P" : [3, 2], "Q" : [8, 1], "R" : [1, 6], "S" : [1, 6], "T" : [1, 6], 
                "U" : [1, 6], "V" : [4, 2], "W" : [10, 1], "X" : [10, 1], "Y" : [10, 1], "Z" : [10, 1]}

        self.number_letters_left = sum([number[1] for number in self.letters.values()])
        self.rack_images = []
        self.rack_letter_names = []
        self.rack_rects = []
        self.rack_centers = []


    def load_rack(self):
        """Load 7 letters images"""
        all_letters = list(self.letters.keys())

        while len(self.rack_images) < 7:
            let_b = choice(all_letters)
            if self.letters[let_b][1] > 0:
                image_b = pygame.image.load("img/"+let_b+".png").convert()
                self.rack_images.append(image_b)
                self.rack_letter_names.append(let_b)
                self.letters[let_b][1] -= 1

                image_b_rect = image_b.get_rect()
                image_b_rect.x = self.rack_x
                image_b_rect.y = self.rack_y
                self.rack_rects.append(image_b_rect)
                self.rack_centers.append(image_b_rect.center)
                self.rack_x += 34
        
        #Zip images and rectangles
        self.rack_dict = dict(zip(self.rack_images, zip(self.rack_letter_names, self.rack_rects)))
    
    def get_sack_size(self):
        """Get the number of letters left in the sack"""
        self.number_letters_left = sum([number[1] for number in self.letters.values()])

    def update_let(self):
        """Update letter position based on movement flag."""

        mouse_pos = pygame.mouse.get_pos()

        for n in range(len(self.rack_rects)):
            collision = self.rack_rects[n].collidepoint(mouse_pos)
            if collision:
                if self.selected:
                    self.rack_rects[n].center = mouse_pos
                    #To allow drop sound to play only when a tile is dropped, used self.count
                    self.played = False

                if not self.selected:
                    if self.played == False:
                        sfx.drop_letter_sound.play()
                        self.played = True


    def blit_let(self):
        """Draw the letter at its current location."""
        if self.rack_images:
            for image, name_rect in self.rack_dict.items():
                self.screen.blit(image, name_rect[1])
