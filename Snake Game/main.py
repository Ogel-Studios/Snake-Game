#Create the Tkinter window.
#Initialize the game manager.
#Keep the window running until the player closes it.

import tkinter as tk
import settings
from game_manager import GameManager

window = tk.Tk()   #Creates the window

window.title(settings.WINDOW_TITLE)

window.geometry(f'{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}')

game = GameManager(window)

window.mainloop()