import pygame

WIDTH, HEIGHT = 620, 610
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (65, 224, 166)
GREY = (100,128,128)
TWHITE= (246,221,204)
TBLACK= (39,55,70)
TBLUE= (29,176,193)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (55, 45))
FB = pygame.transform.scale(pygame.image.load('assets/fb.png'), (65, 65))
FN = pygame.transform.scale(pygame.image.load('assets/fn.png'), (65, 65))