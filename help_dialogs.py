import pygame
from images import Images
import tsoliasgame
import fonts


def story(position, surface, title="Story"):
    story_string = \
        """Your main character is Purpley       , a PurpleFace.
He  used  to live  happily  in  PurpleTown                       (yes,  almost
everything is purple in PurpleTown), until one day the dreadful happened!
He woke up from bed and mysteriously his blue color was gone!!!    \0
He was all red! As a result, PurpleMayor exiled him from PurpleTown.
Your goal is to help PurpleFace collect splatters of blue paint      ,
so that he can regain his purple color."""
    tsoliasgame.draw_text(surface, fonts.font_44, title, position,
                          tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
    tsoliasgame.draw_text(surface, fonts.font_26, story_string, (position[0], position[1] + 50),
                          tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)

    surface.blit(Images.purple_image, (position[0] + 64, position[1] + 50))
    surface.blit(Images.town_image, (position[0] + 60, position[1] + 84))
    surface.blit(Images.red_image, (position[0] + 298, position[1] + 150))
    surface.blit(Images.splatters_image, (position[0] + 272, position[1] + 216), pygame.Rect(0, 0, 32, 32))