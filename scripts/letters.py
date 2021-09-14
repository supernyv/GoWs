import pygame
from random import choice, choices
import scripts.sound_effects as sfx


class Letters():
    """A class to manage all the letters."""

    def __init__(self, game):
        """Create and Initialize letters position."""

        self.screen = game.screen

        self.reset_rack()
        self.get_letters_and_weights()

        self.rack_x = 318
        self.rack_y = 630

        #Movement Flag
        self.selected = False
        #Sound flag
        self.tile_lifted = False


    def reset_rack(self):
        self.letters = {"A" : [1, 9], "B" : [3, 2], "C" : [3, 3], "D" : [2, 3], "E" : [1, 15], 
                "F" : [4, 2], "G" : [2, 2], "H" : [4, 2], "I" : [1, 8], "J" : [8, 1], 
                "K" : [10, 1], "L" : [1, 5], "M" : [2, 4], "N" : [1, 6], "O" : [1, 6], 
                "P" : [3, 2], "Q" : [8, 1], "R" : [1, 6], "S" : [1, 6], "T" : [1, 6], 
                "U" : [1, 6], "V" : [4, 2], "W" : [10, 1], "X" : [10, 1], "Y" : [10, 1], "Z" : [10, 1]}

        self.rack_images = []
        self.rack_letter_names = []
        self.rack_rects = []
        self.rack_centers = []
        self.selected_letter_name = ""
        self.selected_letter_old_rect = pygame.Rect((0, 0), (29, 29))


    def load_rack(self):
        """Load 7 letters images"""

        full = 7
        required = full - len(self.rack_images)
        
        if self.number_letters_left > 0:
            for _ in range(required):
                let = next(iter(choices(self.all_letters, self.letters_probabilities, k=1)))
                if self.letters[let][1] > 0:
                    image = pygame.image.load("img/"+let+".png").convert()
                    self.rack_images.append(image)
                    self.rack_letter_names.append(let)
                    self.letters[let][1] -= 1

                    image_rect = image.get_rect()
                    image_rect.x = self.rack_x
                    image_rect.y = self.rack_y
                    self.rack_rects.append(image_rect)
                    self.rack_centers.append(image_rect.center)
                    self.rack_x += 34
        else:
            #Game ends
            pass
        
        #Zip images and rectangles
        self.rack_dict = dict(zip(self.rack_images, zip(self.rack_letter_names, self.rack_rects)))
    

    def get_sack_size(self):
        """Get the number of letters left in the sack"""
        self.number_letters_left = sum([number[1] for number in self.letters.values()])


    def get_letters_and_weights(self):
        """List all letters and their weight for better selection using random choice"""
        self.all_letters = list(self.letters.keys())
        rare_letters = ("J", "K," "Q", "W", "X", "Y", "Z")
        vowels = ("A", "E", "I", "O", "U")
        self.letters_probabilities = [2 if let in rare_letters 
        else 20 if let in vowels
        else 10 for let in self.all_letters]
        # It should be more likely to get vowels, then letters that are not heavy than the rest


    def update_let(self):
        """Update letter position based on movement flag."""

        mouse_pos = pygame.mouse.get_pos()

        if self.selected:
            for n in range(len(self.rack_rects)):
                collision = self.rack_rects[n].collidepoint(mouse_pos)
                if collision:
                    self.tile_lifted = True
                    self.rack_rects[n].center = mouse_pos
                    self.selected_letter_name = self.rack_letter_names[n]
                    self.selected_letter_old_rect = self.rack_rects[n]

        #To allow drop sound to play only when a tile is dropped
        if not self.selected:
            if self.tile_lifted:
                sfx.drop_letter_sound.play()
                self.tile_lifted = False
                self.selected_letter_name = ""
                self.selected_letter_old_rect = pygame.Rect((0, 0), (29, 29))

        if self.selected_letter_name:
            self._bring_selected_letter_upward()

    def _bring_selected_letter_upward(self):
        """When a letter is select, load another copy of it to scale and blit on the forefront"""
        new_image = pygame.image.load(f"img/{self.selected_letter_name}.png").convert()
        self.selected_letter_image = pygame.transform.scale(new_image, (34, 34))
        self.selected_letter__new_rect = self.selected_letter_image.get_rect()
        self.selected_letter__new_rect.center = self.selected_letter_old_rect.center


    def blit_let(self):
        """Draw the letter at its current location."""
        if self.rack_images:
            for image, name_rect in self.rack_dict.items():
                if name_rect[1] != self.selected_letter_old_rect:
                    self.screen.blit(image, name_rect[1])

            if self.selected_letter_name:
                self.screen.blit(self.selected_letter_image, self.selected_letter__new_rect)
