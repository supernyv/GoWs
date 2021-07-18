import pygame

pygame.mixer.pre_init(20070, -16, 2, 1024)
pygame.mixer.init()

replace_sound = pygame.mixer.Sound('sounds/futuristic-slide.wav')
replace_sound.set_volume(0.1)
undo_sound = pygame.mixer.Sound('sounds/sci-fi-sweep.wav')
undo_sound.set_volume(0.5)

valid_word_sound = pygame.mixer.Sound('sounds/page-forward.wav')
valid_word_sound.set_volume(0.5)
invalid_word_sound = pygame.mixer.Sound('sounds/game-buzz.wav')
invalid_word_sound.set_volume(0.7)

placement_sound = pygame.mixer.Sound('sounds/click-error.wav')
placement_sound.set_volume(0.5)

wrong_start_sound = pygame.mixer.Sound('sounds/single-key-type.wav')

drop_letter_sound = pygame.mixer.Sound('sounds/hard-single-key-press.wav')