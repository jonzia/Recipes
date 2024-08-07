# Import libraries
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
import os, subprocess, platform
from datetime import datetime
import Recipe as rec
import utils
from Units import Unit as unit
from UserConfig import UserConfig as uc

# METHODS

# Handling new recipe button presses
def openNewRecipe():
    # Ensure that a "New Recipe" does not already exist
    for recipe in recipes:
        if recipe.name == "New Recipe":
            debugger.config(text = "New recipe already exists: " + recipe.getFullName())
            return
    # Otherwise, create new recipe and update list
    newRecipe = rec.Recipe("New Recipe", 1)
    newRecipe.saveRecipe(configuration.databaseDirectory)
    populateList()

# Handling view/edit recipe button selection
def openRecipeViewer():

    # Get selected recipe
    recipeIdx = listbox.curselection()[0]

    # Format window
    newWindow = tk.Toplevel()
    newWindow.geometry("350x735")
    newWindow.title(recipes[recipeIdx].getFullName())

    # Declaring function for opening media
    def openMedia():
        for mediaFile in recipes[recipeIdx].media:
            if platform.system() == 'Darwin':
                subprocess.call(('open', mediaFile))
            elif platform.system() == 'Windows':
                os.startfile(mediaFile)
            else:
                subprocess.call(('xdg-open', mediaFile))

    # Title frame
    newFrame = tk.Frame(master = newWindow)
    newFrame.pack()
    recipeDate = tk.Label(master = newFrame, text = "Date Created: " + recipes[recipeIdx].date.strftime("%x"))
    recipeDate.pack()

    # Ingredients title frame
    newFrame1 = tk.Frame(master = newWindow)
    newFrame1.pack()
    ingredientsTitle = tk.Label(master = newFrame1, text = "Ingredients")
    ingredientsTitle.pack()

    # Ingredients list frame
    newFrame2 = tk.Frame(master = newWindow)
    sb = tk.Scrollbar(master = newFrame2, orient = "vertical")
    sb.pack(side = tk.RIGHT, fill = tk.Y)
    tw = tk.Text(master = newFrame2, yscrollcommand=sb.set, height = 10)
    # Populate ingredients list
    for ingredient in recipes[recipeIdx].ingredients:
        tw.insert(tk.END, "- " + ingredient + ": " + str(recipes[recipeIdx].ingredients[ingredient][0]) + " " + recipes[recipeIdx].ingredients[ingredient][1].value)
        tw.insert(tk.END, "\n")
    sb.config(command = tw.yview)
    tw.pack()
    newFrame2.pack()

    # Recipe title frame
    newFrame3 = tk.Frame(master = newWindow)
    newFrame3.pack()
    recipeTitle = tk.Label(master = newFrame3, text = "Recipe")
    recipeTitle.pack()
    
    # Recipe list frame
    newFrame3 = tk.Frame(master = newWindow)
    sb2 = tk.Scrollbar(master = newFrame3, orient = "vertical")
    sb2.pack(side = tk.RIGHT, fill = tk.Y)
    tw2 = tk.Text(master = newFrame3, yscrollcommand=sb2.set, height = 20)
    # Populate recipe list
    for (instructionIdx, instruction) in enumerate(recipes[recipeIdx].instructions):
        tw2.insert(tk.END, str(instructionIdx+1) + ". " + instruction)
        tw2.insert(tk.END, "\n")
    sb2.config(command = tw2.yview)
    tw2.pack()
    newFrame3.pack()

    # Notes title frame
    newFrame4 = tk.Frame(master = newWindow)
    newFrame4.pack()
    noteTitle = tk.Label(master = newFrame4, text = "Notes")
    noteTitle.pack()
    
    # Notes list frame
    newFrame4 = tk.Frame(master = newWindow)
    sb3 = tk.Scrollbar(master = newFrame4, orient = "vertical")
    sb3.pack(side = tk.RIGHT, fill = tk.Y)
    tw3 = tk.Text(master = newFrame4, yscrollcommand=sb3.set, height = 10)
    # Populate notes
    for note in recipes[recipeIdx].notes:
        tw3.insert(tk.END, "- " + note)
        tw3.insert(tk.END, "\n")
    sb3.config(command = tw3.yview)
    tw3.pack()
    newFrame4.pack()

    # Media selection frame
    newFrame5 = tk.Frame(master = newWindow)
    newFrame5.pack()
    viewMediaButton = tk.Button(master = newFrame5, text = "View Media", command = openMedia)
    viewMediaButton.grid(row = 0, column = 0)

    # Spacer
    newFrame6 = tk.Frame(master = newWindow)
    newFrame6.pack()
    spacer = tk.Label(master = newFrame6, text = "")
    spacer.pack()

    # Command prompt
    commandBox = tk.Text(master = newFrame6, height = 1)
    commandBox.insert(tk.END, ">> ")
    commandBox.pack()
    runCommmandButton = tk.Button(master = newFrame6, text = "Run", command = lambda: runCommand(commandBox.get(1.0, tk.END), recipeIdx))
    runCommmandButton.pack()

    # Handling commaand prompt entries
    def runCommand(fullCommand, idx):

        # Extract command accounting for leading ">> "
        fullCommand = fullCommand[3:]
        temp = fullCommand.split("(")
        command = temp[0]

        # Adding ingredient
        # >> ai(ingredient, quantity, unit)
        if command == "ai":
            # Extract variables
            temp = temp[1].split(",")
            ingredient = temp[0]
            quantity = temp[1]
            temp = temp[2].split(")")
            itemUnit = temp[0]
            # Ensure the unit is valid, else return error
            unitMatch = True if itemUnit in [item.value for item in unit] else False
            if not unitMatch:
                debugger.config(text = "Invalid unit entered: " + itemUnit)
                return
            else:
                # If no error, map unit to enum and add ingredient to recipe
                for item in unit:
                    if itemUnit == item.value:
                        itemUnit = item
                        break
                recipes[idx].addIngredient(ingredient, quantity, itemUnit)
                debugger.config(text = "Saved changes to " + recipes[idx].getFullName())

        # Removing ingredient
        # >> ri(ingredient)
        elif command == "ri":
            # Extract variables
            temp = temp[1].split(")")
            ingredientName = temp[0]
            # Remove ingredient, if not successful return error
            success = recipes[idx].removeIngredient(ingredientName)
            if success:
                debugger.config(text = "Saved changes to " + recipes[idx].getFullName())
            else:
                debugger.config(text = "Invalid ingredient entered: " + ingredientName)
                return
            
        # Adding a recipe instruction
        # >> ar(index, instruction)
        elif command == "ar":
            # Extract variables
            temp = temp[1].split(",")
            index = int(temp[0])-1
            temp = temp[1].split(")")
            instruction = temp[0]
            # If -1 (0 by user), add instruction at end, else add at specified location
            success = recipes[idx].addInstruction(instruction, index)
            if success:
                debugger.config(text = "Saved changes to " + recipes[idx].getFullName())
            else:
                debugger.config(text = "Invalid instruction index entered: " + str(index+1))
                return
            
        # Removing a recipe instruction
        # >> ri(index)
        elif command == "rr":
            # Extract variables
            temp = temp[1].split(")")
            index = int(temp[0])-1
            # Remove instruction, if not successful return error
            success = recipes[idx].removeInstruction(index)
            if success:
                debugger.config(text = "Saved changes to " + recipes[idx].getFullName())
            else:
                debugger.config(text = "Invalid instruction index entered: " + str(index+1))
                return
            
        # Edit a recipe instruction
        # >> er(index, instruction)
        elif command == "er":
            # Extract variables
            temp = temp[1].split(",")
            index = int(temp[0])-1
            temp = temp[1].split(")")
            instruction = temp[0]
            # If not successful, return error
            success = recipes[idx].editInstruction(instruction, index)
            if success:
                debugger.config(text = "Saved changes to " + recipes[idx].getFullName())
            else:
                debugger.config(text = "Invalid instruction index entered: " + str(index+1))
                return
            
        # Add a note
        # >> an(note)
        elif command == "an":
            # Extract variables
            temp = temp[1].split(")")
            newNote = temp[0]
            # If not successful, return error
            success = recipes[idx].addNote(newNote)
            if success:
                debugger.config(text = "Saved changes to " + recipes[idx].getFullName())
            else:
                debugger.config(text = "Unable to add note")
                return
        
        # Remove a note
        # >> rn(index)
        elif command == "rn":
            # Extract variables
            temp = temp[1].split(")")
            index = int(temp[0])-1
            # If not successful, return error
            success = recipes[idx].removeNote(index)
            if success:
                debugger.config(text = "Saved changes to " + recipes[idx].getFullName())
            else:
                debugger.config(text = "Invalid note index entered: " + str(index+1))
                return
        
        # Edit a note
        # >> en(index, note)
        elif command == "en":
            # Extract variables
            temp = temp[1].split(",")
            index = int(temp[0])-1
            temp = temp[1].split(")")
            newNote = temp[0]
            # If not successful, return error
            success = recipes[idx].editNote(newNote, index)
            if success:
                debugger.config(text = "Saved changes to " + recipes[idx].getFullName())
            else:
                debugger.config(text = "Invalid note index entered: " + str(index+1))
                return
        
        # Add an image file
        # >> am()
        elif command == "am":
            # Prompt user to select file
            fileName = askopenfilename()
            # Add selected file
            recipes[idx].addMedia(fileName)
            debugger.config(text = "Added file: " + fileName)

        # Remove an image file
        # >> rm()
        elif command == "rm":
            # Prompt user to select file
            fileName = askopenfilename()
            success = recipes[idx].removeMedia(fileName)
            # If file was not able to be removed, report error
            if success:
                debugger.config(text = "Saved changes to " + recipes[idx].getFullName())
            else:
                debugger.config(text = "Invalid file selected: " + fileName)
                return
            
        # List linked image files
        # >> lm()
        elif command == "lm":
            # List linked media
            # If no linked media, print error, else print each file in a new line
            if len(recipes[idx].media) < 1:
                debugger.config(text = "No linked media files for " + recipes[idx].getFullName())
            else:
                temp = ""
                for file in recipes[idx].media:
                    temp += file + "\n"
                    debugger.config(text = temp)
            
        # Update recipe name
        # >> name(new name)
        elif command == "name":
            # Extract variables
            temp = temp[1].split(")")
            newName = temp[0]
            oldFilename = recipes[idx].getFilename(configuration.databaseDirectory)
            # Ensure no recipee will be overwritten
            for recipe in recipes:
                if newName == recipe.name:
                    debugger.config(text = "Recipe with this name exists: " + newName)
                    return
            # If not, update name
            recipes[idx].changeName(newName)
            debugger.config(text = "Name updated: " + newName)
            # Delete old file as new file will be saved
            if os.path.exists(oldFilename):
                os.remove(oldFilename)
            else:
                debugger.config(text = "Unable to remove old file")

        # Update version number
        # >> version(number)
        elif command == "version":
            # Extract variables
            temp = temp[1].split(")")
            newVersion = int(temp[0])
            oldFilename = recipes[idx].getFilename(configuration.databaseDirectory)
            # Ensure no version will be overwritten
            for recipe in recipes:
                if (recipe.name == recipes[idx].name) and (recipe.version == newVersion):
                    debugger.config(text = "Recipe with this version exists: " + str(newVersion))
                    return
            # If not, update version number
            recipes[idx].changeVersion(newVersion)
            debugger.config(text = "Version updated: " + str(newVersion))
            # Delete old file as new file will be saved
            if os.path.exists(oldFilename):
                os.remove(oldFilename)
            else:
                debugger.config(text = "Unable to remove old file")

        # Update date
        # >> date(year, month, day)
        elif command == "date":
            # Extract variables
            temp = temp[1].split(",")
            year = int(temp[0])
            month = int(temp[1])
            temp = temp[2].split(")")
            day = int(temp[0])
            # If date not updated, report error
            success = recipes[idx].changeDate(year, month, day)
            if success:
                debugger.config(text = "Updated date: " + recipes[idx].date.strftime("%x"))
            else:
                debugger.config(text = "Invalid date")
                return
            
        # Create file from recipe
        # >> write(filename)
        # Prompt user to select directory
        elif command == "write":
            directory = askdirectory()
            directory += "/"
            success = recipes[idx].write(directory)
            # Return success if file exists
            if success:
                debugger.config(text = "Wrote file to: " + directory + recipes[idx].getFullName() + ".txt")
            else:
                debugger.config(text = "Unable to write file")
                return
            
        # Refresh user interface
        commandBox.delete("1.0", tk.END)
        commandBox.insert(tk.INSERT, ">> ")
        recipes[idx].saveRecipe(configuration.databaseDirectory)
        refreshRecipe()

    # Handling recipe refreshing after update
    def refreshRecipe():
        # Ingredients
        tw.delete("1.0", tk.END)
        for ingredient in recipes[recipeIdx].ingredients:
            tw.insert(tk.END, "- " + ingredient + ": " + str(recipes[recipeIdx].ingredients[ingredient][0]) + " " + recipes[recipeIdx].ingredients[ingredient][1].value)
            tw.insert(tk.END, "\n")
        # Instructions
        tw2.delete("1.0", tk.END)
        for (instructionIdx, instruction) in enumerate(recipes[recipeIdx].instructions):
            tw2.insert(tk.END, str(instructionIdx+1) + ". " + instruction)
            tw2.insert(tk.END, "\n")
        # Notes
        tw3.delete("1.0", tk.END)
        for note in recipes[recipeIdx].notes:
            tw3.insert(tk.END, "- " + note)
            tw3.insert(tk.END, "\n")
        # Name
        newWindow.title(recipes[recipeIdx].getFullName())
        # Date
        recipeDate.config(text = "Date Created: " + recipes[recipeIdx].date.strftime("%x"))
        # List
        populateList()

