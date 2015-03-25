import colors
import pygame
import math
import xml.etree.ElementTree as eT
import importlib
import os
import re
import vector2
from buttons import Button, ButtonGroup

__all__ = ["ALIGN_LEFT", "ALIGN_CENTER", "ALIGN_RIGHT", "ALIGN_TOP", "ALIGN_BOT", "ANIMATION_STOP", "ANIMATION_RESET",
           "square_distance", "point_distance", "point_angle", "load_image", "load_module", "draw_text",
           "Group", "Obj", "View", "Level", "LevelGroup", "Game", "Button", "ButtonGroup"]

ALIGN_LEFT = ALIGN_TOP = 0
ALIGN_CENTER = 1
ALIGN_RIGHT = ALIGN_BOT = 2
ANIMATION_STOP = 0
ANIMATION_RESET = 1

module = None


def get_all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in get_all_subclasses(s)]

        
def square_distance(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return x * x + y * y


def point_distance(a, b):
    return math.sqrt(square_distance(a, b))


def point_angle(a, b):
    return vector2.get_angle((a[0] - b[0], b[1] - a[1]))


def load_image(image_file, convert=True, hascolorkey=False, colorkey=colors.white):
    image = pygame.image.load(image_file)
    if convert:
        image.convert()
    if hascolorkey:
        image.set_colorkey(colorkey)
    return image


def load_module(module_file):
    global module
    module = importlib.import_module(module_file)
    
    # add the .all attribute for all the new Objs
    subclasses = get_all_subclasses(Obj)
    for cls in subclasses:
        if issubclass(cls, Obj):
            cls.all = Group()
    return module


def draw_text(surface, font, text, position, color=colors.black, h_align=ALIGN_LEFT, v_align=ALIGN_TOP, antialiasing=True):
    lines = re.split(r"\n|\\n", text)  # splits when it finds \n char or "\n" as a 2-char string
    total_height = 0
    current_height = 0
    text_imgs = []
    for line in lines:
        text_img = font.render(line, antialiasing, color)
        text_imgs.append(text_img)
        total_height += text_img.get_height()
        
    for i in range(len(text_imgs)):
        end_pos = (position[0] - text_imgs[i].get_width() * (h_align / 2.0), 
                   position[1] - total_height * (v_align / 2.0) + current_height)
        surface.blit(text_imgs[i], end_pos)
        current_height += text_imgs[i].get_height()


class Group(pygame.sprite.LayeredDirty, object):
    def __init__(self, visible=True):
        pygame.sprite.LayeredDirty.__init__(self)
        self.visible = visible
    
    def add(self, *sprites, **kwargs):
        for obj in sprites:
            obj.groups.append(self)
        pygame.sprite.LayeredDirty.add(self, *sprites, **kwargs)
            
    def pre_update(self):
        for spr in self.sprites():
                spr.pre_update()
            
    def draw(self, surface):
        if self.visible:
            for spr in self.sprites():
                spr.draw(surface)
                
    def collidepoint(self, point):
        #checks if any obj collides with the specified point
        for spr in self.sprites():
            if spr.rect.collidepoint(point):
                return spr
        return None
    
    def check_same_pos(self, other):
        #check if any obj of the current group is in the same position with the other obj
        for spr in self.sprites():
            if spr.check_same_pos(other):
                return spr
        return None
               
drawables = Group()  # a group that contains all the objects that should be drawn


class Obj(pygame.sprite.DirtySprite):
    
    @property
    def position(self):
        return self.__position
    
    @position.setter        
    def position(self, value):
        self.__previous_pos = self.__position
        self.__position = value
        self.rect.x = value[0]
        self.rect.y = value[1]
        
    @property
    def previous_pos(self):
        return self.__previous_pos
    
        
    @property
    def visible(self):
        return self.__visible
    
    @visible.setter        
    def visible(self, value):
        if not value == self.__visible:
            self.__visible = value
            if value:
                drawables.add(self, layer=self.layer)
            else:
                drawables.remove(self)
        
    def __init__(self, image, layer=0, position=(0, 0), speed=(0, 0), accel=(0, 0), visible=True, usemask=True,
                 addtolevel=None):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = image
        self.layer = layer
        self.image_size = self.image.get_size()
        if usemask:
            self.mask = pygame.mask.from_surface(self.image, 200)
        self.rect = image.get_rect()
        self.__position = position
        self.position = position
        self.speed = speed
        self.accel = accel
        
        # animation variables
        self.animation_enabled = False
        self.__animation_rect = pygame.Rect((0, 0) + self.image_size)
        # the rect that represents the portion of the image to be drawn
        # by default it's equal to the image
        
        self.groups = []  # contains reference to all the groups that reference our Obj!
        
        # add Obj to the required groups
        
        # 1st to the drawables group
        self.__visible = False
        if visible:
            self.visible = True
        
        # 2nd to the specified level
        if addtolevel:
            addtolevel.add_obj(self, layer)
        
        # 3rd to .all property of each Obj child!
        cls = self.__class__
        while True:
            cls.all.add(self)
            cls = cls.__bases__[0]
            if cls == Obj:
                break

    def pre_update(self):
        """a function that should be executed before update
        It does nothing just override to use if needed"""
        pass
    
    def update(self):
        # M O V E M E N T
        self.speed = vector2.add(self.speed, self.accel)
        self.add_pos(self.speed)
        
        # A N I M A T I O N
        if self.animation_enabled:
            if self.__animation_counter <= 0:  # time to change image
                if self.animation_reversed:
                    if self.current_image == 0:  # if we reach min
                        if self.end_action == ANIMATION_RESET:
                            self.current_image = self.start_image  # restart from start
                        else:
                            self.animation_enabled = False  # stop
                    else:
                        self.current_image -= 1  # change_image
                else:
                    if self.current_image == self.max_image_count - 1:  # if we reach max
                        if self.end_action == ANIMATION_RESET:
                            self.current_image = self.start_image  # restart from start
                        else:
                            self.animation_enabled = False  # stop
                    else:
                        self.current_image += 1  # change_image
                
                self.__animation_rect.x = self.image_size[0] * (self.current_image % self.__max_image_x)  # set the x of the rect
                self.__animation_rect.y = self.image_size[1] * (self.current_image // self.__max_image_x)  # and the y
                self.__animation_counter = self.change_steps  # reset counter
            else:
                self.__animation_counter -= 1  # reduce counter by 1

    def draw(self, surface, moved=(0, 0)):
        surface.blit(self.image, (self.rect.x + moved[0], self.rect.y + moved[1]), self.__animation_rect)

    def set_center(self, x):
        """sets center of the object"""
        self.position = vector2.substract(x, vector2.multiply(.5, self.image_size))
    
    def add_pos(self, x):
        """moves object relatively to current pos"""
        self.position = vector2.add(self.__position, x)
    
    def get_center(self):
        """returns center of the object"""
        return self.__position[0] + self.image_size[0] / 2, self.__position[1] + self.image_size[1] / 2
    
    def check_grid(self, grid):
        """checks if object is snapped to grid"""
        return self.__position[0] % grid[0] == 0 and self.__position[1] % grid[1] == 0
    
    def snap_grid(self, grid):
        """snaps object to closest grid"""
        self.position = (round(float(self.position[0]) / grid[0]) * grid[0],
                         round(float(self.position[1]) / grid[1]) * grid[1])
        
    def check_collision_ahead(self, group, points=32):
        """checks whether a collision with the specified group of objects will happen ahead"""
        try:
            other = group.collidepoint(vector2.add(self.get_center(), vector2.multiply(points / vector2.get_length(self.speed), self.speed)))
        except ZeroDivisionError:
            return None
        if self == other:
            return None
        return other
    
    def check_same_pos(self, other):
        """checks whether current obj has the same pos with another obj"""
        return self.get_center() == other.get_center()
    
    def collide_circle(self, other):
        return point_distance(self.get_center(), other.get_center()) <= self.radius + other.radius
    
    def change_to(self, cls, centered=False, *attributes):
        """Change to another type of Obj and destroy current - it automatically copies position, speed, accel
        cls: class of other obj
        attributes: list of additional attributes to copy (shallow)"""
        obj = cls(position=self.__position, addtolevel=self.level)
        if centered:
            obj.set_center(self.get_center())
        obj.speed = self.speed
        obj.accel = self.accel
        
        for n in attributes:
            if hasattr(self, n):
                setattr(obj, n, getattr(self, n))
        self.destroy()
        return obj
        
    def destroy(self):
        """destroys the Obj - poor Obj!"""
        #it gets removed from every group it was added
        for group in self.groups:
            group.remove(self)
            
    def start_animation(self, image_size, change_steps=1, start_image=0, max_image_count=1000, animation_reversed=False
                        , end_action=ANIMATION_RESET):
        """use that to begin an animation on the defined object sprite
        it actually initializes all the variables needed for the animation"""
        self.rect.width = image_size[0]
        self.rect.height = image_size[1]
        self.image_size = image_size
        self.__animation_counter = self.change_steps = change_steps - 1
        self.__max_image_x = self.image.get_width() // image_size[0]
        self.current_image = self.start_image = start_image
        self.max_image_count = min(max_image_count,  self.__max_image_x * self.image.get_height() // image_size[1])
        self.__animation_rect = pygame.Rect((0, 0) + self.image_size)
        self.animation_reversed = animation_reversed
        self.end_action = end_action
        self.animation_enabled = True
        
        #finally set the current rect to that of the beginning image
        self.__animation_rect.x = self.image_size[0] * (self.current_image % self.__max_image_x)  # set the x of the rect
        self.__animation_rect.y = self.image_size[1] * (self.current_image // self.__max_image_x)  # and the y


class View(object):
    def __init__(self, position=(0, 0), following=None, limit_position=True):
        self.level = None
        self.position = position
        self.following = following
        self.surface = None
        self.limit_position = limit_position
        
    def update(self):
        if self.surface:
            if self.following:
                self.position = vector2.substract(self.following.get_center(), vector2.multiply(0.5, self.surface.get_size()))
            
            if self.limit_position:
                bound = self.level.size[0] - self.surface.get_width()
                x, y = self.position
                if bound < 0:
                    x = bound / 2
                else:
                    if x < 0:
                        x = 0
                    elif x > bound:
                        x = bound
                
                bound = self.level.size[1] - self.surface.get_height()
                if bound < 0:
                    y = bound / 2
                else:
                    if y < 0:
                        y = 0
                    elif y > bound:
                        y = bound

                self.position = (x, y)
            
    def draw(self, surface):
        self.surface = surface
        if drawables.visible:
            for spr in drawables.sprites():
                spr.draw(surface, vector2.multiply(-1, self.position))


class Level(object):
    def __init__(self, view, source_tmx="", properties_only=False):
        self.group = Group()
        self.view = view
        self.size = (0, 0)
        self.title = self.description = ""
        view.level = self
        
        #load tmx
        self.source_tmx = source_tmx
        if not source_tmx == "":
            self.load_tmx(source_tmx, properties_only)

    def load_tmx(self, source_tmx, properties_only=False):
        global module   
        tree = eT.parse(source_tmx)
        root = tree.getroot()
        if not root.tag.lower() == "map":
            return 1
        
        #extract properties to find title, description
        properties = root.find("properties")
        for propertyy in properties:
            name = propertyy.get("name")
            if name == "Title":
                self.title = propertyy.get("value")
            elif name == "Description":
                self.description = propertyy.get("value")
                
        if properties_only:
            return 0
                
        #get map size
        map_size = (int(root.get("width")), int(root.get("height")))
        self.tile_size = (int(root.get("tilewidth")), int(root.get("tileheight")))
        self.size = (map_size[0] * self.tile_size[0], map_size[1] * self.tile_size[1])
        
        layer = 0        
        for child in root:
            if child.tag.lower() == "layer":
                layer += 1
                data = child.find("data")
                if not data.get("encoding").lower() == "csv":
                    return 1
                    
                csv = data.text.strip()
                tiles = csv.replace("\n", "").split(",")
                for i in range(map_size[0] * map_size[1]):
                    if not tiles[i] == "0":
                        module.obj_from_tiles(layer, [self.tile_size[0] * (i % map_size[0]),
                                                         self.tile_size[1] * (i // map_size[0])], self, int(tiles[i]))
                    
    def add_obj(self, obj, layer=0):
        obj.level = self
        self.group.add(obj, layer=layer)
        
    def clear_all(self):
        for obj in self.group:
            obj.destroy()
    
    def pre_update(self):
        self.group.pre_update()

    def update(self):
        self.group.update()
        self.view.update()
        
    def draw(self, surface):
        self.view.draw(surface)

    def __del__(self):
        self.clear_all()


class LevelGroup(object):
    """A group of levels to be used in the game"""
    def __init__(self, view, level_changed=None):
        """

        :param level_changed: a function to call when the level is changed
        :param view: the view to be used in the levels
        """
        self.view = view
        self.__group = []  # the group of levels
        self.__current_index = -1  # index of current level
        self.level_changed = level_changed
    
    def __len__(self):
        return len(self.__group)
    
    def __getitem__(self, key):
        return self.__group[key]

    def __contains__(self, item):
        for level in self.__group:
            if item == os.path.basename(level.source_tmx):
                return True
        return False

    def current(self):
        """get current level"""
        if self.current_index() == -1:
            return None
        return self[self.__current_index]
    
    def current_index(self):
        """get current level"""
        if self.__current_index >= len(self.__group):
            return -1
        return self.__current_index
    
    def add(self, *levels):
        """add levels
        :param levels: a list of strings - the file location of each level's tmx"""
        for level_location in levels:
            level = Level(self.view, level_location, True)
            self.__group.append(level)
            
    def from_file(self, location):
        """loads a level list from a file"""
        text_file = open(location, "r")
        for line in text_file.readlines():
            text = line.strip()
            if not text[0] == "#":
                self.add(os.path.join(os.path.dirname(location), text))
        text_file.close()
        
    def from_directory(self, directory):
        """loads all tmxs from a directory (except those that start with '.')"""
        for child in sorted(os.listdir(directory)):
            full_path = os.path.join(directory, child)
            (name, extension) = os.path.splitext(child)
            if os.path.isfile(full_path) and extension == ".tmx" and not name[0] == ".":
                self.add(full_path)

    def reset(self):
        """resets levelgroup to empty"""
        self.__group = []
        self.__current_index = -1
                
    def start_level(self, index=0, fire_level_changed=True):
        """start a level"""
        if index == -1:
            return 1
        if not self.__current_index == -1:  # if there was already a level made before
            self.current().clear_all()  # clear its objects
        self.__group[self.__current_index] = Level(self.view, self[self.__current_index].source_tmx, True)
        self.__current_index = index
        self.__group[self.__current_index] = Level(self.view, self[index].source_tmx, False)  # and make the new one
        if fire_level_changed and self.level_changed:
            self.level_changed()
        
    def restart_current(self, fire_level_changed=True):
        """restart current level"""
        self.start_level(self.__current_index, fire_level_changed)
        
    def jump_next(self, fire_level_changed=True):
        """goto next level
        if the current level is the last one this function does nothing but return True"""
        if self.__current_index == len(self) - 1:
            return True
        self.start_level(self.__current_index + 1, fire_level_changed)
        return False
        
    def jump_previous(self, fire_level_changed=True):
        """goto previous level
        if the current level is the first one this function does nothing but return True"""
        if self.__current_index == 0:
            return True
        self.start_level(self.__current_index - 1, fire_level_changed)
        return False
    
    @staticmethod
    def check_empty_dir(directory):
        """checks if given directory is empty (has no tmxs)"""
        for child in os.listdir(directory):
            full_path = os.path.join(directory, child)
            (name, extension) = os.path.splitext(child)
            if os.path.isfile(full_path) and extension == ".tmx" and not name[0] == ".":
                return False
        return True


class Game(object):
    """A game class - dont use directly - inherit it!"""
    def __init__(self, fps, levels, size, flags=0):
        """this function also initializes pygame
        fps: desired framerate
        levels: main LevelGroup
        size: window size - set size[0] to 0 to automatically choose best aspect ratio"""

        if size[0] == 0:
            size_y = size[1]
            size = pygame.display.list_modes()
            size_x = int(size_y * size[0][0] / float(size[0][1]))
            size = (size_x, size_y)
            
        self.fps = fps
        self.levels = levels
        self.size = size
        self.__exit = False  # when this variable goes true game ends
        self.paused = False  # when this variable goes true game pauses
        self.__step_time = 10  # this variable is used to count fps
        self.__clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode(size, flags)
        
    def start(self, drawing_surface, level=0):
        """start the game
        drawing_surface: the surface where the game should be drawn (usually self.screen)
        level: index of the level to start from"""
        self.levels.start_level(level)
        self.main_loop(drawing_surface)
        
    def main_loop(self, drawing_surface):
        """main loop - it just calls the following functions:
        self.event_handling
        self.pre_update
        self.update
        self.draw"""
        
        while not self.__exit:
            self.event_handling()
            if not self.paused:
                self.pre_update()
                self.update()
            self.draw(drawing_surface)
                
            self.__step_time = self.__clock.tick(self.fps) #limits fps to desired
            
    def event_handling(self):
        """event handling: does almost nothing by default - TO BE EXTENDED IN AN ACTUAL GAME"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            
    def pre_update(self):
        """gets called before update and calls pre_update of all Objs in level - TO BE EXTENDED IN AN ACTUAL GAME"""
        self.levels.current().pre_update()
        
    def update(self):
        """calls update of all Objs in level - TO BE EXTENDED IN AN ACTUAL GAME"""
        self.levels.current().update()
            
    def draw(self, surface):
        """calls draw of all Objs in level - TO BE EXTENDED IN AN ACTUAL GAME
        Notice: if game.screen is used as surface remember to flip the display afterwards"""
        self.levels.current().draw(surface)
        
    def exit(self):
        """exits game, not imediatelly but in next step"""
        self.__exit = True
        
    def get_fps(self):
        """returns current fps"""
        return 1000 / self.__step_time