import tsoliasgame.settings
import os
import os.path


class Settings(tsoliasgame.settings.Settings):
    def __init__(self, save_dir, save_file):
        tsoliasgame.settings.Settings.__init__(self)
        self.first_time = False  # will be set to true later if save file was not found
        self.save_dir = save_dir
        self.save_file = os.path.join(save_dir, save_file)  # save file location
        
        self.defaults(True)  # start with defaults first
        
        # and attempt to load the file
        self.load()

    def save(self):
        # before saving we need to get the modified values of achievements
        import achievements
        for key, value in achievements.achievements.iteritems():
            self.set(key, value.main_value)

        tsoliasgame.settings.Settings.save(self, self.save_file)

    def load(self):
        if tsoliasgame.settings.Settings.load(self, self.save_file) == 1:
            self.first_time = True
            
    def defaults(self, progress=False):
        """sets default settings
        :param progress: if True it also resets variables related to progress
        """
        self.set("show_keypad", False)  # show keypad
        self.set("keypad_scale", 1.5)  # keypad size modifier
        self.set("blue_speed", 4)  # speed of character (and everything else that moves)
        self.set("fullscreen", False) # whether its fullscreen
        self.set("quality", True)  # graphics quality (True = normal quality, False = low)
        self.set("debug_mode", False)  # gives you things like level skip and jump main character to point
        self.set("sfx", 1.0)  # sfx volume
        self.set("music", 0.4)  # bgm volume
        self.set("downloaded_levels_dir", os.path.join(self.save_dir, "downloaded"))  # dir where new levels are stored
        self.set("level_download_dir", "https://raw.githubusercontent.com/2028games/PurpleFace_levels/master/")  # url to check for levels to download
        if progress:
            self.set("unlocked", 1)  # number of unlocked levels
            self.set("levels_won", [])  # list of won levels

            self.set("paint_collected", 0)
            self.set("times_restarted", 0)
            self.set("times_died", 0)
            self.set("total_time", 0)
            self.set("total_dist", 0)
            self.set("aheradrim", 0)


save_dir = os.path.join(os.path.expanduser("~"), ".PurpleFace")
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)
settings = Settings(save_dir, "settings.txt")