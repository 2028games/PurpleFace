import pygame
pygame.mixer.pre_init(buffer=512)
pygame.init()
import maingame


def main():

    game = maingame.MainGame(30, (0, 480))  # main game
    
    game.start(game.screen)  # start loop

if __name__ == "__main__":
    #cProfile.run("main()")
    main() #start!
