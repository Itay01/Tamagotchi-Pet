from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox, simpledialog


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class FeedCommand(Command):
    def __init__(self, pet):
        self.pet = pet

    def execute(self):
        food_choice = tk.simpledialog.askstring(
            "Feeding",
            "What would you like to feed your pet?\n1. Meal\n2. Snack"
        )
        if food_choice == '1':
            self.pet.feed('meal')
        elif food_choice == '2':
            self.pet.feed('snack')
        else:
            messagebox.showerror("Error", "Invalid choice.")

class SleepCommand(Command):
    def __init__(self, pet):
        self.pet = pet

    def execute(self):
        self.pet.sleep()

class ExerciseCommand(Command):
    def __init__(self, pet):
        self.pet = pet

    def execute(self):
        self.pet.exercise()

class PlayCommand(Command):
    def __init__(self, pet):
        self.pet = pet

    def execute(self):
        self.pet.play_with()

class CleanCommand(Command):
    def __init__(self, pet):
        self.pet = pet

    def execute(self):
        self.pet.clean()

class SpecialAbilityCommand(Command):
    def __init__(self, pet):
        self.pet = pet

    def execute(self):
        self.pet.activate_special_ability()
