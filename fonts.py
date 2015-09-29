try:
    import pygame_sdl2 as pygame
    font_20 = pygame.font.Font("others/BuxtonSketch.ttf", 27)
    font_26 = pygame.font.Font("others/BuxtonSketch.ttf", 35)
    font_32 = pygame.font.Font("others/BuxtonSketch.ttf", 43)
    font_36 = pygame.font.Font("others/BuxtonSketch.ttf", 49)
    font_44 = pygame.font.Font("others/BuxtonSketch.ttf", 59)
except ImportError:
    import pygame
    font_20 = pygame.font.Font("others/BuxtonSketch.ttf", 20)
    font_26 = pygame.font.Font("others/BuxtonSketch.ttf", 26)
    font_32 = pygame.font.Font("others/BuxtonSketch.ttf", 32)
    font_36 = pygame.font.Font("others/BuxtonSketch.ttf", 36)
    font_44 = pygame.font.Font("others/BuxtonSketch.ttf", 44)