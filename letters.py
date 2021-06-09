import pygame
from random import choice
import sound_effects as sfx


class Letters:
    """A class to manage all the letters."""

    def __init__(self, s_game):
        """Create and Initialize letters position."""

        self.screen = s_game.screen
        self.screen_rect = s_game.screen.get_rect()

        self.letters = {"A" : [1, 9], "B" : [3, 2], "C" : [3, 3], "D" : [2, 3], "E" : [1, 15], 
                "F" : [4, 2], "G" : [2, 2], "H" : [4, 2], "I" : [1, 8], "J" : [8, 1], 
                "K" : [10, 1], "L" : [1, 5], "M" : [2, 4], "N" : [1, 6], "O" : [1, 6], 
                "P" : [3, 2], "Q" : [8, 1], "R" : [1, 6], "S" : [1, 6], "T" : [1, 6], 
                "U" : [1, 6], "V" : [4, 2], "W" : [10, 1], "X" : [10, 1], "Y" : [10, 1], "Z" : [10, 1]}
        #Increase M and C numbers by 1 to account for empty letters

        self.number_letters_left = sum([number[1] for number in self.letters.values()])

        self.rack_images = []
        self.rack_letter_names = []
        self.rack_rects = []
        self.rack_centers = []

        self.rack_x = 318
        self.rack_y = 630

        #Movement Flag
        self.selected = False

        self.count = 1

    def load_rack_imgs(self):
        """Load 7 letters images"""

        self.temp_images = []
        self.temp_letters = []

        if self.number_letters_left > 7:

            if len(self.rack_images) == 0:
            #Only load 3 letters disregarding their number in the bag
                while len(self.rack_images) < 4:
                    let_a = choice(list(self.letters.keys()))
                    if self.letters[let_a][1] > 0:
                        image_a = pygame.image.load("img/"+let_a+".png").convert()
                        self.rack_images.append(image_a)
                        self.rack_letter_names.append(let_a)
                        self.letters[let_a][1] -= 1

                while len(self.rack_images) < 7:
                    let_b = choice(list(self.letters.keys()))
                    if self.letters[let_b][1] > 2:
                        image_b = pygame.image.load("img/"+let_b+".png").convert()
                        self.rack_images.append(image_b)
                        self.rack_letter_names.append(let_b)
                        self.letters[let_b][1] -= 1


            elif len(self.rack_images) > 0 :
                while len(self.temp_images) < 7 - len(self.rack_images):
                    let_c = choice(list(self.letters.keys()))
                    if self.letters[let_c][1] > 0:
                        image_c = pygame.image.load("img/"+let_c+".png").convert()
                        self.temp_images.append(image_c)
                        self.temp_letters.append(let_c)
                        self.letters[let_c][1] -= 1

                self.rack_images += self.temp_images
                self.rack_letter_names += self.temp_letters

        self.number_letters_left = sum([number[1] for number in self.letters.values()])

    def get_rack_rects(self):
        """Draw the loaded images rectangles on the rack."""

        self.temp_rects = []
        self.temp_centers = []
        
        if self.number_letters_left > 7:
            if len(self.rack_rects) == 0:
                while len(self.rack_rects) < 7:
                    for let in self.rack_images:
                        let_rect = let.get_rect()
                        let_rect.x = self.rack_x
                        let_rect.y = self.rack_y
                        self.rack_rects.append(let_rect)
                        self.rack_centers.append(let_rect.center)
                        self.rack_x += 34

            elif len(self.rack_rects) > 0:
                while len(self.temp_rects) < 7 - len(self.rack_rects):
                    for let in self.temp_images:
                        let_rect = let.get_rect()
                        let_rect.x = self.rack_x
                        let_rect.y = self.rack_y
                        self.temp_rects.append(let_rect)
                        self.temp_centers.append(let_rect.center)
                        self.rack_x += 34

                self.rack_rects += self.temp_rects
                self.rack_centers += self.temp_centers
        
        #Zip images and rectangles
        self.rack_dict = dict(zip(self.rack_images, zip(self.rack_letter_names, self.rack_rects)))

    def update_let(self):
        """Update letter position based on movement flag."""

        mouse_pos = pygame.mouse.get_pos()

        for n in range(len(self.rack_rects)):
            collision = self.rack_rects[n].collidepoint(mouse_pos)
            if collision:
                if self.selected:
                    self.rack_rects[n].center = mouse_pos
                    #To allow drop sound to play only when a tile is dropped, used self.count
                    self.count = 0

                if not self.selected:
                    if self.count == 0:
                        sfx.drop_letter_sound.play()
                        self.count += 1

    def blit_let(self):
        """Draw the letter at its current location."""
        for image, name_rect in self.rack_dict.items():
            self.screen.blit(image, name_rect[1])
