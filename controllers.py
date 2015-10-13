import os
import threading
import urllib
import urllib2
import achievements
import dialogs
import help_dialogs
import subprocess
import sys
from images import Images
from maingame import maingame
import tsoliasgame
import pygame
import objs
import fonts
from dialogs import Question
from dialogs import Message
from settings import settings


def bool_to_string(a, true_string="Yes", false_string="No"):
    """
    Converts a bool to string
    :rtype : bool
    :param a: the bool
    :param true_string: the string for true
    :param false_string: the string for false
    """
    if a:
        return true_string
    return false_string


class Controller(object):
    """controls maingame - 
    its a parent class that gets inherited to implement different ways to control maingame
    (level selection screen, main play e.t.c.)
    if used by maingame directly it just creates a screen that does nothing!"""
    
    def __init__(self):
        pass
    
    def event_handling(self):
        pass
    
    def draw(self, surface):
        pass
    
    def level_changed(self):
        pass


class IntroController(Controller):
    """controls intro screen"""
    def __init__(self):
        Controller.__init__(self)
        maingame.paused = True
        self.frames = 0
        self.back_color = tsoliasgame.colors.black

    def event_handling(self):
        """handles pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if x clicked
                maingame.exit()  # exit

    def draw(self, surface):
        surface.fill(self.back_color)

        # choose image to draw
        if self.frames <= 2 * maingame.fps:
            image = Images.c_logo_image
        elif self.frames <= 4 * maingame.fps:
            image = Images.g_logo_image
        else:
            maingame.controller = MainMenuController()  # continue
            return

        surface.blit(image, ((maingame.size[0] - image.get_width()) / 2, (maingame.size[1] - image.get_height()) / 2))  # draw image
        
        # draw version string
        if self.frames > 2 * maingame.fps:
            tsoliasgame.draw_text(surface, fonts.font_20, maingame.version_string, 
                                  ((maingame.size[0] + image.get_width()) / 2 - 100, (maingame.size[1] + image.get_height()) / 2),
                                  tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER, tsoliasgame.ALIGN_CENTER)
        self.frames += 1


class MainMenuController(Controller):
    """controls main menu screen"""
    def __init__(self):
        Controller.__init__(self)
        maingame.paused = True
        self.position = (100, 100)
        self.buttons = tsoliasgame.ButtonGroup()  # buttons group
        self.back_color = tsoliasgame.colors.dodgerblue

        if settings.first_time:
            self.blink = 0  # used to create an effect in the draw function
            self.mode = 1
        else:
            self.mode = 0

        # make the menu items list
        self.items = (
            MenuItem("Level Selection", self.action_level_selection),
            MenuItem("Help", self.action_help),
            MenuItem("Options", self.action_options),
            MenuItem("Achievements", self.action_achievements),
            MenuItem("Credits", self.action_credits),
            MenuItem("Update PurpleFace!", self.action_update),
            MenuItem("Download more levels", self.action_download),
            MenuItem("Exit", self.action_exit))

        # and create a button for each item in the list
        for i in range(len(self.items)):
            button = tsoliasgame.Button(self.items[i].action,
                                        rect=pygame.Rect(self.position[0], self.position[1] + 40 * i, 260, 40), sound=maingame.audio.sfx_click)
            self.buttons.add(button)

        self.small_logo = pygame.transform.scale(Images.g_logo_image, (360, 240))
        self.current_combo = []  # pressed keys - used for konami code
        pygame.mixer.music.stop()

    def event_handling(self):
        """handles pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if x clicked
                maingame.exit()  # exit

            elif event.type == pygame.KEYDOWN:  # keydowns
                if self.mode == 1:
                    self.mode = 2
                elif event.key == pygame.K_ESCAPE:
                   self.action_exit(None)  # exit
                elif event.key == pygame.K_F11:
                    maingame.fullscreen = not maingame.fullscreen
                elif self.test_konami(event.key):  # check for konami code
                    achievements.achievements["konami"].main_value = 1  # unlock achievement
                    maingame.debug_mode = not maingame.debug_mode  # toggle debug mode
                    if maingame.debug_mode:
                        settings.set("debug_mode", True)
                        Message("Debug Mode Enabled", "All levels are now playable and you\ncan use [Ctrl + Click] in game\nto move to cursor position.")
                    else:
                        settings.set("debug_mode", False)
                        Message("Debug Mode Disabled", "Debug mode is too cool for you?")

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.mode == 1:
                    self.mode = 2
                else:
                    self.buttons.handle_clicks(event.pos)

    def draw(self, surface):
        surface.fill(self.back_color)
        if self.mode == 1:
            help_dialogs.story(surface, (maingame.size[0] / 2, maingame.size[1] / 2 - 200), "Welcome to PurpleFace!")

            if self.blink >= 0:
                tsoliasgame.draw_text(surface, fonts.font_26, "Click anywhere to continue!",
                                      (maingame.size[0] / 2, maingame.size[1] / 2 + 110),
                                      tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
            elif self.blink < - 1 * maingame.get_fps():
                self.blink *= -1
            self.blink -= 1
        else:
            surface.blit(self.small_logo, (self.position[0] + 280, 150))
            for i in range(len(self.items)):
                tsoliasgame.draw_text(surface, fonts.font_36, self.items[i].item,
                                      (self.position[0], self.position[1] + 40 * i), tsoliasgame.colors.white)

            if self.mode == 2:
                # cover other choices
                cover_surface = pygame.Surface((self.position[0] - 4, maingame.size[1]))
                cover_surface.set_alpha(100)
                surface.blit(cover_surface, (0, 0))

                cover_surface = pygame.Surface((maingame.size[0], self.position[1]))
                cover_surface.set_alpha(100)
                surface.blit(cover_surface, (self.position[0] - 4, 0))

                cover_surface = pygame.Surface(maingame.size)
                cover_surface.set_alpha(100)
                surface.blit(cover_surface, (self.position[0] - 4, self.position[1] + 36))

                cover_surface = pygame.Surface((maingame.size[0], 36))
                cover_surface.set_alpha(100)
                surface.blit(cover_surface, (self.position[0] + 200, self.position[1]))

                tsoliasgame.draw_text(surface, fonts.font_26, "Click Level Selection to Start!",
                                      (self.position[0] + 400, self.position[1]),
                                      tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
                
            # DRAW ACHIEVEMENT
            achievements.Achievement.draw_achievement(surface)
                
    def test_konami(self, current_key):
        """tests if the konami code got pressed"""
        konami = (pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, 
                  pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a)
        
        if current_key == konami[len(self.current_combo)]:
            self.current_combo.append(current_key)
            if len(self.current_combo) == len(konami):
                self.current_combo = []
                return True
            return False
        
        self.current_combo = []
        return False

    @staticmethod
    def action_level_selection(pos):
        settings.first_time = False
        maingame.controller = LevelSelectionController()

    def action_help(self, pos):
        if self.mode == 0:
            maingame.controller = HelpController()

    def action_options(self, pos):
        if self.mode == 0:
            maingame.controller = OptionsController()

    def action_download(self, pos):
        if self.mode == 0:
            maingame.controller = LevelDownloadController()

    def action_achievements(self, pos):
        if self.mode == 0:
            maingame.controller = AchievementsController()

    def action_credits(self, pos):
        if self.mode == 0:
            maingame.controller = CreditsController()

    @staticmethod
    def action_update(pos):
        if Question("Update PurpleFace?", "PurpleFace will now exit to get updated.\nIs this OK?"):
            try:
                subprocess.Popen([sys.executable, "updater.py"], creation_flags=CREATE_NEW_CONSOLE)
            except:
                subprocess.Popen(["xterm", sys.executable, "updater.py"])
                  
            #maingame.exit()
        
    @staticmethod
    def action_exit(pos):
        maingame.exit()


class LevelDownloadController(Controller):
    def __init__(self):
        """controls level download screen"""
        Controller.__init__(self)
        maingame.paused = True
        self.online_dir = settings.get("level_download_dir")  # online directory with the files
        self.local_dir = settings.get("downloaded_levels_dir")  # local directory to store the files

        # if it doesnt exist lets make it now
        if not os.path.isdir(self.local_dir):
            try:
                os.mkdir(self.local_dir)
            except OSError:
                # might need elevated privileges
                Message("Os Error", "Elevated privileges might be needed for this action.")
                self.action_back(None)

        maingame.levels.pick_directory(self.local_dir)  # will work with the downloaded levels dir

        self.buttons = tsoliasgame.ButtonGroup()
        self.position = (100, 100)
        self.items = []  # levels that can be downloaded
        self.back_color = tsoliasgame.colors.dodgerblue
        self.download_list = []
        self.main_thread = None

        self.btn_list = tsoliasgame.Button(self.action_list, self.position, sound=maingame.audio.sfx_click)
        self.buttons.add(self.btn_list)
        self.action_refresh(None)

    def event_handling(self):
        """handles pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if x clicked
                maingame.exit()  # exit

            elif event.type == pygame.KEYDOWN:  # keydowns
                if event.key == pygame.K_ESCAPE:
                    self.action_back(None)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.buttons.handle_clicks(event.pos)

    def draw(self, surface):
        surface.fill(self.back_color)
        tsoliasgame.draw_text(surface, fonts.font_44, "Download more Levels!", (self.position[0] - 16, self.position[1] - 56), tsoliasgame.colors.white)
        tsoliasgame.draw_text(surface, fonts.font_20, "To download a new level, just click on it and it will be automatically downloaded!", 
                              (self.position[0] - 16, maingame.size[1] - 30), tsoliasgame.colors.white)
        
        if len(self.items) == 0:
            tsoliasgame.draw_text(surface, fonts.font_32, "Nothing new here :(", (self.position[0], self.position[1]), tsoliasgame.colors.white)
            return
            
        for i in range(len(self.items)):
            if self.items[i] in self.download_list:
                color = tsoliasgame.colors.darkgray
            else:
                color = tsoliasgame.colors.white
            tsoliasgame.draw_text(surface, fonts.font_32, self.items[i],
                                  (self.position[0] + (i / 5) * 200, self.position[1] + (i % 5) * 40), color)

    @staticmethod
    def action_back(pos):
        maingame.controller = MainMenuController()  # exit

    def action_refresh(self, pos):
        """gets the levels that are available for download"""
        try:
            response = urllib2.urlopen(self.online_dir + "list")
            
        except urllib2.URLError:
            Message("Connection Error", "A connection error occured:(\n Try again later.")
            return 1

        level_file = response.read()
        level_strings = level_file.split("\n")
        if not level_strings[0] == "#This is a valid list file":
            # response was not valid
            return 1

        self.items = []
        for i in range(1, len(level_strings)):
            level_string = level_strings[i]
            if not level_string in maingame.levels:
                (name, extension) = os.path.splitext(level_string)
                self.items.append(name)

        self.btn_list.rect = pygame.Rect(self.position[0], self.position[1],
                                         200 * ((len(self.items) - 1) / 5 + 1), 40 * min(5, len(self.items)))

    def action_list(self, pos):
        pick = 5 * ((pos[0] - self.position[0]) / 200) + (pos[1] - self.position[1]) / 40
        if pick < len(self.items) and not self.items[pick] in self.download_list:
            self.download_list.append(self.items[pick])
            if not self.main_thread or not self.main_thread.isAlive():
                self.main_thread = threading.Thread(target=self.download_files)
                self.main_thread.start()

    def download_files(self):
        while len(self.download_list) > 0:
            try:
                destination = "{}/{}.tmx".format(self.local_dir, self.download_list[0])
                urllib.urlretrieve(self.online_dir + self.download_list[0] + ".tmx", destination)
                self.download_list.pop(0)
                maingame.levels.add(destination)
                self.action_refresh(None)
            except IOError:
                Message("Connection Error", "A connection error occured:(\n Try again later.")
                return 1


class LevelSelectionController(Controller):
    @property
    def lower_boundary(self):
        return self.__lower_boundary

    @lower_boundary.setter
    def lower_boundary(self, value):
        self.__lower_boundary = max(min(value, len(maingame.levels) - 8), 0)

    def __init__(self):
        """controls level selection screen"""
        Controller.__init__(self)
        maingame.paused = True
        self.image_size = (maingame.size[0] - 200, maingame.size[1] - 140)
        self.back_color = tsoliasgame.colors.dodgerblue
        self.text_color = tsoliasgame.colors.white
        self.__lower_boundary = 0  # lower boundary stores the index of the first level to be written on the list

        self.buttons = tsoliasgame.ButtonGroup()

        self.btn_start = tsoliasgame.Button(self.action_start, Images.start_image,
                                            ((self.image_size[0] - 256) / 2, (self.image_size[1] - 128) / 2), sound=maingame.audio.sfx_click)

        btn_up = tsoliasgame.Button(self.action_up, Images.arrowu_image, (self.image_size[0] + 26, 4), sound=maingame.audio.sfx_click)

        btn_down = tsoliasgame.Button(self.action_down, Images.arrowd_image, (self.image_size[0] + 26, 350), sound=maingame.audio.sfx_click)

        btn_levels = tsoliasgame.Button(self.action_levels, None,
                                        rect=pygame.Rect(self.image_size[0] + 20, 54, 80, 36 * 8), sound=maingame.audio.sfx_click)

        btn_switch = tsoliasgame.Button(self.action_switch, Images.switch_image,
                                        (maingame.size[0] - 48, 8), sound=maingame.audio.sfx_click)

        self.buttons.add(self.btn_start, btn_up, btn_down, btn_levels, btn_switch)
        self.cur_level_index = 0

        self.img_lock = Images.lock_image
        self.img_tick = Images.tick_image

        self.unlocked = settings.get("unlocked")  # shortcut for faster accesss

        self.blink = 0

        levels = maingame.levels
        levels.pick_directory("Levels")  # auto change to default directory if current is empty
        if levels.current_index() == -1:
            levels.start_level(0)
        else:
            levels.restart_current()

        objs.Purple.colorize_images(min(1.0, float(self.unlocked - 1) / len(maingame.levels)))

        pygame.mixer.music.stop()
        self.level_changed()
    
    def event_handling(self):
        """handles pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if x clicked
                maingame.exit()  # exit
                
            elif event.type == pygame.KEYDOWN:  # keydowns
                if event.key == pygame.K_ESCAPE:
                    maingame.controller = MainMenuController()
                if event.key == pygame.K_RETURN:
                    self.action_start(None)  # start level
                elif event.key == pygame.K_UP:
                    self.action_up(None)  # move levels up
                elif event.key == pygame.K_DOWN:
                    self.action_down(None)  # and down
                elif event.key == pygame.K_s:
                    self.action_switch(None)
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                self.buttons.handle_clicks(event.pos)

    def draw(self, surface):
        surface.fill(self.back_color)
        
        cur_level = maingame.levels.current()  # current level

        self.generate_level_image(cur_level)
        surface.blit(cur_level.image, ((self.image_size[0] - cur_level.image.get_width()) / 2, (self.image_size[1] - cur_level.image.get_height()) / 2))
        
        pygame.draw.line(surface, tsoliasgame.colors.black, (0, self.image_size[1]), (self.image_size[0] + 4, self.image_size[1]), 8)
        pygame.draw.line(surface, tsoliasgame.colors.black, (self.image_size[0], 0), (self.image_size[0], self.image_size[1] + 4), 8)
        
        tsoliasgame.draw_text(surface, fonts.font_44, cur_level.title, [self.image_size[0] / 2, self.image_size[1] + 4],
                              self.text_color, tsoliasgame.ALIGN_CENTER, tsoliasgame.ALIGN_TOP)
        tsoliasgame.draw_text(surface, fonts.font_32, cur_level.description, [self.image_size[0] / 2, self.image_size[1] + 44],
                              self.text_color, tsoliasgame.ALIGN_CENTER, tsoliasgame.ALIGN_TOP)
        
        for i in range(self.lower_boundary, min(len(maingame.levels), self.lower_boundary + 8)):
            i_level = maingame.levels[i]  # level i represents

            if i_level == cur_level:  # focused item
                self.cur_level_index = i
                font = fonts.font_44
                color = tsoliasgame.colors.black
                extra_x = 28  # focused item lock or tick will be drawn further away
            else:
                font = fonts.font_32
                color = self.text_color
                extra_x = 0

            text_x = self.image_size[0] + 20
            text_y = 68 + (i - self.lower_boundary) * 36
            
            tsoliasgame.draw_text(surface, font, i_level.title, (text_x, text_y),
                                  color, tsoliasgame.ALIGN_LEFT, tsoliasgame.ALIGN_CENTER)

            # next code draws a lock next to locked levels or a tick next to won levels
            image = None
            if i >= self.unlocked and maingame.levels.current_directory_index() == 0:  # if level locked and we are at the default level group
                image = self.img_lock
            else:
                if not hasattr(i_level, "won"):  # if we dont already know if the current level was won
                    self.check_level_won(i_level)  # check it now
                if i_level.won:
                    image = self.img_tick

            if image:
                surface.blit(image, (text_x + 98 + extra_x, text_y - 20))

        # blink start button
        if self.cur_level_index >= self.unlocked and maingame.levels.current_directory_index() == 0:
            self.btn_start.visible = False
        else:
            if self.blink == 0:
                self.btn_start.visible = False
            elif self.blink < - 1 * maingame.get_fps():
                self.blink *= -1
                self.btn_start.visible = True
            self.blink -= 1

        self.buttons.draw(surface)

    def level_changed(self):
        self.lower_boundary = maingame.levels.current_index() - 4

    def generate_level_image(self, level):
        """creates a map of the level specified"""
        if not hasattr(level, "image"):
            for obj in level.group:
                if not isinstance(obj, objs.Tutorial):
                    obj.visible = True
            # noinspection PyArgumentList
            image = pygame.Surface(level.size)  # create a new image
            image.fill(tsoliasgame.colors.darkkhaki)  # fill it with default background
            level.view.position = (0, 0)
            level.draw(image)  # draw everything

            # scale to the desired size keeping aspect ratio
            w_ratio = float(self.image_size[0] - 16) / level.size[0]
            h_ratio = float(self.image_size[1] - 16) / level.size[1]
            ratio = min(w_ratio, h_ratio)

            level.image = pygame.transform.scale(image, (int(ratio * level.size[0]), int(ratio * level.size[1])))

        return level.image

    @staticmethod
    def check_level_won(level):
        """uses the settings to check if the specified level was won
         and then adds an attribute to it so that we can easily find it later without calling the same function again
        :param level: the level to check
        :rtype : bool
         """
        won_list = settings.get("levels_won")
        level.won = level.source_tmx in won_list
        return level.won

    def action_start(self, pos):
        if self.cur_level_index < self.unlocked or maingame.levels.current_directory_index() != 0 or maingame.debug_mode:
            maingame.controller = GameplayController()

    @staticmethod
    def action_down(pos):
        if maingame.levels.jump_next():
            maingame.levels.start_level(0)

    @staticmethod
    def action_up(pos):
        if maingame.levels.jump_previous():
            maingame.levels.start_level(len(maingame.levels) - 1)

    def action_levels(self, pos):
        clicked_index = (pos[1] - 54) / 36 + self.lower_boundary
        if clicked_index == maingame.levels.current_index():
            self.action_start(None)
        else:
            maingame.levels.start_level(clicked_index)

    @staticmethod
    def action_switch(pos):
        if maingame.levels.next_directory(True):
            maingame.levels.start_level(0)


class OptionsController(Controller):
    def __init__(self):
        """controls settings screen"""
        Controller.__init__(self)
        maingame.paused = True
        self.buttons = tsoliasgame.ButtonGroup()
        self.position = (100, 60)  # position of the menu
        self.back_color = tsoliasgame.colors.dodgerblue
        # next line enables a preview-only keypad so that the user can immediately see the results of options changing!!
        self.keypad = VirtualKeypad(settings.get("show_keypad"), True, True)

        # make the menu items list
        self.items = (
            MenuItem(None, self.action_show_keypad),
            MenuItem(None, self.action_keypad_scale),
            MenuItem(None, self.action_blue_speed),
            MenuItem(None, self.action_fullscreen),
            MenuItem(None, self.action_quality),
            MenuItem(None, self.action_sfx),
            MenuItem(None, self.action_music),
            MenuItem("Defaults", self.action_defaults),
            MenuItem("Clear All Progress", self.action_clear_all_progress),
            MenuItem("Back", self.action_back))
        self.fill_strings()

        # and create a button for each item in the list
        for i in range(len(self.items)):
            button = tsoliasgame.Button(self.items[i].action,
                                        rect=pygame.Rect(self.position[0], self.position[1] + 40 * i, 400, 40), sound=maingame.audio.sfx_click)
            self.buttons.add(button)

    def event_handling(self):
        """handles pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if x clicked
                maingame.exit()  # exit

            elif event.type == pygame.KEYDOWN:  # keydowns
                if event.key == pygame.K_ESCAPE:
                    self.action_back(None)  # back to main menu

            elif event.type == pygame.MOUSEBUTTONUP:
                self.buttons.handle_clicks(event.pos)

    def draw(self, surface):
        surface.fill(self.back_color)
        tsoliasgame.draw_text(surface, fonts.font_44, "Options", (self.position[0] - 16, self.position[1] - 56), tsoliasgame.colors.white)

        for i in range(len(self.items)):
            if i == 1 and not settings.get("show_keypad"):
                color = tsoliasgame.colors.darkgray
            else:
                color = tsoliasgame.colors.white

            tsoliasgame.draw_text(surface, fonts.font_36, self.items[i].item,
                                  (self.position[0], self.position[1] + 40 * i), color)

            self.keypad.draw(surface)

    def fill_strings(self):
        self.items[0].item = "Show Keypad ({0})".format(bool_to_string(settings.get("show_keypad")))
        self.items[1].item = "Keypad Scale (Current: {0})".format(settings.get("keypad_scale"))
        self.items[2].item = "Character Speed (Current: {0})".format(settings.get("blue_speed"))
        self.items[3].item = "Fullscreen (Beta) (Current: {0})".format(bool_to_string(settings.get("fullscreen"),
                                                                                     "On", "Off"))
        self.items[4].item = "Graphics Quality (Current: {0})".format(bool_to_string(settings.get("quality"),
                                                                                     "Normal", "Low"))
        self.items[5].item = "Sound Effects ({0} %)".format(int(settings.get("sfx") * 100))
        self.items[6].item = "Music ({0} %)".format(int(settings.get("music") * 100))

    def action_show_keypad(self, pos):
        settings.set("show_keypad", not settings.get("show_keypad"))
        self.keypad.visible = settings.get("show_keypad")
        self.fill_strings()

    def action_keypad_scale(self, pos):
        if not settings.get("show_keypad"):
            return
        # has a list of valid items and goes to next item when clicked
        choices = (1, 1.5, 2, 2.5, 3)
        try:
            value = choices[(choices.index(settings.get("keypad_scale")) + 1) % len(choices)]
        except ValueError:  # occurs if current setting is not in the list of choices
            value = choices[0]
        settings.set("keypad_scale", value)
        self.keypad.keypad_scale = settings.get("keypad_scale")
        self.fill_strings()

    def action_blue_speed(self, pos):
        # has a list of valid items and goes to next item when clicked
        choices = (2, 4, 8)
        try:
            value = choices[(choices.index(settings.get("blue_speed")) + 1) % len(choices)]
        except ValueError:  # occurs if current setting is not in the list of choices
            value = choices[0]
        settings.set("blue_speed", value)
        objs.Purple.spd = settings.get("blue_speed")
        self.fill_strings()

    def action_fullscreen(self, pos, question=True):
        settings.set("fullscreen", not settings.get("fullscreen"))
        maingame.fullscreen = settings.get("fullscreen")
        self.fill_strings()
        maingame.draw(maingame.screen)
        if question and not Question("Fullscreen Changed", 
                                     "Graphics settings succesfully changed.\nAre the new settings okay?\n(Setting will be reset in %left seconds.)", 15 * maingame.fps).return_value:
            self.action_fullscreen(pos, False)

    def action_quality(self, pos):
        settings.set("quality", not settings.get("quality"))
        self.fill_strings()

    def action_sfx(self, pos):
        choices = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
        try:
            value = choices[(choices.index(settings.get("sfx")) + 1) % len(choices)]
        except ValueError:  # occurs if current setting is not in the list of choices
            value = choices[0]
        settings.set("sfx", value)
        maingame.audio.set_volume()
        self.fill_strings()

    def action_music(self, pos):
        choices = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
        try:
            value = choices[(choices.index(settings.get("music")) + 1) % len(choices)]
        except ValueError:  # occurs if current setting is not in the list of choices
            value = choices[0]
        settings.set("music", value)
        pygame.mixer.music.set_volume(value)
        self.fill_strings()

    def action_defaults(self, pos):
        settings.defaults()
        self.fill_strings()

    def action_clear_all_progress(self, pos):
        if Question("Clear All Progress?",
                    "Are you sure you want to clear progress? \n This action cant be reversed.").return_value:
            settings.defaults(True)  # reset settings
            self.fill_strings()
            for level in maingame.levels:
                level.won = False  # reset levels
                
            for key, achievement in achievements.achievements.iteritems():
                achievement.main_value = settings.get(key)  # reset achievements
                
            Message("Reset completed", "Reset Done. \n Restart PurpleFace now pls.")

    @staticmethod
    def action_back(pos):
        settings.save()
        maingame.controller = maingame.previous_controller.__class__()
        
        
class EndGameController(Controller):
    def __init__(self):
        """controls endgame screen"""
        Controller.__init__(self)
        maingame.paused = True
        self.position = (maingame.size[0] / 2, 20)  # position of the menu
        self.back_color = tsoliasgame.colors.dodgerblue
        self.frame = 0  # to control blinking effect

    def event_handling(self):
        """handles pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if x clicked
                maingame.exit()  # exit

            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:  # any key pressed
                maingame.controller = CreditsController()  # show credits

    def draw(self, surface):
        surface.fill(self.back_color)
        tsoliasgame.draw_text(surface, fonts.font_44, "Main story Completed!", 
                              (self.position[0], self.position[1]), tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
        tsoliasgame.draw_text(surface, fonts.font_32, 
                              """Congratulations! You completed the main levels!
Purpley is purple again and can now return to his hometown.
If he wants to return to the racists who kicked him out just
because he had different color than them. Perhaps he will
continue his adventures in the rest of the world after all.

Thank you for playing this amazing game. If you want to
play more PurpleFace you can download new levels in the
"Download More Levels" screen of the main menu.""", (self.position[0], self.position[1] + 44), tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
        
        if (self.frame / maingame.fps) % 2 == 0:
            tsoliasgame.draw_text(surface, fonts.font_26, "Press any key to continue!", 
                                  (maingame.size[0] - 10, maingame.size[1] - 36), tsoliasgame.colors.white, tsoliasgame.ALIGN_RIGHT)
            
        self.frame += 1


class HelpController(Controller):
    """controls help screen"""
    def __init__(self):
        Controller.__init__(self)
        maingame.paused = True
        self.menu_position = (10, 100)
        self.dialog_position = (460, 20)
        self.buttons = tsoliasgame.ButtonGroup()  # buttons group
        self.back_color = tsoliasgame.colors.dodgerblue
        self.focus = 0  # focused item
        self.frame = 0

        # make the menu items list
        # its a list of 2 strings (1st is menu item, 2nd is name of function to call)
        self.items = (
            ("Story", "story"),
            ("Controls", "controls"),
            ("More Info", "more_info"),
            ("Items I", "itemsi"),
            ("Items II", "itemsii"))

        # and create a big button
        button = tsoliasgame.Button(self.action_menu, rect=pygame.Rect(
            self.menu_position[0], self.menu_position[1], 150, 40 * len(self.items) - 1), sound=maingame.audio.sfx_click)
        self.buttons.add(button)
        
        # and another button for the movie reference achievement
        button = tsoliasgame.Button(self.action_reference, rect=pygame.Rect(
            self.dialog_position[0] - 140, self.dialog_position[1] + 114, 400, 40), debug=False)
        self.buttons.add(button)

        pygame.mixer.music.stop()

    def event_handling(self):
        """handles pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if x clicked
                maingame.exit()  # exit

            elif event.type == pygame.KEYDOWN:  # keydowns
                if event.key == pygame.K_UP:
                    self.focus = (self.focus - 1) % len(self.items)
                elif event.key == pygame.K_DOWN:
                    self.focus = (self.focus + 1) % len(self.items)
                if event.key == pygame.K_ESCAPE:
                    self.action_back(None)  # go back

            elif event.type == pygame.MOUSEBUTTONUP:
                self.buttons.handle_clicks(event.pos)

    def draw(self, surface):
        surface.fill(self.back_color)
        self.frame += 1
        
        self.buttons.draw(surface)

        # draw the side menu
        for i in range(len(self.items)):
            color = tsoliasgame.colors.gray
            if i == self.focus:
                color = tsoliasgame.colors.white

            tsoliasgame.draw_text(surface, fonts.font_26, self.items[i][0],
                                  (self.menu_position[0], self.menu_position[1] + 40 * i), color)

        pygame.draw.line(surface, tsoliasgame.colors.white, (self.menu_position[0] + 110, 0), (self.menu_position[0] + 110, maingame.size[1]), 4)

        getattr(help_dialogs, self.items[self.focus][1])(surface, self.dialog_position, frame=self.frame)
        
        # DRAW ACHIEVEMENT
        achievements.Achievement.draw_achievement(surface)

    def action_menu(self, pos):
        self.focus = (pos[1] - self.menu_position[1]) / 40
        
    def action_reference(self, pos):
        if self.focus == 4:
            achievements.achievements["reference"].main_value = 1

    @staticmethod
    def action_back(pos):
        maingame.controller = maingame.previous_controller.__class__()


class GameplayController(Controller):
    """controls main gameplay and level system"""
    @property
    def camera_locked(self):
        return bool(maingame.levels.view.following)

    @camera_locked.setter
    def camera_locked(self, value):
        if not self.camera_locked and value:
            maingame.levels.view.following = self.__previous_following

        else:
            self.__previous_following = maingame.levels.view.following
            maingame.levels.view.following = None
        
    def __init__(self):
        Controller.__init__(self)
        maingame.paused = False
        self.background = None  # a surface where the background gets saved for faster drawing

        self.buttons = tsoliasgame.ButtonGroup()  # the main button group

        self.hud = Hud((maingame.size[0] - 161, 1), self)  # hud object
        self.pause_menu = PauseMenu((maingame.size[0] / 2 - 144, maingame.size[1] / 2 - 144))  # pause menu object
            
        if settings.get("show_keypad"):  # we must show the virtual keypad
            self.keypad = VirtualKeypad()
        else:
            self.keypad = None

        # button for moving view
        btn_view = tsoliasgame.Button(self.action_camera,
                                      rect=pygame.Rect(maingame.size[0] / 4, maingame.size[1] / 8,
                                                       3 * maingame.size[0] / 4, 7 * maingame.size[1] / 8))

        self.buttons.add(btn_view)
        self.view_changing = False
        self.steps = 0  # counts total steps passed

        # load music
        pygame.mixer.music.unpause()
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("audio/pleasantcreek.ogg")
            pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(settings.get("music"))
            
        self.level_changed()
        
    def level_changed(self):
        objs.Purple.aheradrim = False
        # generate background
        classes = [objs.Wall, objs.Ice, objs.Death]
        if not settings.get("quality"):
            classes.append(objs.Mover)
        self.background = self.generate_background(tsoliasgame.colors.darkkhaki, classes)

        # give Purple the correct colors
        objs.Purple.colorize_images(min(1.0, float(settings.get("unlocked") - 1) / len(maingame.levels)))

    @staticmethod
    def generate_background(color, classes):
        # noinspection PyArgumentList
        img = pygame.Surface(maingame.levels.current().size)
        img.fill(color)
        for cls in classes:
            for obj in cls.all:

                obj.visible = True
                obj.draw(img)
                obj.visible = False
        return img

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                maingame.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    maingame.paused = not maingame.paused
                elif maingame.paused:
                    self.pause_menu.key_down(event)
                elif event.key == pygame.K_r:
                    self.restart_level()
                elif event.key == pygame.K_l:
                    self.camera_locked = not self.camera_locked
                # jump level keys - ONLY IN DEBUG MODE
                elif maingame.debug_mode:
                    if event.key == pygame.K_PAGEDOWN:
                        maingame.levels.jump_previous()
                    elif event.key == pygame.K_PAGEUP:
                        maingame.levels.jump_next()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if maingame.paused:
                    self.pause_menu.mouse_down(event)  # pause menu handles the event
                elif not (self.keypad and self.keypad.mouse_down(event)):
                    self.buttons.handle_clicks(event.pos)  # buttons handle the event

                    # move purple with ctrl + click - ONLY IN DEBUG MODE
                    if maingame.debug_mode:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LCTRL]:
                            for purple in objs.Purple.all:
                                purple.set_center(tsoliasgame.vector2.add(event.pos, maingame.levels.view.position))
                                purple.snap_grid((32, 32))
                                print(purple.position)

            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] == 1:
                    if maingame.paused:
                        self.pause_menu.mouse_motion(event) 
                    elif self.view_changing:
                        maingame.levels.view.position = tsoliasgame.vector2.substract(maingame.levels.view.position,
                                                                                      event.rel)
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if maingame.paused:
                    self.pause_menu.mouse_up(event)
                elif not (self.keypad and self.keypad.mouse_up(event)):
                    objs.TeleporterActive.mouse_up(event)
                    self.view_changing = False

        if not maingame.paused and not self.camera_locked:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                pos = maingame.levels.view.position
                maingame.levels.view.position = (pos[0], pos[1] - 8)
            elif keys[pygame.K_s]:
                pos = maingame.levels.view.position
                maingame.levels.view.position = (pos[0], pos[1] + 8)
            elif keys[pygame.K_a]:
                pos = maingame.levels.view.position
                maingame.levels.view.position = (pos[0] - 8, pos[1])
            elif keys[pygame.K_d]:
                pos = maingame.levels.view.position
                maingame.levels.view.position = (pos[0] + 8, pos[1])

        if not (self.keypad and self.keypad.used):  # if no virtual key was pressed
            objs.Purple.handle_keyboard()  # handle the keyboard to move Purple

        self.steps += 1
        if self.steps >= maingame.fps:
            self.steps = 0
            achievements.achievements["total_time"].main_value += 1

    def draw(self, surface):
        # do some level-related shit
        if objs.Switch.pressed:
            objs.Switch.pressed = False
            objs.Mover.changed = True
        else:
            objs.Mover.changed = False
        
        # draw background tiles
        surface.blit(self.background, tsoliasgame.vector2.multiply(-1, maingame.levels.view.position))
        
        maingame.levels.current().draw(surface)  # draw all items
        
        # DRAW VIRTUAL KEYPAD
        if not maingame.paused and self.keypad:
            self.keypad.draw(surface)
            
        # DRAW HUD
        self.hud.draw(surface)
        
        # DRAW PAUSE MENU IF NEEDED
        if maingame.paused:
            self.pause_menu.draw(surface)

        # DRAW ACHIEVEMENT
        achievements.Achievement.draw_achievement(surface)

    @staticmethod
    def restart_level():
        achievement = achievements.achievements["times_restarted"]
        achievement.main_value += 1
        objs.Tutorial.current = 0  # reset tutorial messages
        maingame.levels.restart_current()

    def action_camera(self, pos):
        self.view_changing = True


class AchievementsController(Controller):
    """controls achievement screen"""
    def __init__(self):
        Controller.__init__(self)
        maingame.paused = True
        self.position = (maingame.size[0] / 2 - 100, 100)
        self.sidebar_position = (maingame.size[0] - 120, 100)
        self.buttons = tsoliasgame.ButtonGroup()  # buttons group
        self.back_color = tsoliasgame.colors.dodgerblue
        self.focus = None
        self.focus_i = 0
        self.achievements = achievements.achievements
        self.line_width = 6
        self.size = (60, 100)

        # and create a big button
        button = tsoliasgame.Button(self.action_menu, rect=pygame.Rect(
            self.position[0] - self.line_width / 2 * self.size[0], self.position[1], self.size[0] * self.line_width, 400))
        self.buttons.add(button)

        pygame.mixer.music.stop()

    def event_handling(self):
        """handles pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if x clicked
                maingame.exit()  # exit

            elif event.type == pygame.KEYDOWN:  # keydowns
                if event.key == pygame.K_ESCAPE:
                    self.action_back(None)  # go back

            elif event.type == pygame.MOUSEBUTTONUP:
                self.buttons.handle_clicks(event.pos)

    def draw(self, surface):
        surface.fill(self.back_color)

        tsoliasgame.draw_text(surface, fonts.font_44, "Achievements",
                              (self.position[0], self.position[1] - 60), tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)

        # draw the medals
        i = 0
        for key, achievement in self.achievements.iteritems():
            j = 0
            for level in achievement.levels:
                image = level.image
                if j >= achievement.current_level:
                    image = Images.medal_hidden_image

                new_image = image
                if i == self.focus_i:
                    self.focus = level
                    new_image = pygame.transform.scale(image, (48, 96))

                    # draw the current medal info
                    surface.blit(new_image,
                                 (self.sidebar_position[0] - 24, self.sidebar_position[1]))
                    tsoliasgame.draw_text(surface, fonts.font_26, self.focus.title,
                                          (self.sidebar_position[0], self.sidebar_position[1] + 100), tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
                    tsoliasgame.draw_text(surface, fonts.font_20, self.focus.description,
                                          (self.sidebar_position[0], self.sidebar_position[1] + 130), tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)

                    status_string = "Completed!"
                    color = tsoliasgame.colors.green
                    if j >= achievement.current_level:
                        color = tsoliasgame.colors.red
                        status_string = "Progress: {0}/{1}".format(achievement.main_value, level.check_value)
                    tsoliasgame.draw_text(surface, fonts.font_20, status_string,
                                          (self.sidebar_position[0], self.sidebar_position[1] + 156), color, tsoliasgame.ALIGN_CENTER)

                surface.blit(new_image,
                             (self.position[0] + self.size[0] * (i % self.line_width - self.line_width / 2),
                              self.position[1] + self.size[1] * (i / self.line_width)))
                i += 1
                j += 1

        pygame.draw.line(surface, tsoliasgame.colors.white,
                         (self.sidebar_position[0] - 120, 0), (self.sidebar_position[0] - 120, maingame.size[1]), 4)

    def action_menu(self, pos):
        self.focus_i = (pos[0] - self.position[0]) / self.size[0] + self.line_width / 2 + \
                       self.line_width * ((pos[1] - self.position[1]) / self.size[1])

    @staticmethod
    def action_back(pos):
        maingame.controller = maingame.previous_controller.__class__()


class CreditsController(Controller):
    """controls credits screen"""
    def __init__(self):
        Controller.__init__(self)
        maingame.paused = True
        self.y = 100
        self.back_color = tsoliasgame.colors.dodgerblue

        self.surface = None
        self.surface_height = self.generate_surface()

        # start music
        pygame.mixer.music.load("audio/pleasantcreek.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(settings.get("music"))

    def event_handling(self):
        """handles pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if x clicked
                maingame.exit()  # exit

            elif event.type == pygame.KEYDOWN:  # keydowns
                self.action_back()  # go back

            elif event.type == pygame.MOUSEBUTTONUP:
                self.action_back()

    def draw(self, surface):
        surface.fill(self.back_color)
        if self.surface:
            surface.blit(self.surface, (0, self.y))
        else:
            Message("Error", "An Error occured! Credits could not be displayed.")
        self.y -= 1
        if -1 * self.y > self.surface_height:
            self.action_back()

    def generate_surface(self):
        """Generates a surface that contains the credits text from credits.txt
        Saves the surface to self.surface
        and returns the height of the surface"""
        
        if not os.path.exists("credits.txt"):
            return 0

        surface = pygame.Surface((maingame.size[0], 2000))
        y = 10
        text_file = open("credits.txt", "r")

        surface.fill(self.back_color)

        for line in text_file.readlines():
            text = line.strip()
            if text == "":
                y += 26
                continue

            if not text[0] == "#":
                if text.startswith("H:"):
                    font = fonts.font_44
                    space = 44
                    remove = 2
                elif text.startswith("h:"):
                    font = fonts.font_32
                    space = 32
                    remove = 2
                else:
                    font = fonts.font_26
                    space = 26
                    remove = 0

                text = text.replace("%version_string", maingame.version_string)
                tsoliasgame.draw_text(surface, font, text[remove:],
                                      (maingame.size[0] / 2, y), tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
                y += space

        text_file.close()
        self.surface = surface
        return y

    @staticmethod
    def action_back():
        maingame.controller = MainMenuController()

class VirtualKeypad(object):
    """A virtual keypad"""
    @property
    def keypad_scale(self):
        return self.__keypad_scale

    # noinspection PyAttributeOutsideInit
    @keypad_scale.setter
    def keypad_scale(self, value):
        """resizes the keypad"""

        size = 32 * value
        if self.right_corner:
            self.position = (maingame.size[0] - size * 3 - 4,  maingame.size[1] - size * 3 - 4)  # position of keypad
        else:
            self.position = (10,  maingame.size[1] - size * 3 - 4)  # position of keypad

        # create buttons for keypad
        self.btn_u = tsoliasgame.Button(self.action_up,
                                        rect=pygame.Rect(self.position[0] + size, self.position[1], size, size))
        self.btn_d = tsoliasgame.Button(self.action_down,
                                        rect=pygame.Rect(self.position[0] + size, self.position[1] + 2 * size, size, size))
        self.btn_l = tsoliasgame.Button(self.action_left,
                                        rect=pygame.Rect(self.position[0], self.position[1] + size, size, size))
        self.btn_r = tsoliasgame.Button(self.action_right,
                                        rect=pygame.Rect(self.position[0] + 2 * size, self.position[1] + size, size, size))
        
        self.image = pygame.transform.scale(self.initial_image, (int(size * 3), int(size * 3)))  # resize the image
        self.__keypad_scale = value
        settings.set("keypad_scale", value)
        
    def __init__(self, visible=True, preview=False, right_corner=False):
        """
        creates a new virtual keypad
        :param visible: if the keypad will be visible
        :param preview: if the keypad will be in preview-only mode
        :param preview: if True keypad will be drawn in the right bottom corner - else left
        """

        self.visible = visible
        self.preview = preview
        self.right_corner = right_corner
        self.buttons = tsoliasgame.ButtonGroup()
        self.image = Images.arrows_image  # keypad image
        self.initial_image = self.image  # needed to later scale the image without compromising quality
        self.keypad_scale = settings.get("keypad_scale")  # set the initial scale from settings
        self.buttons.add(self.btn_u, self.btn_d, self.btn_l, self.btn_r)
        self.used = False  # this variable holds if a virtual button was pressed in the current frame
        
    def draw(self, surface):
        """must be called by parent controller every draw - does nothing if keypad is not visible"""
        if not self.visible:
            return
        surface.blit(self.image, self.position)
        if self.preview:  # draw "Preview Only" text
            draw_pos = tsoliasgame.vector2.add(self.position, tsoliasgame.vector2.multiply(.5, self.image.get_size()))
            tsoliasgame.draw_text(surface, fonts.font_26, "Preview Only!", draw_pos, tsoliasgame.colors.white,
                                  tsoliasgame.ALIGN_CENTER, tsoliasgame.ALIGN_CENTER)

    def mouse_down(self, event):
        """must be called by parent controller every mouse down - returns if a keypad button was pressed
        :rtype : bool
        """
        if self.preview:
            return False
        self.used = self.buttons.handle_clicks(event.pos)  # just let your buttons handle the event
        return self.used

    def mouse_up(self, event):
        """must be called by parent controller every mouse up
        :rtype : bool
        """
        self.used = False  # keypad has stopped being pressed
        return False

    # button actions...
    @staticmethod
    def action_up(pos):
        objs.Purple.direction = (0, -1)

    @staticmethod
    def action_down(pos):
        objs.Purple.direction = (0, 1)

    @staticmethod
    def action_left(pos):
        objs.Purple.direction = (-1, 0)

    @staticmethod
    def action_right(pos):
        objs.Purple.direction = (1, 0)
        

class Hud(object):

    def __init__(self, position, starting_controller):
        self.position = position

        self.background = Images.hud_image  # hud image
        self.padlock_closed = Images.padlock_closed_image
        self.padlock_open = Images.padlock_open_image

        btn_pause = tsoliasgame.Button(self.action_pause,
                                       rect=pygame.Rect(self.position[0] + 118, self.position[1] + 8, 32, 32))
        btn_padlock = tsoliasgame.Button(self.action_padlock,
                                         rect=pygame.Rect(self.position[0] + 74, self.position[1] + 8, 32, 32))

        starting_controller.buttons.add(btn_pause, btn_padlock)
        
    def draw(self, surface):
        surface.blit(self.background, self.position)
        if maingame.controller.camera_locked:
            surface.blit(self.padlock_closed, (self.position[0] + 74, self.position[1] + 8))
        else:
            surface.blit(self.padlock_open, (self.position[0] + 74, self.position[1] + 8))
            
        tsoliasgame.draw_text(surface, fonts.font_20, "x " + str(len(objs.Paint.all)),
                              [self.position[0] + 32, self.position[1] + 12], tsoliasgame.colors.black)

    @staticmethod
    def action_pause(pos):
        maingame.paused = not maingame.paused

    @staticmethod
    def action_padlock(pos):
        maingame.controller.camera_locked = not maingame.controller.camera_locked


class PauseMenu(object):
    def __init__(self, position):
        self.position = position
        self.x = 0
        self.deltax = 0

        self.background = Images.paused_image
        self.items = []
        self.items.append(MenuItem(Images.play_menu_image, self.action_resume, "Resume Game"))
        self.items.append(MenuItem(Images.restart_menu_image, self.action_restart, "Restart Game"))
        self.items.append(MenuItem(Images.back_menu_image, self.action_back, "Back To Level Selection"))
        self.items.append(MenuItem(Images.help_menu_image, self.action_help, "Help"))
        self.items.append(MenuItem(Images.options_menu_image, self.action_options, "Options"))
        self.items.append(MenuItem(Images.exit_menu_image, self.action_exit, "Exit Game"))
    
        self.center = [self.position[0] + self.background.get_width() / 2,
                       self.position[1] + self.background.get_height() / 2]

        self.buttons = tsoliasgame.ButtonGroup()
        self.buttons.add(
            tsoliasgame.Button(self.action_left, rect=pygame.Rect(self.center[0] - 84, self.center[1] - 20, 40, 40), sound=maingame.audio.sfx_click),
            tsoliasgame.Button(self.action_center, rect=pygame.Rect(self.center[0] - 32, self.center[1] - 32, 64, 64), sound=maingame.audio.sfx_click),
            tsoliasgame.Button(self.action_right, rect=pygame.Rect(self.center[0] + 44, self.center[1] - 20, 40, 40), sound=maingame.audio.sfx_click))
        
        self.swiped = False
        self.start_pos = (0, 0)
        
    def key_down(self, event):
        if not self.deltax == 0:
            return
        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            self.items[(self.x + 32) / 64].action()
        if event.key == pygame.K_LEFT:
            self.deltax = -64
        elif event.key == pygame.K_RIGHT:
            self.deltax = 64
        
    def mouse_down(self, event):
        self.start_pos = event.pos
        self.swiped = False
    
    def mouse_up(self, event):
        self.x = (self.x + 32) / 64 * 64
        if not self.swiped:
            self.buttons.handle_clicks(event.pos)

    def mouse_motion(self, event):
        if tsoliasgame.point_distance(self.start_pos, event.pos) > 5:
            self.swiped = True
        self.x -= event.rel[0]
        
    def draw(self, surface):
        if self.deltax > 0:
            self.x += 8
            self.deltax -= 8
        elif self.deltax < 0:
            self.x -= 8
            self.deltax += 8
            
        x_max = len(self.items) * 64
        self.x = (self.x + 32) % x_max - 32
        if self.x < -32:
            self.x = x_max - self.x
            
        surface.blit(self.background, self.position)
       
        x = self.x - 64
        for i in range(3):
            # make sure x is within bounds
            x %= x_max
            
            cur_item = x / 64
            difference = (i - 1) * 64 - self.x % 64
            scale = 64 - abs(difference / 2)
            new_image = pygame.transform.scale(self.items[cur_item].item, (scale, scale))
            surface.blit(new_image,
                         (self.position[0] + self.background.get_width() / 2 - scale / 2 + difference,
                          self.position[1] + self.background.get_height() / 2 - scale / 2))
            x += 64
            
        strr = self.items[(self.x + 32) / 64].description
        tsoliasgame.draw_text(surface, fonts.font_20, strr, [self.center[0], self.position[1] + 210],
                              tsoliasgame.colors.green, tsoliasgame.ALIGN_CENTER)

    def action_left(self, pos):
        self.deltax = -64

    def action_center(self, pos):
        self.items[(self.x + 32) / 64].action()

    def action_right(self, pos):
        self.deltax = 64
        
    @staticmethod
    def action_resume():
        maingame.paused = False

    @staticmethod
    def action_restart():
        maingame.paused = False
        GameplayController.restart_level()
        
    @staticmethod
    def action_back():
        if Question("Leave level?",
                    "Are you sure you want to return\n to level selection? \nCurrent level progress will be lost.").return_value:
            maingame.paused = False
            maingame.controller = LevelSelectionController()

    @staticmethod
    def action_help():
        maingame.controller = HelpController()

    @staticmethod
    def action_options():
        maingame.controller = OptionsController()

    @staticmethod
    def action_exit():
        if Question("Exit?", "Are you sure you want to exit? \nCurrent level progress will be lost.").return_value:
            maingame.exit()


class MenuItem(object):
    def __init__(self, item, action, description=""):
        """Defines a basic menu item

        :param item: main item info - can be a string or a image for example
        :param action: action to be called when item gets activated
        :param description: description - can be blank
        """
        self.item = item
        self.action = action
        self.description = description
