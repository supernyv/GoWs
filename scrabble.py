import pygame
import numpy as np
import sys
from board import Board
from buttons import Buttons
from letters import Letters
from all_stats import ScrabbleStats
from checker import ScrabbleChecker
import sound_effects as sfx

class ScrabbleGame:
    """God of Words (GoW), by Supernyv."""
    def __init__(self):
        """Initialize game and create resources."""
        pygame.init()
        self.screen = pygame.display.set_mode((900, 700))
        pygame.display.set_caption("GoW")
        self.screen_rect = self.screen.get_rect()
        self.stats = ScrabbleStats(self)
        self.board = Board(self)
        self.buttons = Buttons(self)
        self.let = Letters(self)
        self.check = ScrabbleChecker(self)
        self.bg_color = (40, 40, 50)

        #References Grids
        self.board_grid = []
        self.board_indexes = []
        self.rack_grid = []
        self.replacer_grid =[]

        #Items moved to the board during game
        self.moved_images = []
        self.moved_rects = []
        self.moved_letters = []

        self.all_imaginary_rects = []

        #Create board array to hold played letters and empty spaces:
        self.board_array = [[' ' for col in range(15)] for row in range(15)]

        #Initial positions of rack tiles
        self.ract_init_x = [318, 352, 386, 420, 454, 488, 522]

        #First move flag
        self.started = False

        #Allowed directions flags
        self.vertical_on = False
        self.horizontal_on = False

        #pygame.mixer.music.load('sounds/Kotalogie.mp3')
        #pygame.mixer.music.play()


    def rungame(self):
        """Start the main loop of the game."""

        while True:
            self.check_events()
            self.board.prep_board()
            self.create_grids()
            self.store_reference_indexes()
            self.create_temp_array()
            
            self.let.load_rack_imgs()
            self.let.get_rack_rects()
            self.let.update_let()
            self.check_grids_letters_collision()
            self.rack_in_collisions()
            self.store_used_letters()

            self.aligned_test()
            self.starting_move()
            self.valid_follow_up()
            self.cross_words()

            self.if_any_replacement()
            self.buttons.check_play_event()
            self.buttons.check_undo_event()
            self.buttons.check_replace_event()

            self.make_the_word()
            self.zip_moved_letters()
            self.place_moved_letters()
            self.delete_imaginary_under()

            self.update_screen()


    def check_events(self):
        """Detect any input and perform some action."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.let.selected = True
                self.buttons.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.let.selected = False
                self.buttons.pressed = False


    def create_grids(self):
        """Create the reference rectangles for board and rack"""

        #Board reference grids
        x_axis = np.array([221, 251, 282, 313, 343, 374, 405, 435, 466, 497, 527, 558, 589, 619, 650])
        y_axis = np.array([v - 100 for v in x_axis])

        self.board_grid = [pygame.Rect(x, y, 29, 29) for x in x_axis for y in y_axis]
        #Before I used self.board_indexes.append((x_axis.index(x), y_axis.index(y))) for a normal list
        self.board_indexes = [((np.where(x_axis==x)[0][0], np.where(y_axis==y)[0][0])) for x in x_axis for y in y_axis]
        #Because x come first, the board is read by columns (top to bottom)

        #Rack reference grids
        new_x = np.array(list(range(318, 557, 34)))
        new_y = [630]
        self.rack_grid = [pygame.Rect(x, y, 29, 29) for x in new_x for y in new_y]


        #Replacer reference grids
        last_x = np.array(list(range(37, 137, 32)))
        last_y = np.array([330, 363])
        self.replacer_grid = [pygame.Rect(x, y, 29, 29) for x in last_x for y in last_y]


    def store_reference_indexes(self):
        """Store every board grid reference rectangle with its index."""
        rect_numbers = range(225)
        self.rect_index = dict(zip(self.board_indexes, rect_numbers))


    def create_temp_array(self):
        """Temporary array to place letters on the board."""
        self.temp_array = [[' ' for col in range(15)] for row in range(15)]


    def rack_in_collisions(self):
        """Nicer effect when rack letters collide. Optional though."""
        for p in np.array(range(len(self.let.rack_rects))):
            for n in np.array(range(len(self.let.rack_rects))):
                if n != p:
                    if self.let.rack_rects[n].collidepoint(self.let.rack_rects[p].center):
                        self.let.rack_rects[n].center = self.let.rack_centers[n]
                        self.let.rack_rects[p].center = self.let.rack_centers[p]
                        self.let.selected = False


    def _reset_used_items(self):
        """Temporarily hold the tiles to be played or replaced."""
        self.used_images = []
        self.used_rects = []
        self.used_letters = []

        self.replaced_letters = []
        self.replaced_rects = []
        self.replaced_images = []


    def check_grids_letters_collision(self):
        """Detect any collision between reference rectangles on grids and used letters rectangles."""
        #List for temporary storing letters that colide with the board
        self._reset_used_items()

        if self.let.selected == False:
        #Define what happens when a letter from rack is dropped on the board grids

            for b in np.array(range(225)):
            #We have 225 board tiles
                for l in np.array(range(len(self.let.rack_rects))):
                #and we have 7 or less rack tiles numbers depending on the bag.

                    #Collision between letters and all the board grids
                    collisions_1 = self.board_grid[b].colliderect(self.let.rack_rects[l])

                    if collisions_1:
                        self.let.rack_rects[l].center = self.board_grid[b].center

                        self.used_images.append(self.let.rack_images[l])
                        self.used_letters.append(self.let.rack_letter_names[l])
                        self.used_rects.append(self.let.rack_rects[l])

                        #Now set the value of the array grid for the index where collision happened
                        for index, rect_number in self.rect_index.items():
                            if self.board_grid.index(self.board_grid[b]) == rect_number:
                                i = index[0]
                                j = index[1]
                                self.temp_array[i][j] = self.let.rack_letter_names[l]

                        #If undo button is pressed while some letters are on the board.
                        if self.buttons.undo_event:
                            self._undo(l)


            #Define what happens when the letters from the rack are droped on the replace rack
            for rep in np.array(range(8)):
                #Replace grids number
                for l in np.array(range(len(self.let.rack_rects))):
                    collisions_3 = self.replacer_grid[rep].colliderect(self.let.rack_rects[l])

                    if collisions_3:
                        self.let.rack_rects[l].center = self.replacer_grid[rep].center
                    
                        self.replaced_images.append(self.let.rack_images[l])
                        self.replaced_letters.append(self.let.rack_letter_names[l])
                        self.replaced_rects.append(self.let.rack_rects[l])

            #Define what happens when the letters generated from letters dictionary appear on the screen.
            for r in np.array(range(8)):
            #We have 8 rack grids
                for l in np.array(range(len(self.let.rack_rects))):
                #and we have 7 letters
                    collisions_2 = self.rack_grid[r].colliderect(self.let.rack_rects[l])
                    #Collision between letters and the rack grids

                    if collisions_2:
                        self.let.rack_rects[l].center = self.rack_grid[r].center

                    if not collisions_2:
                        if self.buttons.undo_event:
                            self._undo(l)


            #Define what ahppens when rack letters drop on letters that have been locked on the board
            for l in np.array(range(len(self.let.rack_rects))):
            #Still 7 letters
                for moved in self.moved_rects:
                #Goes through all the listed board letter rectangles
                    collisions_4 = moved.colliderect(self.let.rack_rects[l])

                    if collisions_4:
                        self._undo(l)
    def _undo(self, l):
        self.let.rack_rects[l].x = self.ract_init_x[l]
        self.let.rack_rects[l].y = self.let.rack_y


    def store_used_letters(self):
        """Store image, location, letter name, and rectangle for each used letter"""
        self.used_dict = dict(zip(self.used_images, zip(self.used_letters, self.used_rects)))
        self.replaced_dict = dict(zip(self.replaced_images, zip(self.replaced_letters, self.replaced_rects)))


    def aligned_test(self):
        """To make sure all letters are aligned with the first placed on board"""
        self.aligned = []
        for rect in self.used_rects:
            if rect.x != self.used_rects[0].x:
                self.horizontal_on = False
                if rect.y != self.used_rects[0].y:
                    self.vertical_on = False
                    self.aligned.append(False)
                        
        #Once more than two letters are on the board, only one direction is allowed
        if len(self.used_rects) >= 2:
            if self.used_rects[1].x == self.used_rects[0].x:
                self.vertical_on = True
                self.horizontal_on = False
                for rect in self.used_rects[2:]:
                    if rect.x != self.used_rects[0].x:
                        self.aligned.append(False)

            elif self.used_rects[1].y == self.used_rects[0].y:
                self.horizontal_on = True
                self.vertical_on = False
                for rect in self.used_rects[2:]:
                    if rect.y != self.used_rects[0].y:
                        self.aligned.append(False)


    def starting_move(self):
        """Make sure the game proceeds only if there is tile at the board's center grid"""

        for l in np.array(range(len(self.used_rects))):
            
            collide_center = self.board_grid[112].colliderect(self.used_rects[l])
            #Collision between used letters and central board grids
            if not self.let.selected:
                if collide_center:
                    self.started = True
                        
                    if self.buttons.undo_event:
                        self.started = False
                
                    if False in self.aligned:
                        self.started = False
        #Because self.started is set to true once a collision is detected, when the collided tile is moved,
        #Self.started remains true, so next is to make sure that does not happen.
        if not self.moved_rects:
            if self.temp_array[7][7] == ' ':
                self.started = False


    def valid_follow_up(self):
        """Any subsequent letters should touch existing letters."""
        self.validate_moves = []

        #Collisions between imaginary rectangles and used rectangles:
        if self.moved_rects:
            for imaginary in self.all_imaginary_rects:
                for used in self.used_rects:
                    imaginary_collision = used.colliderect(imaginary)

                    if imaginary_collision:
                        self.validate_moves.append(True)
                    else:
                        self.validate_moves.append(False)

    
    def cross_words(self):
        """Get vertical and horizontal words"""
        self.word_found = ""
        self.empty_space_in = False

        self.words_formed_vertical = []
        self.words_formed_horizontal = []
        held_vertical = ""
        held_horizontal = ""

        for column in self.temp_array:
            column.append(' ')
            for let in column:
                if let == ' ':
                    if held_vertical:
                        self.words_formed_vertical.append(held_vertical)
                        held_vertical = ""
                else:
                    held_vertical += let

        for n in np.array(range(15)):
            for column in self.temp_array:
                column.append(' ')
                if column[n] == ' ':
                    if held_horizontal:
                        self.words_formed_horizontal.append(held_horizontal)
                        held_horizontal = ""
                else:
                    held_horizontal += column[n]

        if self.vertical_on:
            if len(self.words_formed_vertical) > 1:
                self.empty_space_in = True
            elif len(self.words_formed_vertical) == 1:
                self.word_found = self.words_formed_vertical[0]

        elif self.horizontal_on:
            if len(self.words_formed_horizontal) > 1:
                self.empty_space_in = True
            elif len(self.words_formed_horizontal) == 1:
                self.word_found = self.words_formed_horizontal[0]


    def all_played_words(self):
        """Combine temp array and main board array"""
        ...


    def if_any_replacement(self):
        """If some tiles are on the replace rack."""
        if not self.let.selected:
            if self.buttons.replace_event:

                for image, letter_rect in self.replaced_dict.items():

                    del self.let.rack_letter_names[self.let.rack_rects.index(letter_rect[1])]
                    self.let.rack_rects.remove(letter_rect[1])
                    self.let.rack_images.remove(image)
                    self.let.letters[letter_rect[0]][1] += 1
                self.buttons.replace_event = False

                #Reset rack letters positions
                x = 318
                for rect in self.let.rack_rects:
                    rect.x = x
                    x += 34
                self.let.rack_x = x


    def make_the_word(self):
        """Formed a worded using the letters placed on the board when play button is pressed
        And check whether the word is valid"""
        if not self.let.selected:

            if self.buttons.play_event:
                if self.started:
                    if self.empty_space_in == False:

                        if False not in self.aligned:
                            if len(self.moved_rects) == 0:
                                self._word_checking()
                                self.buttons.play_event = False

                            elif len(self.moved_rects) > 0:
                                if True in self.validate_moves:
                                    self._word_checking()
                                    self.buttons.play_event = False
                                    
                                elif True not in self.validate_moves:
                                    self._reset_tiles_positions()
                                    sfx.placement_sound.play()
                                    self.stats.news = f"Move not allowed!"
                                    self.board.prep_news()
                                    self.buttons.play_event = False

                        elif False in self.aligned:
                            self._reset_tiles_positions()
                            self._reset_used_items()
                            sfx.placement_sound.play()
                            self.stats.news = f"Wrong Placement"
                            self.board.prep_news()
                            self.buttons.play_event = False

                    if self.empty_space_in == True:
                        self._reset_tiles_positions()
                        sfx.placement_sound.play()
                        self.stats.news = f"Invalid Formation"
                        self.board.prep_news()
                        self.buttons.play_event = False

                elif not self.started:
                    sfx.placement_sound.play()
                    self.stats.news = f"Must touch the center!"
                    self.board.prep_news()
                    self._reset_tiles_positions()
                    self.buttons.play_event = False

            self.buttons.play_event = False


    def _reset_tiles_positions(self):
        """Reinitialize rack tiles positions."""

        for l in range(len(self.let.rack_rects)):
            self._undo(l)


    def _word_checking(self):
        try:
            points = int(self.check.check_word(self.word_found))
        except Exception:

            if self.word_found:
                for l in range(len(self.let.rack_rects)):
                    self._undo(l)
                sfx.invalid_word_sound.play()
                self.stats.news = f"{self.word_found} not valid."
                self.board.prep_news()
            else:
                pass
        else:
            sfx.valid_word_sound.play()
            self.stats.player_1_score += points
            self.stats.news = f"{self.word_found} : +{points}"

            self.board.prep_news()
            self.board.prep_scores()

            self._move_played_letters()
            self._make_imaginary_rects()


    def _move_played_letters(self):
        #Delete letters, Images, and their rectangles from rack and move them to board

        for image, letter_rect in self.used_dict.copy().items():

            self.moved_images.append(image)
            self.moved_rects.append(letter_rect[1])
            self.moved_letters.append(letter_rect[0])

            del self.let.rack_letter_names[self.let.rack_rects.index(letter_rect[1])]
            self.let.rack_rects.remove(letter_rect[1])
            self.let.rack_images.remove(image)
        
        #Reset rack letters positions
        x = 318
        for rect in self.let.rack_rects:
            rect.x = x
            x += 34
        self.let.rack_x = x


    def _make_imaginary_rects(self):
        """"All rectangles on the board will have side rectangles where subsewuent letters should be placed."""
        #Imaginary rectangles that used letters must collide with for valid moves
        #These rectangles will be generated from rectangles already on the board
        self.imaginary_top_rects = []
        self.imaginary_bottom_rects = []
        self.imaginary_left_rects = []
        self.imaginary_right_rects = []


        self.imaginary = pygame.Surface((29, 29))
        self.imaginary.set_alpha(50)
        self.imaginary.fill((50, 250, 20))

        for rectangle in self.moved_rects:
            top_rect = self.imaginary.get_rect()
            top_rect.x = rectangle.x
            top_rect.y = rectangle.y - 30
            self.imaginary_top_rects.append(top_rect)
            if top_rect not in self.all_imaginary_rects:
                self.all_imaginary_rects.append(top_rect)

            bottom_rect = self.imaginary.get_rect()
            bottom_rect.x = rectangle.x
            bottom_rect.y = rectangle.y + 32
            self.imaginary_bottom_rects.append(bottom_rect)
            if bottom_rect not in self.all_imaginary_rects:
                self.all_imaginary_rects.append(bottom_rect)

            left_rect = self.imaginary.get_rect()
            left_rect.x = rectangle.x - 30
            left_rect.y = rectangle.y
            self.imaginary_left_rects.append(left_rect)
            if left_rect not in self.all_imaginary_rects:
                self.all_imaginary_rects.append(left_rect)

            right_rect = self.imaginary.get_rect()
            right_rect.x = rectangle.x + 32
            right_rect.y = rectangle.y
            self.imaginary_right_rects.append(right_rect)
            if right_rect not in self.all_imaginary_rects:
                self.all_imaginary_rects.append(right_rect)


    def zip_moved_letters(self):
        """A dictionary to store the board letters images and rectangle for blitting."""

        self.moved_dict = dict(zip(self.moved_images, zip(self.moved_letters, self.moved_rects)))


    def place_moved_letters(self):
        """All grids with letter on top will have the value of that letter."""
        for b in np.array(range(225)):
            for let, rect in self.moved_dict.values():
                moved_collide = self.board_grid[b].colliderect(rect)

                if moved_collide:
                    for index, number in self.rect_index.items():
                        if self.board_grid.index(self.board_grid[b]) == number:
                            i = index[0]
                            j = index[1]
                            self.board_array[i][j] = let


    def delete_imaginary_under(self):
        """Delete all imaginary rectangles that are under moved rectangles"""

        for moved in self.moved_rects:
            for imaginary in self.all_imaginary_rects:
                collide_imaginary = imaginary.colliderect(moved)

                if collide_imaginary:
                    del self.all_imaginary_rects[self.all_imaginary_rects.index(imaginary)]


    def draw_played_letters(self):
        """Draw the locked letters on the board."""
        for image, let_rect in self.moved_dict.items():
            self.screen.blit(image, let_rect[1])
    

    def draw_imaginary_rects(self):

        two_coordinates = []
        if self.moved_rects:

            for im_rect in self.all_imaginary_rects:
                if (im_rect.x, im_rect.y) not in two_coordinates:
                    two_coordinates.append((im_rect.x, im_rect.y))
                    if 221 <= im_rect.x <= 681 :
                        if 121 <= im_rect.y <= 581:
                            self.screen.blit(self.imaginary, im_rect)
                #Not effectibe yet!!!!!!!!!


    def update_screen(self):
        """Update the images on the screen."""

        self.screen.fill(self.bg_color)
        self.board.draw_board()
        self.buttons.draw_buttons()
        self.draw_imaginary_rects()
        self.draw_played_letters()
        self.let.blit_let()

        pygame.display.flip()

if __name__ == "__main__":
    s_game = ScrabbleGame()
    s_game.rungame()
