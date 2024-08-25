# WorldExploration
A metroidvania game. The levels are not complete, but the game features: 
- 6 enemies and 2 bosses
- 50 screens
- 4 upgrades

Though the game has some save/load functionality, it has not been properly implemented. I wanted to try to include something with stored sava data like the saving akin to that of Elements For Money, another project of mine, but ended up focusing my time on other projects instead.

Reaching the end of the game crashes it, as you eventually fall into a level that is not in the list of levels. 

## How To Play
### 1. Ensure you have Python 3 and Pygame installed
You can install Python 3 from https://www.python.org/.
To install Pygame, type `pip install pygame` in the terminal of either a virtual environment or your global system.

### 2. Run the script
Run main.py by typing `python main.py` while your terminal is in the directory. 

### 3. Click New Game
Note that loading should be treated as, for all intents and purposes, not functioning. Clicking Load Game will have no way of going back, either, so ideally don't click it. 

You can move using WASD and pause/unpause using Escape. 

Other controls are explained during the game.

## Internals
This game uses two main OOP principles throughout, those being the Template Method through abstract base classes and the Facade design pattern through 'manager' classes.  

### Object hierarchy
The following diagram shows which classes inherit from which: 
![WorldExplorationObjectHierarchy](https://github.com/user-attachments/assets/50007459-5ffd-488b-a49f-b1f331671b4d)
Note that MenuManager is the only non-GameObject class. This is because it is used to handle transitions between menus in which the game doesn't exist yet (e.g., between the main menu to the game) and hence would not function properly as a GameObject.

### Facade hierarchy
The following diagram shows which concrete classes are used in which manager classes:
![WorldExplorationFacadeHierarchy](https://github.com/user-attachments/assets/eb7a70e2-6780-4bf6-aa93-94264e9f7a03)
Note that SavePoint and UpgradePoint are both used in two classes. This is because the WorldManager needs their constructors to make them, whereas the SaveManager and UpgradeManager need them to call their functions. 

Player is not a manager and hence not shown, but it is called in main. Bullet and Explosion are unique in that they are used in a few different places throughout that need to either create new bullets, reset explosion particles, etc. They have been excluded from this diagram for the reason of making it more legible. 

 
