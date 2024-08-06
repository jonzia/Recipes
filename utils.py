import pickle
import os

# Loading a recipe from a file
def loadRecipe(recipeName, version, directory):
    # baseDirectory = os.getcwd()
    # databaseDirectory = os.path.join(baseDirectory, "database/")
    fileName = directory + recipeName + "_v" + str(version) + ".pkl"
    with open(fileName, 'rb') as file:
        return pickle.load(file)