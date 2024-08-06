import os

class UserConfig:

    def __init__(self):
        self.databaseDirectory = os.getcwd() + "/"
        self.mediaDirectory = os.getcwd() + "/"

    def setDatabaseDirectory(self, directory):
        self.databaseDirectory = directory + "/"
    
    def setMediaDirectory(self, directory):
        self.mediaDirectory = directory + "/"