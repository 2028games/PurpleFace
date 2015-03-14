import tsoliasgame


class MultiLevelGroup(tsoliasgame.LevelGroup):
    """a LevelGroup that can switch between multiple different directories"""
    def __init__(self, view, level_changed=None):
        """
        :param level_changed: a function to call when the level is changed
        :param view: the view to be used in the levels
        """
        tsoliasgame.LevelGroup.__init__(self, view, level_changed)
        self.directories = []
        self.__current_dir_index = -1

    def pick_directory(self, directory, check_empty = False):
        """
        chooses the current directory from the list of valid directories and returns True if directory was changed
        :param directory: might be an int specifying the index in the list, or the string of the directory wanted -
        if the string specified isnt already in the list it gets added
        check_empty: if True a change to an empty dir will fail
        """
        if isinstance(directory, int):
            new_dir_index = directory
        elif isinstance(directory, str):
            try:
                new_dir_index = self.directories.index(directory)
            except ValueError:
                # if directory doesnt exist add it now
                self.directories.append(directory)
                new_dir_index = len(self.directories) - 1

        # now make the changes that should be made - if they should be made
        if not new_dir_index == self.__current_dir_index and not(check_empty and tsoliasgame.LevelGroup.check_empty_dir(self.directories[new_dir_index])):
            current_level = self.current()
            if current_level:
                current_level.clear_all()
            self.__current_dir_index = new_dir_index
            self.reset()
            self.from_directory(self.directories[self.__current_dir_index])
            return True
        return False

    def current_directory_index(self):
        return self.__current_dir_index

    def next_directory(self, check_empty = False):
        """picks next directory in the list - it cycles from the last to the first"""
        return self.pick_directory((self.__current_dir_index + 1) % len(self.directories), check_empty)

    def previous_directory(self, check_empty = False):
        """picks previous directory in the list - it cycles from the first to the last"""
        return self.pick_directory((self.__current_dir_index - 1) % len(self.directories), check_empty)