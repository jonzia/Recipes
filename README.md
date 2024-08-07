# Flavortown Recipe Compendium
A simple recipe book applet in Python.

## User Guide

1. On launch, select database folder containing recipe files.
2. To create a new recipe, press `New Reipce` in the main window. This will create a blank recipe which can be edited.
3. To view a recipe, select a recipe in the main window and press `View/Edit`, which will launch the viewer window.
4. To edit a recipe, select a recipe in the main window and press `View/Edit`. Recipes can be edited using the command prompt at the bottom of the viewer window. Available commands are listed in the command library below. Note that edits made outside of the command prompt will not be saved to the recipe.
5. To create a new version of a recipe, press `New Version`, which will create a copy of the currently selected recipe with an incremented version number.
6. To delete a recipe, select the recipe in the main window and press `Delete Recipe`.

## Command Library

| Command | Syntax | Comment |
| -------- | ------- | ------- | 
| Add an ingredient  | `>> ai(ingredient, quantity, unit)` | `ingredient` is string, `quantity` is double, `unit` of type Unit.value |
| Removing an ingredient | `>> ri(index)` | |
| Add an instruction | `ar(index , instruction)` |  `index = 0` to append new instruction, `instruction` of type string |
| Removing an instruction | `>> rr(index)` | |
| Editing an instruction | `>> ri(index, instruction)` | |
| Adding a note | `>> an(note)` | `note` of type string |
| Removing a note | `>> rn(index)` | |
| Editing a note | `>> an(index, note)` | |
| Adding an image file | `>> am()` | File selection prompt will appear |
| Removing an image file | `>> rm()` | File selection prompt will appear |
| List all image files | `>> lm()` | |
| Update a recipe name | `>> name(newName)` | `newName` of type string |
| Update a recipe version | `>> version(newVersion)` | `newVersion` of type int |
| Update a recipe date | `>> date(year, month, day)` | `year`, `month`, `day` of type int |
| Write recipe to file | `>> write()` | User will be prompted to select desstination folder |

*Note that all indices start at 1, not 0, and are of type int.*
