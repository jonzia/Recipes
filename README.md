# Flavortown Recipe Compendium
A simple recipe book applet in Python.

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
| Update a recipe name | `>> name(newName)` | `newName` of type string |
| Update a recipe version | `>> version(newVersion)` | `newVersion` of type int |
| Update a recipe date | `>> date(year, month, day)` | `year`, `month`, `day` of type int |

*Note that all indices start at 1, not 0, and are of type int.*
