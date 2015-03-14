try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer
from settings import settings


class Audio:
    def __init__(self):
        self.sfx_suck = mixer.Sound("audio/suck.ogg")
        #self.sfx_click = mixer.Sound("audio/click.ogg")
        self.sfx_push = mixer.Sound("audio/rock_moved.ogg")
        self.sfx_pickup = mixer.Sound("audio/pickup.ogg")

    def set_volume(self):
        sfx = settings.get("sfx")
        self.sfx_suck.set_volume(sfx)
        self.sfx_push.set_volume(sfx)
        self.sfx_pickup.set_volume(sfx)