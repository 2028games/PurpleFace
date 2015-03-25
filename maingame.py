import audio

try:
    import android
except ImportError:
    android = None

maingame = None

import tsoliasgame
import pygame
import fonts
from settings import settings
from multilevelgroup import MultiLevelGroup


class MainGame(tsoliasgame.Game):
    @property
    def fullscreen(self):
        return self.__fullscreen

    @fullscreen.setter
    def fullscreen(self, value):
        self.__fullscreen = value
        size = pygame.display.list_modes()[0]
        if value:
            height = 600
            width = int(height * size[0] / float(size[1]))
            size = (width, height)
            pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            height = 480
            width = int(height * size[0] / float(size[1]))
            size = (width, height)
            pygame.display.set_mode(size)
        info = pygame.display.Info()
        self.size = (info.current_w, info.current_h)
        print("new size: " + str(self.size))


    @property
    def controller(self):
        return self.__controller

    # noinspection PyAttributeOutsideInit
    @controller.setter
    def controller(self, value):
        self.previous_controller = self.__controller
        self.__controller = value

    def __init__(self, fps, size):
        global maingame
        maingame = self  # reference to be used by other objects

        # make main levelgroup
        levels = MultiLevelGroup(tsoliasgame.View((0, 0)))  # main level group
        levels.pick_directory("Levels")
        levels.directories.append(settings.get("downloaded_levels_dir"))
        levels.level_changed = self.level_changed

        self.__fullscreen = False
        tsoliasgame.Game.__init__(self, fps, levels, size)
        self.fullscreen = settings.get("fullscreen")
        tsoliasgame.load_module("objs")
        self.audio = audio.Audio()  # initialize audio
        
        if android:  # make some android specific actions
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
            android.map_key(android.KEYCODE_MENU, pygame.K_p)

        self.debug_mode = settings.get("debug_mode")  # shortcut for debug mode bool

        # and start the primary controller
        import controllers
        self.__controller = None
        self.controller = controllers.MainMenuController()
                
    def pre_update(self):
        pass
    
    def event_handling(self):
        if android and android.check_pause():
                android.wait_for_resume()
        
        self.controller.event_handling()
        
    def level_changed(self):
        self.controller.level_changed()

    def draw(self, surface):
        surface.fill(tsoliasgame.colors.darkkhaki)  # fill screen
        
        self.controller.draw(surface)
        
        # DRAW FPS
        if self.debug_mode:
            tsoliasgame.draw_text(surface, fonts.font_20, "fps: " + str(self.get_fps()),
                                  (self.size[0] - 80, self.size[1] - 26), tsoliasgame.colors.green)
        
        if surface == self.screen:
            pygame.display.flip()  # flip to screen