# Create new recipe version
def createNewVersion():
    # Get selected recipe
    recipeIdx = listbox.curselection()[0]
    newRecipe = recipes[recipeIdx].createNewVersion()
    # Ensure that a new version of the recipe does not already exist
    for recipe in recipes:
        if recipe.getFullName() == newRecipe.getFullName():
            debugger.config(text = "Incremented version already exists: " + recipe.getFullName())
            return
    # Save the udpated recipe and update the list
    newRecipe.saveRecipe(configuration.databaseDirectory)
    populateList()

# Update the list of recipes
def populateList():
    # Clear existing list
    listbox.delete(0, tk.END)
    recipes.clear()
    modifier = 0    # Accounting for .DS_store
    for idx, fileName in enumerate(sorted(os.listdir(configuration.databaseDirectory))):
        # Ignore .DS_store if it exists
        if fileName[0] == ".": 
            modifier = 1
            continue
        try:
            # Get recipe name from file name
            recipeName = fileName.split("_")[0]
            versionNumber = fileName.split("_")[1].split(".")[0][1:]
            # Load the recipe
            recipes.append(utils.loadRecipe(recipeName, versionNumber, configuration.databaseDirectory))
            # Add the recipe to the list box
            listbox.insert(idx - modifier, recipes[idx - modifier].getFullName())
        except:
            continue

