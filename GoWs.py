"""Author: Supernyv"""

import pygame
import platform
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
        icon = pygame.image.load("img/icon.png")
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT),0, 32)
        pygame.display.set_caption(f"GoWs    |    Python {platform.python_version()}    |    Pygame {pygame.version.ver}    |    SDL {'.'.join([str(v) for v in pygame.get_sdl_version()])}")
        self.screen_rect = self.screen.get_rect()
        self.bg_color = (40, 50, 60)
        self.imaginary_color = (100, 255, 0)
        self.clock = pygame.time.Clock()

        #Order Matters here
        self.let = Letters(self)
        self.board = Board(self)
        self.check = GoWsChecker(self)
        self.buttons = Buttons(self)
        self.menu = Menu(self)


        #Imaginary rectangles
        self.imaginary_surface = pygame.Surface((29, 29)).convert()
        self.imaginary_surface.set_alpha(50)
        self.imaginary_surface.fill(self.imaginary_color)

        self.imaginary_rectangles = []
        self.all_imaginary_indexes = []

        self.new_game()

        #Initial positions of rack tiles
        self.ract_init_x = [318, 352, 386, 420, 454, 488, 522]

        self.create_board_rectangles()


        pygame.mixer.music.load('sounds/Kotalogie.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.00, 5000)     #(-1 is loop indefinetely, delay, fade in)

        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.K_ESCAPE, pygame.K_SPACE])


    def create_board_rectangles(self):
        """The reference grids that will be used in the game"""
        #Board reference grids
        x_coordinates = [221, 251, 282, 313, 343, 374, 405, 435, 466, 497, 527, 558, 589, 619, 650]
        #Would have used np.arange(221, 660, 31) if the grids were perfectly evenly spaced
        y_coordinates = [v - 100 for v in x_coordinates]

        self.board_rectangles = [pygame.Rect(x, y, 29, 29) for x in x_coordinates for y in y_coordinates]
        self.board_indexes = [(x, y) for x in range(15) for y in range(15)]
        #Because x come first, the board is read by columns (top to bottom)
        self.index_to_rectangle = dict(zip(self.board_indexes, self.board_rectangles))

        #Rack reference grid rectangles
        new_x = range(318, 557, 34)
        new_y = [630]
        self.rack_rectangles = [pygame.Rect(x, y, 29, 29) for x in new_x for y in new_y]

        #Replacer reference grids
        last_x = range(37, 137, 32)
        last_y = [330, 363]
        self.replacer_grid = [pygame.Rect(x, y, 29, 29) for x in last_x for y in last_y]

        #Store every board grid reference rectangle with its index.
        rect_numbers = range(225)
        self.number_to_index = dict(zip(rect_numbers, self.board_indexes))
        #Try self.index_coordinates_number


    def start_game(self):
        """Start the main loop of the game."""

        while True:
            self.check_events()

            if self.menu.main_menu_on:
                self.menu.get_menu()

            else:
                if self.menu.new_game_event == True:
                    if self.menu.game_reset == False:
                        self.new_game()
                        self.menu.game_reset = True
                    else:
                        self.continue_game()

                if self.menu.game_paused == True:
                    self.menu.get_menu()

                else:
                    self.continue_game()

            self.update_screen()
            pygame.display.update()


    def check_events(self):
        """Detect any input and perform some action."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
                    self.transition_fall()
                    self.menu.main_menu_on = True

                elif event.key == pygame.K_SPACE:
                    #Pause game to a menu with continue option
                    self.transition_fade()
                    self.menu.game_paused = True


    def new_game(self):
        """(Re)Initialize all game dynamic parameters"""

        #Items moved to the board during game
        self.moved_dict = {}
        self.words_ids = []

        #This listed will be written over but is needed here
        self.horizontal_words_list = []
        self.vertical_words_list = []

        self.double_word_tiles = [
        18, 26, 32, 42, 46, 58, 64, 70, 96, 98, 
        126, 128, 154, 160, 166, 178, 182, 192, 198, 206
         ]

        self.triple_word_tiles = [4, 10, 60, 74, 150, 164, 214, 220]

        self.double_letter_tiles = [
        0, 14, 16, 28, 37, 67, 80, 84, 
        107, 109, 115, 117,
        140, 144, 157, 187, 196, 208, 210, 224]

        self.triple_letter_tiles = [
        20, 24, 51, 53, 76, 88, 93, 101,
        123, 131, 136, 148, 171, 173, 200, 204]

        self.forbidden_letter_tiles = [52, 108, 116, 172]
        self.forbidden_word_tiles = [7, 105, 119, 217]

        #Imaginary rectangles references
        self.all_imaginary_indexes = []
        self.board_array = [[{} for col in range(16)] for row in range(16)]
        #This must be 16 instead of the expected 15, see the crossword function

        self.board_copy =[[x.copy() for x in row] for row in self.board_array]

        self.let.rack_x = 318
        self.let.rack_y = 630

        self.board.reset_scores()
        self.board.prep_news()
        self.board.prep_scores()
        self.let.reset_rack()
        self.menu.game_reset = False
        self.board_needs_a_copy = False

        #First move flag
        self.started = False

        #Allowed directions flags
        self.vertical_on = False
        self.horizontal_on = False
        self.moving_letters = False

        self.ai_turn = self.board.player_2 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    def continue_game(self):
        """Gaming function"""

        self.let.get_sack_size()
        self.let.load_rack()
        self.board.prep_sack(str(self.let.number_letters_left))
        self.let.update_let()
        self.reset_used_items()
        self.check_grids_letters_collision()
        self.rack_in_collisions()
        self.store_used_letters()

        self.alignment_test()
        self.empty_space_test()
        self.starting_move()
        self.valid_next_move()

        self.if_any_replacement()
        self.buttons.check_play_event()
        self.buttons.check_undo_event()
        self.perform_undo()
        self.buttons.check_replace_event()

        self.play_the_word()
        self.place_moved_letters()
        self.make_imaginary_rects()

        if self.let.number_letters_left <= 0:
            if len(self.let.rack_images) <= 0:
                self.transition_fade()
                self.menu.main_menu_on = True


    def _get_new_board_copy(self):
        """Copy the board"""
        #Set a way to only copy the board if something changed
        self.board_copy =[[x.copy() for x in row] for row in self.board_array]


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
        self.used_ids = []
        self.master_board_collisions = []

        self.replaced_letters = []
        self.replaced_rects = []
        self.replaced_images = []


    def check_grids_letters_collision(self):
        """Detect any collision between reference rectangles on grids and used letters rectangles."""

        if self.let.selected == False:

            for l in range(len(self.let.rack_rects)):
            #Define what happens when the letters generated from letters dictionary appear on the screen.
                for r in range(8):
                #We have 8 rack grid rectangles
                    collisions_2 = self.rack_rectangles[r].colliderect(self.let.rack_rects[l])
                    #Collision between letters and the rack grids

                    if collisions_2:
                        self.let.rack_rects[l].center = self.rack_rectangles[r].center

                #Set a lock for the next loops to only operate when any one letter is moved from the rack
                if self.let.rack_rects[l].center != self.rack_rectangles[l].center:
                    self.moving_letters = True


            if self.moving_letters:
                self._get_new_board_copy()
                #Define what happens when a letter from rack is dropped on the board grids
                for b in range(225):
                    #We have 225 board tiles, and this for loop needs to come first so that used letters
                    #will be appended in the order they appear on the board
                    for l in range(len(self.let.rack_rects)):
                        #Collision between letters and all the board grids

                        if self.board_rectangles[b].colliderect(self.let.rack_rects[l]):
                            self.let.rack_rects[l].center = self.board_rectangles[b].center
                            if (l, b) not in self.master_board_collisions:
                                self.master_board_collisions.append((l, b))

                            self.used_images.append(self.let.rack_images[l])
                            self.used_letters.append(self.let.rack_letter_names[l])
                            self.used_rects.append(self.let.rack_rects[l])
                        

                for l in range(len(self.let.rack_rects)):
                    #Define what happens when rack letters drop on letters that have been locked on the board
                    for let, index, rect in self.moved_dict.values():
                    #Goes through all the listed board letter rectangles
                        collisions_4 = rect.colliderect(self.let.rack_rects[l])

                        if collisions_4:
                            self._undo(l)

                    #Define what happens when the letters from the rack are droped on the replace rack
                    for rep in range(8):
                        collisions_3 = self.replacer_grid[rep].colliderect(self.let.rack_rects[l])

                        if collisions_3:
                            self.let.rack_rects[l].center = self.replacer_grid[rep].center

                            self.replaced_images.append(self.let.rack_images[l])
                            self.replaced_letters.append(self.let.rack_letter_names[l])
                            self.replaced_rects.append(self.let.rack_rects[l])

            if self.master_board_collisions:
                self._match_board_collisions()


    def _match_board_collisions(self):
        #Now get the coordinates of the grid where collision happen
        for l, b in self.master_board_collisions:
            for rect_number, index in self.number_to_index.items():
                if self.board_rectangles.index(self.board_rectangles[b]) == rect_number:
                    i = index[0]
                    j = index[1]

                    let_name = self.let.rack_letter_names[l]
                    let_id = str(rect_number) + '_'
                    self.used_indexes.append([i, j])
                    self.used_ids.append(let_id)
                    self.board_copy[i][j][let_name] = let_id
                    #So let_id can be used for double and triple letter


    def perform_undo(self):
        if self.buttons.undo_event:
            self._reset_tiles_positions()
            self.moving_letters = False


    def _reset_tiles_positions(self):
        """Reinitialize rack tiles positions."""

        for l in range(len(self.let.rack_rects)):
            self._undo(l)


    def _undo(self, l):
        self.let.rack_rects[l].x = self.ract_init_x[l]
        self.let.rack_rects[l].y = self.let.rack_y


    def store_used_letters(self):
        """Store image, location, letter name, and rectangle for each used letter"""
        self.saved_words_bonus = {}

        if self.used_images:
            self.used_dict = dict(zip
                                    (zip(self.used_images, self.used_ids), 
                                    zip(self.used_letters, self.used_indexes, self.used_rects)))
        if self.replaced_images:
            self.replaced_dict = dict(zip
                                        (self.replaced_images, 
                                        zip(self.replaced_letters, self.replaced_rects)))



    def alignment_test(self):
        """To make sure all letters are aligned with the first placed on board"""
        self.aligned = []
    
        #Once more than two letters are on the board, only one direction is allowed
        if len(self.used_rects) >= 2:
            if self.used_rects[1].x == self.used_rects[0].x:
                self.vertical_on = True
                self.horizontal_on = False
                for rect in self.used_rects[2:]:
                    if rect.x != self.used_rects[0].x:
                        self.aligned.append(False)

            if self.used_rects[1].y == self.used_rects[0].y:
                self.horizontal_on = True
                self.vertical_on = False
                for rect in self.used_rects[2:]:
                    if rect.y != self.used_rects[0].y:
                        self.aligned.append(False)


    def empty_space_test(self):
        """No empty space should be allowed between currently played letters"""

        self.empty_space_in = False
        truth_test = []

        if len(self.used_indexes) > 1:
            i_f, j_f = self.used_indexes[0]
            i_l, j_l = self.used_indexes[-1]

            if self.horizontal_on:
                i_distance = i_l - i_f + 1
                for i in range(1, i_distance):
                    if not self.board_copy[i_f + i][j_f]:
                        truth_test.append(False)

            elif self.vertical_on:
                j_distance = j_l - j_f + 1
                for j in range(1, j_distance):
                    if not self.board_copy[i_f][j_f+j]:
                        truth_test.append(False)

        if False in truth_test:
            self.empty_space_in = True


    def starting_move(self):
        """Make sure the game proceeds only if there is tile at the board's center grid"""

        if not self.moved_dict:
            if not self.board_copy[7][7]:
                self.started = False
            else:
                self.started = True


    def valid_next_move(self):
        """Any subsequent letters should touch existing letters."""
        self.validate_moves = []

        for index in self.used_indexes:
            if index in self.all_imaginary_indexes:
                self.validate_moves.append(True)
                #At least one index is already in imaginary indexes, indicating contact

        if True not in self.validate_moves:
            self.validate_moves.append(False)


    def if_any_replacement(self):
        """If some tiles are on the replace rack."""
        count_replaced = 0

        if not self.let.selected:
            if self.buttons.replace_event:
                if self.replaced_letters:

                    for image, letter_rect in self.replaced_dict.items():

                        del self.let.rack_letter_names[self.let.rack_rects.index(letter_rect[1])]
                        self.let.rack_rects.remove(letter_rect[1])
                        self.let.rack_images.remove(image)
                        self.let.letters[letter_rect[0]][1] += 1
                        count_replaced += 1
                    self.buttons.replace_event = False
                    self.board.prep_sack(str(self.let.number_letters_left))

                    #Reset rack letters positions
                    self._reset_rack_coordinates()
                    self.moving_letters = False

        if count_replaced > 0:
            if self.board.player_1 == True:
                self.board.player_1 = False
                self.board.player_2 = True
            elif self.board.player_2 == True:
                self.board.player_1 = True
                self.board.player_2 = False


    def _read_cross_words(self):
        """Read words vertically and horizontally"""

        read_vertical = {}
        read_horizontal = {}

        held_vertical = ""
        vertical_id = ""

        held_horizontal = ""
        horizontal_id = ""

        self.letter_bonus_used = []

        #Ranges need to be 16, not 15, so that the last row and the last column
        #Always end the previous word formed, preventing the code from joining different loops
        for column in range(16):
            #To scan from top to bottom, right to left
            for row in range(16):
                p = self.board_copy[column][row]
                if not p:
                    if held_vertical:
                        #Filter and append
                        if len(held_vertical) > 1:
                            read_vertical[held_vertical] = vertical_id.strip('_')
                        held_vertical = ""
                        vertical_id = ""
                else:
                    held_vertical += next(iter(p))
                    vertical_id += next(iter(p.values()))

        for row in range(16):
            #To scan from left to right, top to bottom
            for column in range(16):
                n = self.board_copy[column][row]
                if not n:
                    if held_horizontal:
                        #Filter and append
                        if len(held_horizontal) > 1:
                            read_horizontal[held_horizontal] = horizontal_id.strip('_')
                        held_horizontal = ""
                        horizontal_id = ""
                else:
                    held_horizontal += next(iter(n))
                    horizontal_id += next(iter(n.values()))

        if read_vertical:   #Only list new vertical words
            self.vertical_words_list = [
                (word, w_id) for word, w_id in read_vertical.items() if w_id not in self.words_ids]
            self._find_bonus_letters(self.vertical_words_list)

        if read_horizontal: #Only list new horizontal words
            self.horizontal_words_list = [
                (word, w_id) for word, w_id in read_horizontal.items() if w_id not in self.words_ids]
            self._find_bonus_letters(self.horizontal_words_list)


    def _find_bonus_letters(self, words_list):
        for word, w_id in words_list:
            letters = list(word)
            let_ids = w_id.split("_")
            for bonus_let, let_id in zip(letters, let_ids):
                self._get_bonus_points(word, w_id, bonus_let, int(let_id))


    def _get_bonus_points(self, word, w_id, bonus_let, rect_number):
        """Get bonus from letter bonus tiles"""
        self.saved_words_bonus.setdefault((word, w_id), 0)

        if rect_number in self.double_letter_tiles:
            self.saved_words_bonus[(word, w_id)] += self.let.letters[bonus_let][0]
            self.letter_bonus_used.append(rect_number)

        elif rect_number in self.triple_letter_tiles:
            self.saved_words_bonus[(word, w_id)] += self.let.letters[bonus_let][0]*2
            self.letter_bonus_used.append(rect_number)

        elif rect_number in self.forbidden_letter_tiles:
            self.saved_words_bonus[(word, w_id)] -= self.let.letters[bonus_let][0]*2
            self.letter_bonus_used.append(rect_number)


    def _reset_rack_coordinates(self):
        self.let.rack_x = 318
        for rect in self.let.rack_rects:
            rect.x = self.let.rack_x
            self.let.rack_x += 34


    def play_the_word(self):
        """Formed a worded using the letters placed on the board when play button is pressed
        And check whether the word is valid"""
        self.invalid_words = []
        self.valid_words = []
        self.word_bonus_used = []
        self.points = 0
        self.accepted = False

        if not self.let.selected:

            if self.buttons.play_event:
                if self.started:
                    if self.empty_space_in == False:

                        if False not in self.aligned:
                            self._read_cross_words()
                            self._engage_checking()
                        else:
                            self.board.news = "Wrong Alignment!"
                            self._announce_news()

                    else:
                        self.board.news = f"Multiple words!"
                        self._announce_news()

                else:
                    self.board.news = f"Missed the board center!"
                    self._announce_news()

                self.moving_letters = False
            self.buttons.play_event = False


    def _announce_news(self):
        """News after playing wrong"""
        self._reset_tiles_positions()
        sfx.placement_sound.play()
        self.board.prep_news()
        self.buttons.play_event = False


    def _engage_checking(self):
        """Start words checking procedures"""
        if not self.moved_dict:

            if self.horizontal_on:
                horizontal_word = next(iter(self.horizontal_words_list))
                self._word_checking(horizontal_word)
            else:
                vertical_word = next(iter(self.vertical_words_list))
                self._word_checking(vertical_word)

            self._accept_or_reject_words()
            self.buttons.play_event = False

        else:
            if True in self.validate_moves:
                if self.vertical_on:
                    self._check_all_words(self.vertical_words_list, self.horizontal_words_list)

                else:
                    self._check_all_words(self.horizontal_words_list, self.vertical_words_list)

                self._accept_or_reject_words()
                self.buttons.play_event = False

            else:
                self.board.news = f"Missed contact!"
                self._announce_news()


    def _check_all_words(self, first, second):
        """Pass lists of words to word checking"""
        for word_and_id in first:
            self._word_checking(word_and_id)
        for word_and_id in second:
            self._word_checking(word_and_id)


    def _word_checking(self, word_and_id):
        """Check a single word"""

        try:
            step_points = int(self.check.check_word(word_and_id[0]))
                    
        except Exception:
            if word_and_id:
                self.invalid_words.append(word_and_id[0])
            else:
                pass
        else:
            self.valid_words.append(word_and_id[0])

            self._multiply_words_points(word_and_id, step_points)


    def _multiply_words_points(self, word_and_id, step_points):
        """Multiple each word points by the number of times indicated by the spot"""

        _, w_id = word_and_id
        word_bonus = 0
        let_bonus = 0

        for number in w_id.split("_"):
            if int(number) in self.double_word_tiles:
                self.word_bonus_used.append(int(number))
                if self.saved_words_bonus[word_and_id]:
                    let_bonus += self.saved_words_bonus[word_and_id]

                word_bonus += (step_points+let_bonus)*2

            if int(number) in self.triple_word_tiles:
                self.word_bonus_used.append(int(number))

                if self.saved_words_bonus[word_and_id]:
                    let_bonus += self.saved_words_bonus[word_and_id]

                word_bonus += (step_points+let_bonus)*3

            if int(number) in self.forbidden_word_tiles:
                self.word_bonus_used.append(int(number))

                if self.saved_words_bonus[word_and_id]:
                    let_bonus += self.saved_words_bonus[word_and_id]

                word_bonus -= (step_points+let_bonus)*3

        #For words
        if word_bonus:
            self.points += word_bonus
        else:
            if self.saved_words_bonus[word_and_id]:
                    let_bonus += self.saved_words_bonus[word_and_id]
            self.points += (step_points+let_bonus)

        if not self.moved_dict:
            self.points *= 2 #First player gets 2 times word points


    def _accept_or_reject_words(self):

        if len(self.invalid_words) > 0:
            self._reset_tiles_positions()
            sfx.invalid_word_sound.play()
            self.board.news = f"{next(iter(self.invalid_words))} not valid."
            self.board.prep_news()
            self.accepted = False

        elif len(self.invalid_words) == 0:
            if self.valid_words:
                self.accepted = True
                sfx.valid_word_sound.play()

                self._award_points()
                self.board.prep_news()
                self.board.prep_scores()
                self._move_played_letters()

                if self.word_bonus_used:
                    for number in set(self.word_bonus_used):
                        if number in self.double_word_tiles:
                            self.double_word_tiles.remove(number)
                        elif number in self.triple_word_tiles:
                            self.triple_word_tiles.remove(number)
                        elif number in self.forbidden_word_tiles:
                            self.forbidden_word_tiles.remove(number)

                if self.letter_bonus_used:
                    for number in self.letter_bonus_used:
                        if number in self.double_letter_tiles:
                            self.double_letter_tiles.remove(number)
                        elif number in self.triple_letter_tiles:
                            self.triple_letter_tiles.remove(number)
                        elif number in self.forbidden_letter_tiles:
                            self.forbidden_letter_tiles.remove(number)

            else:
                self._reset_tiles_positions()
                sfx.invalid_word_sound.play()
                self.board.news = f"No valid words."
                self.board.prep_news()
                self.accepted = False


    def _award_points(self):
        """Add earned points to the player's scores"""
        #Add letters bonuses

        if self.board.player_1 == True:
            self.board.player_1_score += self.points
            self.board.player_1 = False
            self.board.player_2 = True

        elif self.board.player_2 == True:
            self.board.player_2_score += self.points
            self.board.player_1 = True
            self.board.player_2 = False

        if self.points > 0:
            self.board.news = f"{next(iter(self.valid_words))} : + {self.points}"
        else:
            self.board.news = f"{next(iter(self.valid_words))} : - {-1*self.points}"


    def _move_played_letters(self):
        #Delete letters, Images, and their rectangles from rack and move them to board
        for image_id, letter_index_rect in self.used_dict.items():
            self.moved_dict[image_id] = letter_index_rect

            del self.let.rack_letter_names[self.let.rack_rects.index(letter_index_rect[2])]
            self.let.rack_rects.remove(letter_index_rect[2])
            self.let.rack_images.remove(image_id[0])

        #Reset rack letters positions
        self._reset_rack_coordinates()


    def make_imaginary_rects(self):
        """"All rectangles on the board will have side rectangles where subsewuent letters should be placed."""
        #Imaginary rectangles that used letters must collide with for valid moves
        #These rectangles will be generated from rectangles already on the board

        temporary_imaginary_rectangles = []
        temporary_imaginary_indexes = []

        for i in range(15):
            for j in range(15):
                if self.board_array[i][j]:
                    if i == 0:
                        if not self.board_array[i+1][j]:
                            temporary_imaginary_rectangles.append(self.index_to_rectangle[(i+1, j)])
                            temporary_imaginary_indexes.append([i+1, j])
                    elif i == 14:
                        if not self.board_array[i-1][j]:
                            temporary_imaginary_rectangles.append(self.index_to_rectangle[(i-1, j)])
                            temporary_imaginary_indexes.append([i-1, j])
                    else:
                        if not self.board_array[i+1][j]:
                            temporary_imaginary_rectangles.append(self.index_to_rectangle[(i+1, j)])
                            temporary_imaginary_indexes.append([i+1, j])
                        if not self.board_array[i-1][j]:
                            temporary_imaginary_rectangles.append(self.index_to_rectangle[(i-1, j)])
                            temporary_imaginary_indexes.append([i-1, j])

                    if j == 0:
                        if not self.board_array[i][j+1]:
                            temporary_imaginary_rectangles.append(self.index_to_rectangle[(i, j+1)])
                            temporary_imaginary_indexes.append([i, j+1])
                    elif j == 14:
                        if not self.board_array[i][j-1]:
                            self.imaginary_rectangles.append(self.index_to_rectangle[(i, j-1)])
                            temporary_imaginary_indexes.append([i, j-1])
                    else:
                        if not self.board_array[i][j+1]:
                            temporary_imaginary_rectangles.append(self.index_to_rectangle[(i, j+1)])
                            temporary_imaginary_indexes.append([i, j+1])
                        if not self.board_array[i][j-1]:
                            temporary_imaginary_rectangles.append(self.index_to_rectangle[(i, j-1)])
                            temporary_imaginary_indexes.append([i, j-1])

        self.imaginary_rectangles = temporary_imaginary_rectangles
        self.all_imaginary_indexes = temporary_imaginary_indexes


    def place_moved_letters(self):
        """All grids with letter tile on top will have the value of that letter."""

        if self.accepted == True:
            for imgage_id, let_index_rect in self.used_dict.items():
                i = let_index_rect[1][0]
                j = let_index_rect[1][1]
                letter = let_index_rect[0]
                self.board_array[i][j][letter] = imgage_id[1]

            for words, id_a in self.horizontal_words_list:
                if id_a not in self.words_ids:
                    self.words_ids.append(id_a)

            for words, id_b in self.vertical_words_list:
                if id_b not in self.words_ids:
                    self.words_ids.append(id_b)


    def draw_played_letters(self):
        """Draw the locked letters on the board."""
        for image_id, let_index_rect in self.moved_dict.items():
            self.screen.blit(image_id[0], let_index_rect[2])


    def draw_imaginary_rects(self):

        for im_rect in self.imaginary_rectangles:
            self.screen.blit(self.imaginary_surface, im_rect)


    def ai_simulations(self):
        ...


    def ai_play(self):
        """Simulate the play for the second player played by the computer"""

        #ai_letters = {let : [(rect_number, rect_pos), (i, j)]}

        if self.ai_turn:
            pygame.time.delay(50)

            for let, coordinates in ai_letters.items():
                i = coordinates[1][0]
                j = coordinates[1][1]
                self.board_array[i][j] = let #add all dict as expected here
                self.let.rack_rects[coordinates[0][0]].center = coordinates[0][1]
                pygame.time.delay(20)
            self.play_event = True


    def transition_fade(self):
        """A fading in transition"""
        transition_screen = pygame.Surface((self.SCREENWIDTH, self.SCREENHEIGHT))
        transition_screen.fill(self.bg_color)

        for alpha in range(0, 255, 5):
            transition_screen.set_alpha(alpha)
            self.update_screen()
            self.screen.blit(transition_screen, (0, 0))
            self.clock.tick(500)
            pygame.display.update()


    def transition_fall(self):
        """A falling background transition"""
        transition_screen = pygame.Surface((self.SCREENWIDTH, self.SCREENHEIGHT))
        transition_screen.fill(self.bg_color)
        transition_screen_rect = transition_screen.get_rect()

        for position in range(-self.SCREENHEIGHT, 0, 10):
            transition_screen_rect.y = position
            self.update_screen()
            self.screen.blit(transition_screen, transition_screen_rect)
            self.clock.tick(500)
            pygame.display.update()


    def update_screen(self):
        """Update the images on the screen."""

        self.screen.fill(self.bg_color)

        if self.menu.main_menu_on:
            self.menu.draw_menu()

        else:
            if self.menu.game_paused == True:
                self.menu.draw_menu()

            else:
                self.board.draw_board()
                self.buttons.draw_buttons()
                if self.moved_dict:
                    self.draw_imaginary_rects()
                    self.draw_played_letters()
                self.let.blit_let()


if __name__ == "__main__":
    game = GoWs()
    game.start_game()
