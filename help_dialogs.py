import pygame
from images import Images
from maingame import maingame
import tsoliasgame
import fonts


def story(surface, position, title="Story", frame=0):
    description_string = \
        """Your main character is Purpley       , a PurpleFace.
He  used  to live  happily  in  PurpleTown                       (yes,  almost
everything is purple in PurpleTown), until something terrible happened!
He woke up from bed and mysteriously his blue color was gone!!!    \0
He was all red! As a result, PurpleMayor exiled him from PurpleTown.
Your goal is to help PurpleFace collect splatters of blue paint      ,
so that he can regain his purple color."""
    tsoliasgame.draw_text(surface, fonts.font_44, title, position,
                          tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
    tsoliasgame.draw_text(surface, fonts.font_26, description_string, (position[0], position[1] + 80),
                          tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)

    surface.blit(Images.purple_image, (position[0] + 64, position[1] + 80))
    surface.blit(Images.town_image, (position[0] + 60, position[1] + 114))
    surface.blit(Images.red_image, (position[0] + 298, position[1] + 180))
    surface.blit(Images.splatters_image, (position[0] + 272, position[1] + 246), pygame.Rect(0, 0, 32, 32))


def controls(surface, position, title="Controls", frame=0):
    description_string = \
        """To move Purpley around
To pause the game
To restart current level
To lock/unlock screen view
To move screen (while unlocked)"""
    tsoliasgame.draw_text(surface, fonts.font_44, title, position,
                          tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
    tsoliasgame.draw_text(surface, fonts.font_26, description_string, (position[0] - 140, position[1] + 80),
                          tsoliasgame.colors.white)

    surface.blit(Images.keyboard_left_image, (position[0] - 300, position[1] + 80))
    surface.blit(Images.keyboard_up_image, (position[0] - 260, position[1] + 80))
    surface.blit(Images.keyboard_right_image, (position[0] - 220, position[1] + 80))
    surface.blit(Images.keyboard_down_image, (position[0] - 180, position[1] + 80))

    surface.blit(Images.keyboard_esc_image, (position[0] - 180, position[1] + 114))

    surface.blit(Images.keyboard_r_image, (position[0] - 180, position[1] + 148))

    surface.blit(Images.keyboard_l_image, (position[0] - 180, position[1] + 182))

    surface.blit(Images.keyboard_w_image, (position[0] - 300, position[1] + 216))
    surface.blit(Images.keyboard_s_image, (position[0] - 260, position[1] + 216))
    surface.blit(Images.keyboard_a_image, (position[0] - 220, position[1] + 216))
    surface.blit(Images.keyboard_d_image, (position[0] - 180, position[1] + 216))


def more_info(surface, position, title="More Info", frame=0):
    description_string = \
        """Your main purpose is to guide Purpley       \0
through each level, while collecting all the
splatters of blue paint      . After that you
have to guide him safely to the exit       to
advance to the next level."""
    tsoliasgame.draw_text(surface, fonts.font_44, title, position,
                          tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
    tsoliasgame.draw_text(surface, fonts.font_26, description_string, (position[0], position[1] + 80),
                          tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)

    surface.blit(Images.purple_image, (position[0] + 164, position[1] + 80))
    surface.blit(Images.splatters_image, (position[0] + 18, position[1] + 148), pygame.Rect(0, 0, 32, 32))
    surface.blit(Images.exit_image, (position[0] + 138, position[1] + 182), pygame.Rect(32 + 32 * ((frame / maingame.fps) % 2), 0, 32, 32))


def itemsi(surface, position, title="Items", frame=0):
    description_string = \
        """Purpley: Your main character
Wall: Does what walls usually do...
Paint: You have to collect those
Exit: Get there to finish the level\n  (activates after you collect all paint splatters)
Movers: They accelerate you in one direction
Reversers: They reverse all movers
Ice: Causes you to slide
Rock: You can push them around"""
    tsoliasgame.draw_text(surface, fonts.font_44, title, position,
                          tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
    tsoliasgame.draw_text(surface, fonts.font_26, description_string, (position[0] - 140, position[1] + 80),
                          tsoliasgame.colors.white)

    surface.blit(Images.purple_image, (position[0] - 180, position[1] + 80), pygame.Rect(0, 0, 32, 32))

    surface.blit(Images.wall_image, (position[0] - 180, position[1] + 114), pygame.Rect(96, 96, 32, 32))

    surface.blit(Images.splatters_image, (position[0] - 180, position[1] + 148), pygame.Rect(0, 0, 32, 32))

    surface.blit(Images.exit_image, (position[0] - 180, position[1] + 182), pygame.Rect(32 + 32 * ((frame / maingame.fps) % 2), 0, 32, 32))

    surface.blit(Images.moverU_image, (position[0] - 300, position[1] + 250), pygame.Rect(0, 0, 32, 32))
    surface.blit(Images.moverD_image, (position[0] - 260, position[1] + 250), pygame.Rect(0, 0, 32, 32))
    surface.blit(Images.moverL_image, (position[0] - 220, position[1] + 250), pygame.Rect(0, 0, 32, 32))
    surface.blit(Images.moverR_image, (position[0] - 180, position[1] + 250), pygame.Rect(0, 0, 32, 32))

    surface.blit(Images.switch_en_image, (position[0] - 220, position[1] + 284))
    surface.blit(Images.switch_dis_image, (position[0] - 180, position[1] + 284))

    surface.blit(Images.ice_image, (position[0] - 180, position[1] + 318))

    surface.blit(Images.rock_image, (position[0] - 180, position[1] + 352))


def itemsii(surface, position, title="Items", frame=0):
    description_string = \
        """Black Hole: Sucks everything inside killing them
  (or transfering them inside a library...)
Wood: You can step on it once, but it will break
  when you leave revealing the tile below
Wooden Box: Can be destroyed when hit with the 
  extra speed from a mover
Teleporter: Teleports you to another teleporter
  of your choice and gets disabled afterwards"""
    tsoliasgame.draw_text(surface, fonts.font_44, title, position,
                          tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
    tsoliasgame.draw_text(surface, fonts.font_26, description_string, (position[0] - 140, position[1] + 80),
                          tsoliasgame.colors.white)

    surface.blit(Images.death_image, (position[0] - 180, position[1] + 80))

    surface.blit(Images.wood_image, (position[0] - 180, position[1] + 148))

    surface.blit(Images.wooden_box_image, (position[0] - 180, position[1] + 216))
    
    surface.blit(Images.teleporter_image, (position[0] - 220, position[1] + 284))
    surface.blit(Images.teleporter_dis_image, (position[0] - 180, position[1] + 284))

