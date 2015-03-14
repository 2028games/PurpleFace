from images import Images
import maingame
import tsoliasgame
import pygame
import fonts


class Question():
    def __init__(self):
        self.surface = maingame.maingame.screen
        self.background = Images.question_image
        self.position = ((self.surface.get_width() - self.background.get_width()) / 2,
                         (self.surface.get_height() - self.background.get_height()) / 2)
        self.clock = pygame.time.Clock()
        self.rect_yes = pygame.Rect(self.position[0], self.position[1] + 200, 198, 50)
        self.rect_no = pygame.Rect(self.position[0] + 202, self.position[1] + 200, 198, 50)
        
    def show(self, title, text):

        previous_screen = self.surface.copy()  # i keep the last screen so that i can draw it again in every tick

        x = self.surface.get_width()
        move_mode = 0  # towards the left
        while True:
            # a fancy transition effect on the x axis!
            if move_mode == 0 and x > self.position[0] - 100:
                x -= 64
            elif x < self.position[0]:
                move_mode = 1  # towards the right
                x += 16
            else:
                x = self.position[0]
                move_mode = 2  # no movement

            if move_mode == 2:  # the transition effect has ended
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # immediately end game
                        maingame.maingame.exit()  # ask the game to exit
                        return False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_y:
                            return True
                        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_n:
                            return False

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if self.rect_yes.collidepoint(event.pos):
                            return True
                        elif self.rect_no.collidepoint(event.pos):
                            return False

            self.surface.blit(previous_screen, (0, 0))
            self.surface.blit(self.background, (x, self.position[1]))

            tsoliasgame.draw_text(self.surface, fonts.font_44, title,
                                  [x + self.background.get_width() / 2, self.position[1] + 30],
                                  tsoliasgame.colors.green, tsoliasgame.ALIGN_CENTER, tsoliasgame.ALIGN_CENTER)
            tsoliasgame.draw_text(self.surface, fonts.font_26, text,
                                  [x + self.background.get_width() / 2, self.position[1] + 120],
                                  tsoliasgame.colors.green, tsoliasgame.ALIGN_CENTER, tsoliasgame.ALIGN_CENTER)
            tsoliasgame.draw_text(self.surface, fonts.font_36, "Yes",
                                  [x + self.background.get_width() / 4, self.position[1] + 222],
                                  tsoliasgame.colors.green, tsoliasgame.ALIGN_CENTER, tsoliasgame.ALIGN_CENTER)
            tsoliasgame.draw_text(self.surface, fonts.font_36, "No",
                                  [x + 3 * self.background.get_width() / 4, self.position[1] + 222],
                                  tsoliasgame.colors.green, tsoliasgame.ALIGN_CENTER, tsoliasgame.ALIGN_CENTER)

            pygame.display.flip()

            self.clock.tick(maingame.maingame.fps)


class Message():
    def __init__(self):
        self.surface = maingame.maingame.screen
        self.background = Images.message_image
        self.position = ((self.surface.get_width() - self.background.get_width()) / 2,
                         (self.surface.get_height() - self.background.get_height()) / 2)
        self.clock = pygame.time.Clock()
        self.rect_ok = pygame.Rect(self.position[0] + 100, self.position[1] + 200, 200, 50)

    def show(self, title, text):

        previous_screen = self.surface.copy()  # i keep the last screen so that i can draw it again in every tick

        x = self.surface.get_width()
        move_mode = 0  # towards the left
        while True:
            # a fancy transition effect on the x axis!
            if move_mode == 0 and x > self.position[0] - 100:
                x -= 64
            elif x < self.position[0]:
                move_mode = 1  # towards the right
                x += 16
            else:
                x = self.position[0]
                move_mode = 2  # no movement

            if move_mode == 2:  # the transition effect has ended
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # immediately end game
                        maingame.maingame.exit()  # ask the game to exit
                        return False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_y:
                            return True
                        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_n:
                            return False

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if self.rect_ok.collidepoint(event.pos):
                            return True

            self.surface.blit(previous_screen, (0, 0))
            self.surface.blit(self.background, (x, self.position[1]))

            tsoliasgame.draw_text(self.surface, fonts.font_44, title,
                                  [x + self.background.get_width() / 2, self.position[1] + 30],
                                  tsoliasgame.colors.green, tsoliasgame.ALIGN_CENTER, tsoliasgame.ALIGN_CENTER)
            tsoliasgame.draw_text(self.surface, fonts.font_26, text,
                                  [x + self.background.get_width() / 2, self.position[1] + 120],
                                  tsoliasgame.colors.green, tsoliasgame.ALIGN_CENTER, tsoliasgame.ALIGN_CENTER)
            tsoliasgame.draw_text(self.surface, fonts.font_36, "Ok!",
                                  [x + self.background.get_width() / 2, self.position[1] + 228],
                                  tsoliasgame.colors.green, tsoliasgame.ALIGN_CENTER, tsoliasgame.ALIGN_CENTER)

            pygame.display.flip()

            self.clock.tick(maingame.maingame.fps)


question = Question()
message = Message()