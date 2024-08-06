import os

class UserConfig:

    def __init__(self):
        self.databaseDirectory = os.getcwd() + "/database/"
        self.mediaDirectory = os.getcwd() + "/media/"

    def setDatabaseDirectory(self, directory):
        self.databaseDirectory = directory + "/"
    
    def setMediaDirectory(self, directory):
        self.mediaDirectory = directory + "/"