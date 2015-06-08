import random
import dialogs
import tsoliasgame
import pygame
import maingame
import achievements
from settings import settings
from images import Images


# L A Y E R 3

class Moveable(tsoliasgame.Obj):
    # all objects that move inherit from this (rocks and blues)
    def __init__(self, image, layer=3, position=(0, 0), speed=(0, 0), addtolevel=None, shrink_image=None):
        tsoliasgame.Obj.__init__(self, image, layer, position, speed, usemask=False, addtolevel=addtolevel)
        self.paused = False  # controls if update happens normally
        self.dead = False  # controls if dead - obviously
        self.shrink_image = shrink_image
        self.initial_image = image

    def on_grid_update(self):
        # must be called when on grid for each update
        # returns if update should stop

        # collision with mover
        if not self.speed == (0, 0):
            other = Mover.all.check_same_pos(self)
            if other:
                self.speed = tsoliasgame.vector2.multiply(2 * Purple.spd, other.__class__.direction)
                return True

        # collision with Death
        if Death.all.check_same_pos(self):
            self.start_shrink()  # start shrinking
            self.dead = True
            return True

        # collision with Teleporter_En
        other = TeleporterEn.all.check_same_pos(self)
        if other:
            self.start_shrink()

            self.other_teleporter = other  # remember so we can later delete this
            TeleporterEn.teleporting = self  # we must remember which obj instance is teleporting

            for teleporter in TeleporterEn.all:
                if not teleporter == other:
                    teleporter.change_to(TeleporterActive, True)
            return True

        return False

    def on_update_end(self):
        # must be called on the end of each update
        if self.paused:
            # SHRINK ANIMATION - ONLY IF PAUSED
            if self.animation_reversed:  # DESHRINKING
                if self.current_image == 0:  # end of effect
                    self.paused = False  # enable movement again
                    Purple.paused = False
                    Purple.aheradrim = False
                    self.image = self.initial_image  # and restore correct image
            else:  # SHRINKING
                if self.current_image == 7:  # end of effect
                    if self.dead:  # we are shrinking due to death tile
                        # DIE
                        self.die()
                    else:  # we are shrinking due to teleporter tile
                        self.visible = False  # hide

    def die(self):
        self.destroy()  # destroy me - will be overriden if needed
        Purple.paused = False

    def start_shrink(self):
        # enable shrink effect (for when teleporting)
        self.image = self.shrink_image
        self.start_animation((32, 32), 2, end_action=tsoliasgame.ANIMATION_STOP)
        self.paused = True  # disables update
        Purple.paused = True  # for blue too
        self.speed = [0, 0]
        maingame.maingame.audio.sfx_suck.play()


