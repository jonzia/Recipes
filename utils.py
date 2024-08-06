import pickle

# Loading a recipe from a file
def loadRecipe(recipeName, version):
    fileName = "database/" + recipeName + "_v" + str(version) + ".pkl"
    with open(fileName, 'rb') as file:
        return pickle.load(file)