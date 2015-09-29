import pygame
from settings import settings


class Audio:
    def __init__(self):
        self.sfx_suck = pygame.mixer.Sound("audio/suck.ogg")
        self.sfx_click = pygame.mixer.Sound("audio/click.ogg")
        self.sfx_break = pygame.mixer.Sound("audio/breaking_wood.ogg")
        self.sfx_push = pygame.mixer.Sound("audio/rock_moved.ogg")
        self.sfx_pickup = pygame.mixer.Sound("audio/pickup.ogg")

    def set_volume(self):
        sfx = settings.get("sfx")
        self.sfx_suck.set_volume(sfx)
        self.sfx_click.set_volume(sfx)
        self.sfx_break.set_volume(sfx)
        self.sfx_push.set_volume(sfx)
        self.sfx_pickup.set_volume(sfx)