class Purple(Moveable):
    spd = settings.get("blue_speed")  # speed the object should take when a key is pressed
    paused = False
    aheradrim = False
    direction = (0, 0)  # the direction the object should move according to input

    def __init__(self, layer=3, position=(0, 0), speed=(0, 0), addtolevel=None):
        Moveable.__init__(self, Images.blue_blink_image, layer, position, speed, addtolevel=addtolevel,
                          shrink_image=Images.blue_shrink_image)
        Purple.paused = False

        self.radius = 16
        self.collided = 0
        self.__blink = maingame.maingame.fps * 10
        self.start_animation((32, 32), 1)
        maingame.maingame.levels.view.following = self

    def update(self):
        if not Purple.paused:
            if self.check_grid((32, 32)):  # checks grid

                if not self.position == self.previous_pos:
                    # update move achievement
                    achievements.achievements["total_dist"].main_value += 32

                    # aheradrim
                    if self.position[0] == -96 and not Purple.aheradrim and \
                       "secret" in maingame.maingame.levels.current().description:
                        achievements.achievements["aheradrim"].main_value = 1
                        Purple.aheradrim = True
                        self.image = Images.aheradrim_image

                if not self.on_grid_update():  # if update was not handled by parent
                    # handle it now
                    # collision with Exit
                    other = Exit.all.check_same_pos(self)
                    if other:
                        if other.check_enabled():
                            # LEVEL WON

                            # first add to the list of won levels
                            current_level_location = maingame.maingame.levels.current().source_tmx
                            levels_won = settings.get("levels_won")
                            if current_level_location not in levels_won:
                                levels_won.append(current_level_location)

                            # then increment unlocked if needed
                            unlocked = settings.get("unlocked")
                            if maingame.maingame.levels.current_index() == unlocked - 1:
                                settings.set("unlocked", unlocked + 1)

                            settings.save()  # and save

                            if maingame.maingame.levels.jump_next():
                                maingame.maingame.exit()  # exit game TODO: make a proper winning message
                            return

                    # collision with Paint
                    other = Paint.all.check_same_pos(self)
                    if other:
                        achievement = achievements.achievements["paint_collected"]
                        achievement.main_value += 1

                        maingame.maingame.audio.sfx_pickup.play()
                        other.destroy()
                        if len(Paint.all) == 0:
                            Exit.all.get_sprite(0).enable()

                    # collision with Switch
                    if SwitchEn.all.check_same_pos(self):
                        SwitchEn.action()

                    # collision with Tutorial
                    other = Tutorial.all.check_same_pos(self)
                    if other and not other.inactive:
                        dialogs.message.show("Tutorial", Tutorial.messages[Tutorial.current])
                        Tutorial.current = min(Tutorial.current + 1, len(Tutorial.messages) - 1)
                        other.destroy()

                    # handle keyboard
                    if self.speed == (0, 0) or not Ice.all.check_same_pos(self):  # if we are not sliding
                        if self.collided <= 0:  # if it is not moving then set speed according to key pressed
                            self.speed = tsoliasgame.vector2.multiply(Purple.spd, Purple.direction)
                        else:
                            self.speed = (0, 0)

                # anyway check if target position is occupied
                if self.check_collision_ahead(Wall.all) and not Purple.aheradrim:  # collision with wall
                    self.speed = (0, 0)  # set speed to 0
                else:
                    other = self.check_collision_ahead(WoodenBox.all)  # collision with wooden box
                    if other:
                        if tsoliasgame.vector2.get_length(self.speed) <= Purple.spd:
                            self.speed = (0, 0)
                        else:
                            other.destroy()

            else:  # not on grid
                other = pygame.sprite.spritecollideany(self, Rock.all,
                                                       tsoliasgame.Obj.collide_circle)  # check collision with rocks
                if other:
                    other.speed = self.speed
                    # if there is another rock or wall ahead of the collided rock
                    if other.check_collision_ahead(Wall.all) or other.check_collision_ahead(Rock.all) \
                            or other.check_collision_ahead(WoodenBox.all):
                        self.speed = (0, 0)  # set the speed of everything to 0 and snap to grid
                        self.snap_grid((32, 32))
                        other.speed = (0, 0)

                    else:
                        other.collided = True
                        # the other.collided will prevent the rock from instantly setting its speed to 0

                        self.speed = tsoliasgame.vector2.multiply(-1, other.speed)  # reverse self speed

                    self.collided = int(maingame.maingame.get_fps() * 0.3)
                    # and set self.collided so that we dont allow keypresses to work for ~500ms

        self.collided -= 1

        # HANDLE ANIMATION
        self.on_update_end()
        if not self.paused and not Purple.aheradrim:
            # BLINK ANIMATION - ONLY IF NOT PAUSED
            if self.current_image == 0:
                if self.__blink <= 0:
                    self.animation_enabled = True
                    self.__blink = maingame.maingame.fps * 10
                else:
                    self.animation_enabled = False
                    self.__blink -= 1

        tsoliasgame.Obj.update(self)

    def die(self):
        # update death achievement
        achievements.achievements["times_died"].main_value += 1

        from controllers import GameplayController
        GameplayController.restart_level()

    @staticmethod
    def handle_keyboard():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            Purple.direction = (0, -1)
        elif keys[pygame.K_DOWN]:
            Purple.direction = (0, 1)
        elif keys[pygame.K_LEFT]:
            Purple.direction = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            Purple.direction = (1, 0)
        else:
            Purple.direction = (0, 0)

    @staticmethod
    def colorize_images(blue_factor):
        new_image = Images.blue_blink_original.copy()
        pixel_array = pygame.PixelArray(new_image)
        pixel_array.replace((0, 0, 255), (160, 0, int(blue_factor * 160)), 0, (1.0, 1.0, 0))
        pixel_array = None
        Images.blue_blink_image.blit(new_image, (0, 0))
        Images.blue_blink_image.convert()

        new_image = Images.blue_shrink_original.copy()
        pixel_array = pygame.PixelArray(new_image)
        pixel_array.replace((0, 0, 255), (160, 0, int(blue_factor * 160)), 0, (1.0, 1.0, 0))
        pixel_array = None
        Images.blue_shrink_image.blit(new_image, (0, 0))
        Images.blue_shrink_image.convert()


