import os
import ast


class Settings(object):
    def __init__(self):
        self.__items = {}
        
    def set(self, name, value):
        self.__items[name] = value
        
    def get(self, name):
        return self.__items[name]
    
    def save(self, location):
        """
        Saves all items of the instance to the specified path
        \n :param location: the path to save to
        """

        text_file = open(location, "w")
        for key, value in self.__items.iteritems():
            if isinstance(value, str):
                value = "'{}'".format(value)  # adds '' to a string to make it recognisable
            text_file.write("{} = {} \n".format(key, value))
            
        text_file.close()
        
    def load(self, location):
        """
        Loads a save file from the specified path
        \n :rtype : int
        \n :param location: the path of the file to load
        \n :return:
        \n 0 if everything ok
        \n 1 if file doesnt exist
        \n 2 if file format not recognizable
        """

        if not os.path.exists(location):
            return 1
       
        text_file = open(location, "r")
        for line in text_file.readlines():
            text = line.strip()
            if not text[0] == "#":
                arr = text.split("=")
                if not len(arr) == 2:
                    text_file.close()
                    return 2
                name = arr[0].strip()
                value = ast.literal_eval(arr[1].strip())
                self.set(name, value)
                
        text_file.close()
        return 0