import pygame
pygame.mixer.pre_init(20070, -16, 2, 1024) #(frequency in Hz, Bitdepth, Number of channels 1 for mono and 2 stereo, buffer size
pygame.mixer.init()

replace_sound = pygame.mixer.Sound('sounds/replace.wav')
replace_sound.set_volume(0.1)
undo_sound = pygame.mixer.Sound('sounds/undo.wav')
undo_sound.set_volume(0.5)

valid_word_sound = pygame.mixer.Sound('sounds/valid.wav')
valid_word_sound.set_volume(0.5)
invalid_word_sound = pygame.mixer.Sound('sounds/invalid.wav')
invalid_word_sound.set_volume(0.7)

placement_sound = pygame.mixer.Sound('sounds/wrong_placement.wav')
placement_sound.set_volume(0.5)

drop_letter_sound = pygame.mixer.Sound('sounds/drop.wav')
drop_letter_sound.set_volume(0.5)

new_game_sound = pygame.mixer.Sound('sounds/new_game.wav')
new_game_sound.set_volume(0.5)

golden_sound = pygame.mixer.Sound('sounds/golden_reveal.wav')
golden_sound.set_volume(0.5)