class Paint(tsoliasgame.Obj):
    def __init__(self, layer=2, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, Images.splatters_image, layer, position, usemask=False, addtolevel=addtolevel)
        self.start_animation((32, 32), start_image=random.randint(0, 7))

    def update(self):
        pass  # no update needed


# L A Y E R 2


class Rock(Moveable):
    def __init__(self, layer=1, position=(0, 0), addtolevel=None):
        Moveable.__init__(self, Images.rock_image, layer, position, addtolevel=addtolevel, shrink_image=Images.rock_shrink_image)
        self.radius = 16
        self.collided = False

    def update(self):
        # almost same code with the Purple without having independent movement - only sliding ability
        if not (self.position == self.previous_pos or self.paused):
            if not self.collided and self.check_grid((32, 32)):  # checks grid

                # again call parent update and then check if target position is occupied or if we are sliding
                if (not self.on_grid_update() and not Ice.all.check_same_pos(self)) or \
                        self.check_collision_ahead(Wall.all) or self.check_collision_ahead(Rock.all):
                    self.speed = (0, 0)  # set speed to 0
                else:
                    other = self.check_collision_ahead(WoodenBox.all)  # collision with wooden box
                    if other:
                        if tsoliasgame.vector2.get_length(self.speed) <= Purple.spd:
                            self.speed = (0, 0)
                        else:
                            other.destroy()

            elif self.collided:
                self.collided = False
                maingame.maingame.audio.sfx_push.play()

        self.on_update_end()

        tsoliasgame.Obj.update(self)


# L A Y E R 1


class Wood(tsoliasgame.Obj):
    def __init__(self, layer=1, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, Images.wood_image, layer, position, usemask=False, addtolevel=addtolevel)
        self.below = None  # contains the class of the object that is below...

    def update(self):
        for other in self.level.group:  # checks every Obj
            if (not (self == other or other.__class__ == Exit or other.__class__ == Paint)) and \
                    pygame.sprite.collide_rect(self, other):  # if they collide
                self.below = other.__class__
                if hasattr(other, "tile"):
                    self.tile_data = other.tile  # copy tile info (currently only needed for walls)
                other.destroy()
                self.change_to(Wood2, False, "below", "tile_data")
                return  # collision handled so we leave the function


class Wood2(Wood):
    # do not instantiate this directly! instead, wood is converted into wood2 when it finds something behind
    def __init__(self, position=(0, 0), addtolevel=None):
        Wood.__init__(self, layer=1, position=position, addtolevel=addtolevel)
        self.collided = False  # whether it has colllided

    def update(self):
        other = pygame.sprite.spritecollideany(self, Purple.all)  # collision with blue
        if other:
            self.collided = True
        else:
            other = pygame.sprite.spritecollideany(self, Rock.all)  # collision with rock
            if other:
                self.collided = True
            elif self.collided:  # if there is no collision in current step but there was before
                # create the "below" again
                if hasattr(self, "tile_data"):
                    self.below(position=self.position, addtolevel=self.level, tile=self.tile_data)
                else:
                    self.below(position=self.position, addtolevel=self.level)  
                self.destroy()


