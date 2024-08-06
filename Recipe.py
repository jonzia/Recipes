import pickle
from copy import deepcopy
from datetime import datetime
import os

class Recipe:

    def __init__(self, name, version, year = None, month = None, day = None):
        self.name = name
        self.version = version
        self.date = datetime.now() if year == None else datetime(year, month, day)
        self.ingredients = {}
        self.instructions = []
        self.notes = []
        self.media = []

    def changeName(self, name):
        self.name = name
    
    def changeVersion(self, version):
        self.version = version

    def changeDate(self, year, month, day):
        try:
            self.date = datetime(year, month, day)
            return True
        except:
            return False

    def addIngredient(self, ingredient, quantity, unit):
        self.ingredients[ingredient] = [quantity, unit]

    def removeIngredient(self, ingredient):
        try:
            del self.ingredients[ingredient]
            return True
        except:
            return False
    
    def addInstruction(self, instruction, atIndex = -1):
        if atIndex == -1:
            self.instructions.append(instruction)
            return True
        else:
            try:
                self.instructions.insert(atIndex, instruction)
                return True
            except:
                return False
            
    def removeInstruction(self, atIndex):
        try:
            del self.instructions[atIndex]
            return True
        except:
            return False
        
    def editInstruction(self, instruction, atIndex):
        try:
            self.instructions[atIndex] = instruction
            return True
        except:
            return False
    
    def addNote(self, note):
        try:
            self.notes.append(note)
            return True
        except:
            return False
        
    def removeNote(self, atIndex):
        try:
            del self.notes[atIndex]
            return True
        except:
            return False
        
    def editNote(self, note, atIndex):
        try:
            self.notes[atIndex] = note
            return True
        except:
            return False
    
    def addMedia(self, imagePath):
        self.media.append(imagePath)

    def removeMedia(self, imagePath):
        for (idx, item) in enumerate(self.media):
            if imagePath == item:
                del self.media[idx]
                return True
        return False

    def getFullName(self):
        return self.name + " (v" + str(self.version) + ")"

    def createNewVersion(self):
        newVersion = deepcopy(self)
        newVersion.version += 1
        return newVersion

    def saveRecipe(self):
        fileName = self.getFilename()
        with open(fileName, 'wb') as file:
            pickle.dump(self, file)

    def deleteRecipe(self):
        fileName = self.getFilename()
        if os.path.exists(fileName):
            os.remove(fileName)
            return True
        else:
            return False
        
    def getFilename(self, directory):
        # baseDirectory = os.getcwd()
        # databaseDirectory = os.path.join(baseDirectory, "database/")
        return directory + self.name + "_v" + str(self.version) + ".pkl"

    def clear(self):
        self.name = "None"
        self.version = 0
        self.date = datetime.now()
        self.ingredients = {}
        self.instructions = []
        self.notes = []
        self.media = []