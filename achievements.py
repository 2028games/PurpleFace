import collections
from settings import settings
from maingame import maingame
import fonts
import tsoliasgame
import pygame
from images import Images

class AchievementLevel(object):
    def __init__(self, check_value, title, description, image):
        self.check_value = check_value
        self.title = title
        self.description = description
        self.image = image


class Achievement(object):
    achievement_to_draw = None
    step = 0

    @property
    def main_value(self):
        return self.__main_value

    @main_value.setter
    def main_value(self, value):
        self.__main_value = value
        self.check_progress()

    def __init__(self, start_value, check, levels):
        self.__main_value = start_value
        self.check = check
        self.levels = levels
        self.current_level = self.get_current_level()

    def get_current_level(self):
        current_level = 0
        for level in self.levels:
            if self.check(self.main_value, level.check_value):
                current_level += 1
            else:
                return current_level

        return current_level

    def check_progress(self):
        curr_level = self.get_current_level()
        if curr_level > self.current_level:
            self.current_level = curr_level
            Achievement.achievement_to_draw = self
            return True
        return False

    @staticmethod
    def draw_achievement(surface):
        if not Achievement.achievement_to_draw:
            return
        if Achievement.step >= 5 * maingame.fps:
            Achievement.achievement_to_draw = None
            Achievement.step = 0
            return

        position = (maingame.size[0] / 2, min(100, 100.0 * Achievement.step / maingame.fps))
        curr_level = Achievement.achievement_to_draw.levels[Achievement.achievement_to_draw.current_level - 1]

        pygame.draw.rect(surface, tsoliasgame.colors.dodgerblue, pygame.Rect(position[0] - 200, 0, 400, position[1]))

        tsoliasgame.draw_text(surface, fonts.font_32, "Achievement Completed!",
                              (position[0], position[1] - 95), tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
        tsoliasgame.draw_text(surface, fonts.font_26, curr_level.title,
                              (position[0], position[1] - 60), tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
        tsoliasgame.draw_text(surface, fonts.font_20, curr_level.description,
                              (position[0], position[1] - 30), tsoliasgame.colors.white, tsoliasgame.ALIGN_CENTER)
        surface.blit(curr_level.image, (position[0] - 180, position[1] - 80))

        Achievement.step += 1

achievements = collections.OrderedDict([
    ("paint_collected", Achievement(settings.get("paint_collected"), lambda current, x: current >= x,
                                    (AchievementLevel(20, "Novice Collector", "Collect 20 paint splatters", Images.medal1_image),
                                     AchievementLevel(50, "Average Collector", "Collect 50 paint splatters", Images.medal2_image),
                                     AchievementLevel(100, "Expert Collector", "Collect 100 paint splatters", Images.medal3_image)))),

    ("times_restarted", Achievement(settings.get("times_restarted"), lambda current, x: current >= x,
                                    (AchievementLevel(10, "A Few Fails", "Restart a total of 10 times", Images.medal1_image),
                                     AchievementLevel(30, "More Fails", "Restart a total of 30 times", Images.medal2_image),
                                     AchievementLevel(100, "Way too Many Fails", "Restart a total of 100 times", Images.medal3_image)))),

    ("times_died", Achievement(settings.get("times_died"), lambda current, x: current >= x,
                               (AchievementLevel(10, "A Few Deaths", "Die a total of 10 times", Images.medal1_image),
                                AchievementLevel(20, "More Deaths", "Die a total of 20 times", Images.medal2_image),
                                AchievementLevel(40, "Lots of deaths", "Die a total of 40 times", Images.medal3_image)))),

    ("total_time", Achievement(settings.get("total_time"), lambda current, x: current >= x,
                               (AchievementLevel(600, "10 Minutes", "Play a total of 10 minutes", Images.medal1_image),
                                AchievementLevel(3600, "1 hour", "Play a total of 1 hour", Images.medal2_image),
                                AchievementLevel(86400, "Lost a day!", "Play a total of 24 hours", Images.medal3_image)))),

    ("total_dist", Achievement(settings.get("total_dist"), lambda current, x: current >= x,
                               (AchievementLevel(1024, "A few pixels", "Travel a total of 1024 pixels", Images.medal1_image),
                                AchievementLevel(4096, "More pixels", "Travel a total of 4096 pixels", Images.medal2_image),
                                AchievementLevel(40000, "Round the pixel earth!", "Travel a total of 40000 pixels", Images.medal3_image)))),

    ("aheradrim", Achievement(settings.get("aheradrim"), lambda current, x: current >= x,
                              (AchievementLevel(1, 'The Aheradrim "Feature"!', "Discover a hidden secret", Images.medal_aheradrim_image),)))


])
print("test")