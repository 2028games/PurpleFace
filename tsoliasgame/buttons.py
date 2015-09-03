import pygame


class Button(object):
    def __init__(self, action, image=None, pos=None, rect=None, visible=True, debug=False):
        """a button class for pygame

        :param action: action to be made
        :param image: image to draw - can be None for no drawing
        :param pos: position to draw - can be None if rect is specified
        :param rect: collision rect - can be None if bot image and pos are specified
        :param visible: if image should be drawn
        :param debug: if debug will draw rect boundaries
        """
        self.action = action
        self.image = image
        self.visible = visible
        self.debug = debug

        if pos:
            self.draw_pos = pos
            if rect:
                self.rect = rect
            elif image:
                self.rect = pygame.Rect(pos[0], pos[1], image.get_width(), image.get_height())
        elif rect:
            self.rect = rect
            self.draw_pos = rect.x, rect.y

    def check_action(self, pos):
        """check if button was clicked
        and if it was clicked then do the predefined action and return the check result

        :rtype : bool
        :param pos: click position
        """

        # noinspection PyArgumentList
        if self.rect.collidepoint(pos):
            self.action(pos)
            return True
        else:
            return False

    def draw(self, surface):
        """draw the button on the specified surface

        :param surface: the surface on which the button will be drawn
        """
        if self.image and self.visible:
            surface.blit(self.image, self.draw_pos)
        
        if self.debug:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)


class ButtonGroup(object):
    def __init__(self):
        self.__group = []

    def __len__(self):
        return len(self.__group)

    def __getitem__(self, key):
        return self.__group[key]

    def add(self, *buttons):
        """add buttons
        :param buttons: the buttons to add
        """
        for button in buttons:
            self.__group.append(button)

    def handle_clicks(self, pos):
        """must be called in each event_handling
        checks action for all its buttons and returns if any button was clicked
        :rtype : bool
        :param pos: click position
        """
        for button in self.__group:
            if button.check_action(pos):
                return True
        return False

    def draw(self, surface):
        """draw all its buttons on the specified surface

        :param surface: the surface on which the buttons will be drawn
        """
        for button in self.__group:
            button.draw(surface)