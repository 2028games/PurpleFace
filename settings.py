import tsoliasgame.settings


class Settings(tsoliasgame.settings.Settings):
    def __init__(self, location):
        tsoliasgame.settings.Settings.__init__(self)
        self.first_time = False  # will be set to true later if save file was not found
        self.location = location  # save file location
        
        self.defaults(True)  # start with defaults first
        
        # and attempt to load the file
        if self.load():  # error value returned
            self.save()  # save the defaults

    def save(self):
        tsoliasgame.settings.Settings.save(self, self.location)

    def load(self):
        if tsoliasgame.settings.Settings.load(self, self.location) == 1:
            self.save()
            self.first_time = True
            
    def defaults(self, progress=False):
        """sets default settings
        :param progress: if True it also resets variables related to progress
        """
        self.set("show_keypad", False)  # show keypad
        self.set("keypad_scale", 1.5)  # keypad size modifier
        self.set("blue_speed", 4)  # speed of character (and everything else that moves)
        self.set("fullscreen", False)
        self.set("quality", True)  # graphics quality (True = normal quality, False = low)
        self.set("debug_mode", False)  # gives you things like level skip and jump main character to point
        self.set("sfx", 1.0)  # sfx volume
        self.set("music", 0.4)  # bgm volume
        self.set("downloaded_levels_dir", "downloaded")  # dir where new levels are stored
        self.set("level_download_dir", "https://raw.githubusercontent.com/2028games/PurpleFace_levels/master/")  # url to check for levels to download
        if progress:
            self.set("unlocked", 1)  # number of unlocked levels
            self.set("levels_won", [])  # list of won levels
        
settings = Settings("settings.txt")