# L A Y E R 0


class Wall(tsoliasgame.Obj):
    def __init__(self, layer=0, position=(0, 0), addtolevel=None, tile=0):
        tsoliasgame.Obj.__init__(self, Images.wall_image, layer, position, usemask=False, addtolevel=addtolevel)
        self.tile = tile
        self.start_animation((32, 32), start_image=tile)

    def update(self):
        pass  # no update needed


class Death(tsoliasgame.Obj):
    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, Images.death_image, layer, position, usemask=False, addtolevel=addtolevel)

    def update(self):
        pass  # no update needed


class Exit(tsoliasgame.Obj):
    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, Images.exit_image, layer, position, usemask=False, addtolevel=addtolevel)
        self.__enabled = False
        self.start_animation((32, 32), 25, 1)
        self.animation_enabled = False
        self.current_image = 0

    def enable(self):
        self.__enabled = True
        self.current_image = 1
        self.animation_enabled = True

    def check_enabled(self):
        return self.__enabled


class Mover(tsoliasgame.Obj):
    direction = (0, 0)

    def __init__(self, image, layer=0, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, image, layer, position, usemask=False, addtolevel=addtolevel)

        # animation init code - only on normal quality
        if settings.get("quality"):
            animspeed = 1
            self.start_animation((32, 32), animspeed)  # start animation

            # if there is already another mover we need to synchronize with it however
            for mover in self.__class__.all:
                if not mover == self:  # make sure we are not using equality with ourselves
                    self.current_image = mover.current_image
                    break
        else:  # needed to draw only the first 32x32 part instead of whole image
            self.start_animation((32, 32), 1)
            self.animation_enabled = False


class MoverU(Mover):
    direction = (0, -1)

    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        Mover.__init__(self, Images.moverU_image, layer, position, addtolevel=addtolevel)


class MoverD(Mover):
    direction = (0, 1)

    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        Mover.__init__(self, Images.moverD_image, layer, position, addtolevel=addtolevel)


class MoverL(Mover):
    direction = (-1, 0)

    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        Mover.__init__(self, Images.moverL_image, layer, position, addtolevel=addtolevel)


class MoverR(Mover):
    direction = (1, 0)

    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        Mover.__init__(self, Images.moverR_image, layer, position, addtolevel=addtolevel)


class Switch(tsoliasgame.Obj):
    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, None, layer, position, usemask=False, addtolevel=addtolevel)

    def update(self):
        pass  # no update needed


class SwitchEn(Switch):
    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, Images.switch_en_image, layer, position, usemask=False, addtolevel=addtolevel)

    @staticmethod
    def action():
        for mover in Mover.all:
            if mover.__class__ == MoverU:
                mover.change_to(MoverD)
            elif mover.__class__ == MoverD:
                mover.change_to(MoverU)
            elif mover.__class__ == MoverL:
                mover.change_to(MoverR)
            elif mover.__class__ == MoverR:
                mover.change_to(MoverL)

        for switch in Switch.all:
            if switch.__class__ == SwitchEn:
                switch.change_to(SwitchDis)
            elif switch.__class__ == SwitchDis:
                switch.change_to(SwitchEn)


class SwitchDis(Switch):
    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, Images.switch_dis_image, layer, position, usemask=False, addtolevel=addtolevel)


class Ice(tsoliasgame.Obj):
    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, Images.ice_image, layer, position, usemask=False, addtolevel=addtolevel)

    def update(self):
        pass  # no update needed


class TeleporterEn(tsoliasgame.Obj):
    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, Images.teleporter_image, layer, position, usemask=False, addtolevel=addtolevel)

    def update(self):
        pass  # no update needed


class TeleporterDis(tsoliasgame.Obj):
    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, Images.teleporter_dis_image, layer, position, usemask=False, addtolevel=addtolevel)

    def update(self):
        pass  # no update needed