# Delete the selected recipe
def deleteRecipe():
    recipeIdx = listbox.curselection()[0]
    recipes[recipeIdx].deleteRecipe(configuration.databaseDirectory)
    populateList()

# Set the database directory
def setDatabaseDirectory():
    databaseDirectory = askdirectory()
    configuration.setDatabaseDirectory(databaseDirectory)
    debugger.config(text = "Updated database directory: " + databaseDirectory)
    populateList()

# Initialize the GUI
window = tk.Tk()
window.geometry("350x350")
window.title("Recipe Book")

# Base directory
# baseDirectory = os.path.abspath(os.path.dirname(__file__))
# databaseDirectory = os.path.join(baseDirectory, "database/")
# databaseDirectory = askdirectory()
# databaseDirectory = databaseDirectory + "/"
configuration = uc()

# GUI header
frame1 = tk.Frame(master = window)
frame1.pack()
titleText = tk.Label(master = frame1, text = "The Flavortown Compendium")
titleText.pack()

frame2 = tk.Frame(master = window)
frame2.pack()
selectDatabaseButton = tk.Button(master = frame2, text = "Recipe Directory", command = setDatabaseDirectory)
selectDatabaseButton.pack()

# Recipe list frame
frame3 = tk.Frame(master = window)
frame3.pack()
listbox = tk.Listbox(master = frame3)
recipes = []
populateList()
listbox.pack()

# Button frame
frame4 = tk.Frame(master = window)
frame4.pack()
# Creating a new recipe
newRecipeButton = tk.Button(master = frame4, text = "New Recipe", command = openNewRecipe)
newRecipeButton.grid(row = 0, column = 0)
# Creating a new version
viewRecipeButton = tk.Button(master = frame4, text = "New Version", command = createNewVersion)
viewRecipeButton.grid(row = 0, column = 1)
# Viewing/Editing a recipe
editRecipeButton = tk.Button(master = frame4, text = "View/Edit", command = openRecipeViewer)
editRecipeButton.grid(row = 1, column = 0)
# Deleting a recipe
newVersionButton = tk.Button(master = frame4, text = "Delete Recipe", command = deleteRecipe)
newVersionButton.grid(row = 1, column = 1)

# Debugger frame
frame5 = tk.Frame(master = window)
frame5.pack()
debugger = tk.Message(master = frame5, text = "", width = 300)
debugger.pack()

# Run GUI
window.mainloop()