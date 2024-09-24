import tkinter as tk
import pygame

from game.game_manger import GameManager

pygame.init()
pygame.mixer.init()

if __name__ == "__main__":
    root = tk.Tk()
    GameManager(root)
    root.mainloop()
