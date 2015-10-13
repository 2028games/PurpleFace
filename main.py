#! /usr/bin/env python
try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
    sdl2 = True
except ImportError:
    # No pygame_sdl2
    sdl2 = False
    
import pygame
if not sdl2:
    pygame.mixer.pre_init(buffer=512)
    
pygame.init()
import maingame


def main():
    if sdl2:
        game = maingame.MainGame(30, (800, 480), True)  # main game
    else:
        game = maingame.MainGame(30, (0, 480), False)  # main game
        
    
    game.start(game.screen)  # start loop

if __name__ == "__main__":
    # cProfile.run("main()")
    main()  # start!