class TeleporterActive(tsoliasgame.Obj):
    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, Images.teleporter_active_image, layer, position, usemask=False, addtolevel=addtolevel)
        self.visible = True
        self.start_animation((64, 64), maingame.maingame.fps)

    @staticmethod
    def mouse_up(event):
        # for each teleporter
        for teleporter in TeleporterActive.all:
            # check if clicked
            if tsoliasgame.point_distance(
                    tsoliasgame.vector2.substract(teleporter.get_center(), maingame.maingame.levels.view.position),
                    event.pos) < 24:
                TeleporterEn.teleporting.set_center(teleporter.get_center())  # move other to teleporter's position
                TeleporterEn.teleporting.visible = True  # show blue again
                TeleporterEn.teleporting.start_animation((32, 32), 2, 7,
                                                         animation_reversed=True,
                                                         end_action=tsoliasgame.ANIMATION_STOP)  # enable deshrink efect
                TeleporterEn.teleporting.other_teleporter.change_to(TeleporterDis, True)  # disable entrance teleporter

                teleporter.change_to(TeleporterDis, True)  # disable exit teleporter

                # then change all active teleporters back to original
                # or if there is only teleporter left deactivate him too so that the player doesnt get stuck
                if len(TeleporterActive.all) > 1:
                    teleporter_type = TeleporterEn  # stores the type active teleporters should become
                else:
                    teleporter_type = TeleporterDis

                for teleporter2 in TeleporterActive.all:
                    teleporter2.change_to(teleporter_type, True)

                break


class Tutorial(tsoliasgame.Obj):
    current = 0
    messages = (
        "Welcome to PurpleFace! \n Use the arrow keys to move!",
        "Your purpose is to collect those\nsplatters of blue paint \nthat are scattered in the level.",
        "To your right you can see a\nmover tile. They allow movement\nin one direction only.\nThey also double your speed temporarily,\nwhich can be useful sometimes!",
        "Hmm, this mover is blocking\n your way. What will you do?",
        "Nice!\nNow you can see ice on the\n road ahead. Ice makes you slide.",
        "To your left there is a rock. You\ncan push rocks by moving towards them.\nThere are also some other tiles.\nStep on them to see what happens!",
        "Ok next time dont fall into\nblack holes they can kill you :)\n Now, you have to collect\nthe remaining paint.",
        "If you have collected all the paint\nyou can now go to the next\nlevel throught the exit.\nIf not, press [R] to restart.",
        "As you might have noticed,\nwooden boxes are unmovable\nbut can be broken with higher speed.",
        "Goodbye!"
    )

    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, Images.ice_image, layer, position, visible=False, usemask=False, addtolevel=addtolevel)
        self.inactive = maingame.maingame.fps / 3

    def update(self):
        if self.inactive > 0:
            self.inactive -= 1


def obj_from_tiles(layer, position, addtolevel, tile):
    wall_tiles = 77
    tmx_bindings = {1: Exit, 2: Wall, 3: Ice, 4: Death, 5: TeleporterEn, 6: Tutorial,
                    9: MoverU, 10: MoverD, 11: MoverL, 12: MoverR, 13: SwitchDis, 14: SwitchEn,
                    17: Wood, 19: WoodenBox, 25: Rock, 33: Purple, 34: Paint}
                    
    if tile <= wall_tiles:
        return Wall(layer=layer, position=position, addtolevel=addtolevel, tile=tile - 1)
    else:
        try:
            obj_type = tmx_bindings[tile - wall_tiles]
            return obj_type(layer=layer, position=position, addtolevel=addtolevel)
        except KeyError:
            print(tile)


class WoodenBox(tsoliasgame.Obj):
    def __init__(self, layer=0, position=(0, 0), addtolevel=None):
        tsoliasgame.Obj.__init__(self, Images.wooden_box_image, layer, position, usemask=False, addtolevel=addtolevel)

    def update(self):
        pass  # no update needed
