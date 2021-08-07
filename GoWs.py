"""Author: Supernyv"""

import pygame
import copy, platform
from sys import exit

from scripts.menu import Menu
from scripts.board import Board
from scripts.buttons import Buttons
from scripts.letters import Letters
from scripts.checker import GoWsChecker
import scripts.sound_effects as sfx

class GoWs():
    """Game of Words (GoWs), by Supernyv."""
    def __init__(self):
        """Initialize game and create resources."""
        pygame.init()
        self.SCREENWIDTH = 900
        self.SCREENHEIGHT = 700
        self.screen = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT),0, 32)
        self.bg_color = (30, 40, 50)
        pygame.display.set_caption(f"GoWs    |    Python {platform.python_version()}    |    Pygame {pygame.version.ver}    |    SDL {'.'.join([str(v) for v in pygame.get_sdl_version()])}")
        self.screen_rect = self.screen.get_rect()
        #Order Matters here
        self.let = Letters(self)
        self.board = Board(self)
        self.check = GoWsChecker(self)
        self.buttons = Buttons(self)
        self.menu = Menu(self)

        #Items moved to the board during game
        self.moved_images = []
        self.moved_rects = []
        self.moved_letters = []
        self.words_ids = []

        #This listed will be written over but is needed here
        self.horizontal_words_list = []
        self.vertical_words_list = []

        #Imaginary rectangles
        self.all_imaginary_indexes = []
        
        #Create board array to hold played letters and empty spaces:
        self.board_array = [[{} for col in range(16)] for row in range(16)]
        #This must be 16 instead of the expected 15, see the crossword function

        #Initial positions of rack tiles
        self.ract_init_x = [318, 352, 386, 420, 454, 488, 522]

        #First move flag
        self.started = False

        #Allowed directions flags
        self.vertical_on = False
        self.horizontal_on = False


        pygame.mixer.music.load('sounds/Kotalogie.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.00, 5000)     #(-1 is loop indefinetely, delay, fade in)

        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.K_ESCAPE, pygame.K_SPACE])


    def start_game(self):
        """Start the main loop of the game."""

        self.create_grids()
        self.store_reference_indexes()

        while True:
            self.check_events()

            if self.menu.main_menu_on:
                self.menu.get_menu()

            elif not self.menu.main_menu_on:
                if self.menu.new_game == True:
                    if self.menu.watcher == 0:
                        self.new_game()
                        self.menu.watcher += 1
                    else:
                        self.continue_game()

                if self.menu.game_paused == True:
                    self.menu.get_menu()
                
                else:
                    self.continue_game()


            self.update_screen()
        pygame.quit()


    def check_events(self):
        """Detect any input and perform some action."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.let.selected = True
                    self.buttons.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.let.selected = False
                    self.buttons.pressed = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu.main_menu_on = True

                elif event.key == pygame.K_SPACE:
                    #Pause game to a menu with continue option
                    self.menu.game_paused = True


    def continue_game(self):
        """Gaming function"""

        self.let.load_rack()
        self.let.get_sack_size()
        self.board.prep_sack(str(self.let.number_letters_left))
        self.let.update_let()
        self.copy_board_array()
        self.reset_used_items()
        self.check_grids_letters_collision()
        self.rack_in_collisions()
        self.store_used_letters()

        self.aligned_test()
        self.empty_space_test()
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
        self.make_imaginary_rects()

    def new_game(self):

        #Items moved to the board during game
        self.moved_images = []
        self.moved_rects = []
        self.moved_letters = []
        self.words_ids = []

        #This listed will be written over but is needed here
        self.horizontal_words_list = []
        self.vertical_words_list = []

        #Imaginary rectangles
        self.all_imaginary_indexes = []
        self.board_array = [[{} for col in range(16)] for row in range(16)]

        self.let.rack_x = 318
        self.let.rack_y = 630


        self.board.player_1_score = 0
        self.board.player_2_score = 0
        self.board.news = ""

        self.board.prep_news()
        self.board.prep_scores()
        self.let.reset_rack()
        self.menu.watcher = 0

        #First move flag
        self.started = False

        #Allowed directions flags
        self.vertical_on = False
        self.horizontal_on = False


    def create_grids(self):
        """Create the reference rectangles for board and rack"""

        #Board reference grids
        x_axis = [221, 251, 282, 313, 343, 374, 405, 435, 466, 497, 527, 558, 589, 619, 650]
        #Would have used np.arange(221, 660, 31) if the grids were perfectly evenly spaced
        y_axis = [v - 100 for v in x_axis]

        self.board_grid = [pygame.Rect(x, y, 29, 29) for x in x_axis for y in y_axis]
        self.board_indexes = [(x, y) for x in range(15) for y in range(15)]
        #Because x come first, the board is read by columns (top to bottom)
        self.index_to_coordinates = dict(zip(self.board_indexes, self.board_grid))

        #Rack reference grids
        new_x = list(range(318, 557, 34))
        new_y = [630]
        self.rack_grid = [pygame.Rect(x, y, 29, 29) for x in new_x for y in new_y]

        #Replacer reference grids
        last_x = list(range(37, 137, 32))
        last_y = [330, 363]
        self.replacer_grid = [pygame.Rect(x, y, 29, 29) for x in last_x for y in last_y]


    def store_reference_indexes(self):
        """Store every board grid reference rectangle with its index."""
        rect_numbers = range(225)
        self.index_and_number = dict(zip(self.board_indexes, rect_numbers))


    def rack_in_collisions(self):
        """Nicer effect when rack letters collide. Optional though."""
        for p in range(len(self.let.rack_rects)):
            for n in range(len(self.let.rack_rects)):
                if n != p:
                    if self.let.rack_rects[n].collidepoint(self.let.rack_rects[p].center):
                        self.let.rack_rects[n].center = self.let.rack_centers[n]
                        self.let.rack_rects[p].center = self.let.rack_centers[p]
                        self.let.selected = False


    def reset_used_items(self):
        """Temporarily hold the tiles to be played or replaced."""
        self.used_images = []
        self.used_rects = []
        self.used_letters = []
        self.used_indexes = []

        self.replaced_letters = []
        self.replaced_rects = []
        self.replaced_images = []
    

    def copy_board_array(self):
        """Copy the board"""
        self.board_copy = copy.deepcopy(self.board_array)

    def check_grids_letters_collision(self):
        """Detect any collision between reference rectangles on grids and used letters rectangles."""
        #List for temporary storing letters that colide with the board

        if self.let.selected == False:
        #Define what happens when a letter from rack is dropped on the board grids

            for b in range(225):
            #We have 225 board tiles
                for l in range(len(self.let.rack_rects)):
                #and we have 7 or less rack tiles numbers depending on the bag.

                    #Collision between letters and all the board grids
                    collisions_1 = self.board_grid[b].colliderect(self.let.rack_rects[l])

                    if collisions_1:
                        self.let.rack_rects[l].center = self.board_grid[b].center

                        self.used_images.append(self.let.rack_images[l])
                        self.used_letters.append(self.let.rack_letter_names[l])
                        self.used_rects.append(self.let.rack_rects[l])

                        #Now set the value of the array grid for the index where collision happened
                        for index, rect_number in self.index_and_number.items():
                            if self.board_grid.index(self.board_grid[b]) == rect_number:
                                i = index[0]
                                j = index[1]

                                self.used_indexes.append([i, j])
                                let_id = str(rect_number) + '_'
                                self.board_copy[i][j][self.let.rack_letter_names[l][0]] = let_id

                        #If undo button is pressed while some letters are on the board.
                        if self.buttons.undo_event:
                            self._undo(l)


            #Define what happens when the letters from the rack are droped on the replace rack
            for rep in range(8):
                #Replace grids number
                for l in range(len(self.let.rack_rects)):
                    collisions_3 = self.replacer_grid[rep].colliderect(self.let.rack_rects[l])

                    if collisions_3:
                        self.let.rack_rects[l].center = self.replacer_grid[rep].center
                    
                        self.replaced_images.append(self.let.rack_images[l])
                        self.replaced_letters.append(self.let.rack_letter_names[l])
                        self.replaced_rects.append(self.let.rack_rects[l])

            #Define what happens when the letters generated from letters dictionary appear on the screen.
            for r in range(8):
            #We have 8 rack grids
                for l in range(len(self.let.rack_rects)):
                #and we have 7 letters
                    collisions_2 = self.rack_grid[r].colliderect(self.let.rack_rects[l])
                    #Collision between letters and the rack grids

                    if collisions_2:
                        self.let.rack_rects[l].center = self.rack_grid[r].center

                    if not collisions_2:
                        if self.buttons.undo_event:
                            self._undo(l)


            #Define what ahppens when rack letters drop on letters that have been locked on the board
            for l in range(len(self.let.rack_rects)):
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

    def empty_space_test(self):

        self.empty_space_in = False
        truth_test = []
        
        if self.used_indexes:
            x, y = self.used_indexes[0]

            for _ in range(len(self.used_indexes) - 1):
                if self.vertical_on:
                    y += 1
                    if not self.board_copy[x][y]:
                        truth_test.append(False)
                if self.horizontal_on:
                    x += 1
                    if not self.board_copy[x][y]:
                        truth_test.append(False)

        if False in truth_test:
            self.empty_space_in = True
        else:
            self.empty_space_in = False

        
    def starting_move(self):
        """Make sure the game proceeds only if there is tile at the board's center grid"""

        for l in range(len(self.used_rects)):
            
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
            if not self.board_copy[7][7]:
                self.started = False


    def valid_follow_up(self):
        """Any subsequent letters should touch existing letters."""
        self.validate_moves = []

        for index in self.used_indexes:
            if index in self.all_imaginary_indexes:
                self.validate_moves.append(True)

        if True not in self.validate_moves:
            self.validate_moves.append(False)

    
    def cross_words(self):
        """Get vertical and horizontal words"""

        self.word_found = ""

        self.words_formed_vertical = {}
        self.words_formed_horizontal = {}

        held_vertical = ""
        vertical_id = ""

        held_horizontal = ""
        horizontal_id = ""

        for column in range(16):
            #To scan from top to bottom, right to left
            for row in range(16):
                p = self.board_copy[column][row]
                if not p:
                    if held_vertical:
                        #Filter and append
                        if len(held_vertical) > 1:
                            self.words_formed_vertical[held_vertical] = vertical_id.strip('_')
                        held_vertical = ""
                        vertical_id = ""

                else:
                    held_vertical += list(p.keys())[0]
                    vertical_id += list(p.values())[0]

        #Previously added anew column to board_array to prevent attaching right edges letters to
        #Letters on the next first rows of the first column... Well, this is the easiest way to explain it.
        
        for row in range(16):
            #To scan from left to right, top to bottom
            for column in range(16):
                n = self.board_copy[column][row]
                if not n:
                    if held_horizontal:
                        #Filter and append
                        if len(held_horizontal) > 1:
                            self.words_formed_horizontal[held_horizontal] = horizontal_id.strip('_')
                        held_horizontal = ""
                        horizontal_id = ""
                else:
                    held_horizontal += list(n.keys())[0]
                    horizontal_id += list(n.values())[0]
        
        if self.words_formed_vertical:
            self.vertical_words_list = [
                word for word, w_id in self.words_formed_vertical.items() if w_id not in self.words_ids]

        if self.words_formed_horizontal:
            self.horizontal_words_list = [
                word for word, w_id in self.words_formed_horizontal.items() if w_id not in self.words_ids]


    def if_any_replacement(self):
        """If some tiles are on the replace rack."""
        count_replaced = 0

        if not self.let.selected:
            if self.buttons.replace_event:

                for image, letter_rect in self.replaced_dict.items():

                    del self.let.rack_letter_names[self.let.rack_rects.index(letter_rect[1])]
                    self.let.rack_rects.remove(letter_rect[1])
                    self.let.rack_images.remove(image)
                    self.let.letters[letter_rect[0][0]][1] += 1
                    count_replaced += 1
                self.buttons.replace_event = False
                self.board.prep_sack(str(self.let.number_letters_left))

                #Reset rack letters positions
                x = 318
                for rect in self.let.rack_rects:
                    rect.x = x
                    x += 34
                self.let.rack_x = x

        if count_replaced > 0:
            if self.board.player_1 == True:
                self.board.player_1 = False
                self.board.player_2 = True
            elif self.board.player_2 == True:
                self.board.player_1 = True
                self.board.player_2 = False


    def make_the_word(self):
        """Formed a worded using the letters placed on the board when play button is pressed
        And check whether the word is valid"""
        self.invalid_words = []
        self.valid_words = []
        self.points = 0
        self.accepted = False

        if not self.let.selected:

            if self.buttons.play_event:
                if self.started:
                    if self.empty_space_in == False:

                        if False not in self.aligned:
                            if len(self.moved_rects) == 0:
                                if self.horizontal_on:
                                    self._word_checking(self.horizontal_words_list[0])
                                elif self.vertical_on:
                                    self._word_checking(self.vertical_words_list[0])

                                self._confirmed_or_rejected()
                                self.buttons.play_event = False

                            elif len(self.moved_rects) > 0:
                                if True in self.validate_moves:
                                    if self.horizontal_on:
                                        for word in self.horizontal_words_list:
                                            self._word_checking(word)
                                        for word in self.vertical_words_list:
                                            self._word_checking(word)

                                    elif self.vertical_on:
                                        for word in self.vertical_words_list:
                                            self._word_checking(word)
                                        for word in self.horizontal_words_list:
                                            self._word_checking(word)

                                    else:
                                        for word in self.horizontal_words_list:
                                            self._word_checking(word)
                                        for word in self.vertical_words_list:
                                            self._word_checking(word)

                                    self._confirmed_or_rejected()
                                    self.buttons.play_event = False
                                    
                                elif True not in self.validate_moves:
                                    self._reset_tiles_positions()
                                    sfx.placement_sound.play()
                                    self.board.news = f"Missed contact!"
                                    self.board.prep_news()
                                    self.buttons.play_event = False

                        elif False in self.aligned:
                            self._reset_tiles_positions()
                            sfx.placement_sound.play()
                            self.board.news = f"Wrong Alignment!"
                            self.board.prep_news()
                            self.buttons.play_event = False

                    elif self.empty_space_in == True:
                        self._reset_tiles_positions()
                        sfx.placement_sound.play()
                        self.board.news = f"Multiple words!"
                        self.board.prep_news()
                        self.buttons.play_event = False

                elif not self.started:
                    sfx.placement_sound.play()
                    self.board.news = f"Missed the board center!"
                    self.board.prep_news()
                    self._reset_tiles_positions()
                    self.buttons.play_event = False

            self.buttons.play_event = False


    def _reset_tiles_positions(self):
        """Reinitialize rack tiles positions."""

        for l in range(len(self.let.rack_rects)):
            self._undo(l)


    def _word_checking(self, word):

        try:
            self.points += int(self.check.check_word(word))
                    
        except Exception:
            if word:
                self.invalid_words.append(word)
            else:
                pass
        else:
            self.valid_words.append(word)


    def _confirmed_or_rejected(self):

        if len(self.invalid_words) > 0:
            for l in range(len(self.let.rack_rects)):
                self._undo(l)
            sfx.invalid_word_sound.play()
            self.board.news = f"{self.invalid_words[0]} not valid."
            self.board.prep_news()
            self.accepted = False

        elif len(self.invalid_words) == 0:
            if self.valid_words:
                self.accepted = True
                sfx.valid_word_sound.play()

                if self.board.player_1 == True:
                    self.board.player_1_score += self.points
                    self.board.player_1 = False
                    self.board.player_2 = True

                elif self.board.player_2 == True:
                    self.board.player_2_score += self.points
                    self.board.player_1 = True
                    self.board.player_2 = False

                self.board.news = f"{self.valid_words[0]} : + {self.points}"

                self.board.prep_news()
                self.board.prep_scores()

                self._move_played_letters()

            else:
                for l in range(len(self.let.rack_rects)):
                    self._undo(l)
                sfx.invalid_word_sound.play()
                self.board.news = f"No valid words."
                self.board.prep_news()
                self.accepted = False


    def _move_played_letters(self):
        #Delete letters, Images, and their rectangles from rack and move them to board
        for image, letter_and_rect in self.used_dict.items():

            self.moved_images.append(image)
            self.moved_rects.append(letter_and_rect[1])
            self.moved_letters.append(letter_and_rect[0])

            del self.let.rack_letter_names[self.let.rack_rects.index(letter_and_rect[1])]
            self.let.rack_rects.remove(letter_and_rect[1])
            self.let.rack_images.remove(image)
        
        #Reset rack letters positions
        x = 318
        for rect in self.let.rack_rects:
            rect.x = x
            x += 34
        self.let.rack_x = x


    def make_imaginary_rects(self):
        """"All rectangles on the board will have side rectangles where subsewuent letters should be placed."""
        #Imaginary rectangles that used letters must collide with for valid moves
        #These rectangles will be generated from rectangles already on the board

        self.imaginary = pygame.Surface((29, 29)).convert()
        self.imaginary.set_alpha(50)
        self.imaginary.fill((50, 250, 20))

        self.imaginary_rectangles = []

        for i in range(15):
            for j in range(15):
                if self.board_array[i][j]:
                    if i == 0:
                        if not self.board_array[i+1][j]:
                            self.imaginary_rectangles.append(self.index_to_coordinates[(i+1, j)])
                            self.all_imaginary_indexes.append([i+1, j])
                    elif i == 14:
                        if not self.board_array[i-1][j]:
                            self.imaginary_rectangles.append(self.index_to_coordinates[(i-1, j)])
                            self.all_imaginary_indexes.append([i-1, j])
                    else:
                        if not self.board_array[i+1][j]:
                            self.imaginary_rectangles.append(self.index_to_coordinates[(i+1, j)])
                            self.all_imaginary_indexes.append([i+1, j])
                        if not self.board_array[i-1][j]:
                            self.imaginary_rectangles.append(self.index_to_coordinates[(i-1, j)])
                            self.all_imaginary_indexes.append([i-1, j])

                    if j == 0:
                        if not self.board_array[i][j+1]:
                            self.imaginary_rectangles.append(self.index_to_coordinates[(i, j+1)])
                            self.all_imaginary_indexes.append([i, j+1])
                    elif j == 14:
                        if not self.board_array[i][j-1]:
                            self.imaginary_rectangles.append(self.index_to_coordinates[(i, j-1)])
                            self.all_imaginary_indexes.append([i, j-1])
                    else:
                        if not self.board_array[i][j+1]:
                            self.imaginary_rectangles.append(self.index_to_coordinates[(i, j+1)])
                            self.all_imaginary_indexes.append([i, j+1])
                        if not self.board_array[i][j-1]:
                            self.imaginary_rectangles.append(self.index_to_coordinates[(i, j-1)])
                            self.all_imaginary_indexes.append([i, j-1])


    def zip_moved_letters(self):
        """A dictionary to store the board letters images and rectangle for blitting."""

        self.moved_dict = dict(zip(self.moved_images, zip(self.moved_letters, self.moved_rects)))


    def place_moved_letters(self):
        """All grids with letter tile on top will have the value of that letter."""


        for b in range(225):
            for let, rect in self.moved_dict.values():
                moved_collide = self.board_grid[b].colliderect(rect)

                if moved_collide:
                    for index, number in self.index_and_number.items():
                        if self.board_grid.index(self.board_grid[b]) == number:
                            i = index[0]
                            j = index[1]

                            letter_id = str(number) + '_'
                            self.board_array[i][j][let[0]] = letter_id

        if self.accepted == True:
            for id_a in self.words_formed_horizontal.values():
                if id_a not in self.words_ids:
                    self.words_ids.append(id_a)
        
            for id_b in self.words_formed_vertical.values():
                if id_b not in self.words_ids:
                    self.words_ids.append(id_b)


    def draw_played_letters(self):
        """Draw the locked letters on the board."""
        for image, let_rect in self.moved_dict.items():
            self.screen.blit(image, let_rect[1])
    

    def draw_imaginary_rects(self):

        if self.moved_rects:

            for im_rect in self.imaginary_rectangles:
                if 221 <= im_rect.x <= 681 :
                    if 121 <= im_rect.y <= 581:
                        self.screen.blit(self.imaginary, im_rect)


    def update_screen(self):
        """Update the images on the screen."""

        self.screen.fill(self.bg_color)

        if self.menu.main_menu_on:
            self.menu.draw_menu()

        else:
            if self.menu.new_game == True:
                self.board.draw_board()
                self.buttons.draw_buttons()
                if self.moved_images:
                    self.draw_imaginary_rects()
                    self.draw_played_letters()
                self.let.blit_let()

            if self.menu.game_paused == True:
                self.menu.draw_menu()

            else:
                self.board.draw_board()
                self.buttons.draw_buttons()
                if self.moved_images:
                    self.draw_imaginary_rects()
                    self.draw_played_letters()
                self.let.blit_let()

        pygame.display.update()

if __name__ == "__main__":
    game = GoWs()
    game.start_game()
