# import random
# import time
# import threading
# from abc import ABC, abstractmethod
# import tkinter as tk
# from tkinter import messagebox, simpledialog
#
#
# class Pet(ABC):
#     LIFE_STAGES = ['Baby', 'Child', 'Teenager', 'Adult', 'Senior']
#
#     def __init__(self, name, color, pattern, accessories, update_status_callback):
#         self.name = name
#         self.color = color
#         self.pattern = pattern
#         self.accessories = accessories
#         self.hunger = 50
#         self.happiness = 50
#         self.training = 0
#         self.health = 100
#         self.cleanliness = 100
#         self.age = 0
#         self.weight = 5
#         self.life_stage_index = 0
#         self.life_stage = self.LIFE_STAGES[self.life_stage_index]
#         self.alive = True
#         self.sick = False
#         self.update_status_callback = update_status_callback
#         self.game_over = False
#
#         # Start the time thread
#         self.time_thread = threading.Thread(target=self.time_passes)
#         self.time_thread.daemon = True
#         self.time_thread.start()
#
#     @abstractmethod
#     def characteristic(self):
#         pass
#
#     @abstractmethod
#     def special_ability(self):
#         pass
#
#     @abstractmethod
#     def special_ability_effect(self):
#         pass
#
#     def activate_special_ability(self):
#         if self.alive:
#             self.special_ability_effect()
#             self.update_status_callback()
#         else:
#             messagebox.showinfo("Info", f"{self.name} is not able to perform this action.")
#
#     def time_passes(self):
#         while self.alive:
#             time.sleep(5)  # Time interval can be adjusted
#             self.update_meters()
#             self.update_status_callback()
#             if random.randint(1, 5) == 1:
#                 self.random_event()
#                 self.update_status_callback()
#             if not self.alive:
#                 self.game_over = True
#                 messagebox.showinfo("Game Over", f"Unfortunately, {self.name} has passed away.")
#                 break
#
#     def update_meters(self):
#         self.hunger -= random.randint(5, 10)
#         self.happiness -= random.randint(2, 5)
#         self.cleanliness -= random.randint(5, 10)
#         self.health -= random.randint(0, 2)
#         self.age += 1
#
#         self.hunger = max(0, min(self.hunger, 100))
#         self.happiness = max(0, min(self.happiness, 100))
#         self.health = max(0, min(self.health, 100))
#         self.cleanliness = max(0, min(self.cleanliness, 100))
#
#         if self.age % 5 == 0:
#             self.advance_life_stage()
#
#         self.check_sickness()
#         self.check_alive()
#
#     def check_alive(self):
#         if self.hunger <= 0 or self.health <= 0 or self.cleanliness <= 0:
#             self.alive = False
#
#     def advance_life_stage(self):
#         if self.life_stage_index < len(self.LIFE_STAGES) - 1:
#             self.life_stage_index += 1
#             self.life_stage = self.LIFE_STAGES[self.life_stage_index]
#             messagebox.showinfo("Life Stage", f"{self.name} has grown to the {self.life_stage} stage!")
#             self.special_ability()
#
#     def feed(self, food_type):
#         if food_type == 'meal':
#             self.hunger += 30
#             self.weight += 0.5
#             messagebox.showinfo("Feeding", f"{self.name} enjoyed a hearty meal!")
#         elif food_type == 'snack':
#             self.hunger += 10
#             self.happiness += 5
#             self.weight += 0.2
#             messagebox.showinfo("Feeding", f"{self.name} loved the tasty snack!")
#         self.hunger = min(self.hunger, 100)
#         self.happiness = min(self.happiness, 100)
#
#     def play_with(self):
#         def play_game():
#             number = random.randint(1, 5)
#             try:
#                 guess = int(guess_entry.get())
#                 if guess == number:
#                     messagebox.showinfo("Game", "You guessed it! That was fun!")
#                     self.happiness += 15
#                 else:
#                     messagebox.showinfo("Game", f"Oops! The correct number was {number}. Maybe next time!")
#                     self.happiness += 5
#             except ValueError:
#                 messagebox.showerror("Error", "Please enter a valid number.")
#             self.hunger -= 5
#             self.happiness = min(self.happiness, 100)
#             self.hunger = max(0, self.hunger)
#             game_window.destroy()
#             self.update_status_callback()
#
#         game_window = tk.Toplevel()
#         game_window.title("Guess the Number")
#         tk.Label(game_window, text="Guess a number between 1 and 5").pack()
#         guess_entry = tk.Entry(game_window)
#         guess_entry.pack()
#         tk.Button(game_window, text="Submit", command=play_game).pack()
#
#     def sleep(self):
#         self.health += 20
#         self.hunger -= 10
#         self.cleanliness -= 5
#         self.health = min(self.health, 100)
#         self.hunger = max(0, self.hunger)
#         self.cleanliness = max(0, self.cleanliness)
#         messagebox.showinfo("Sleep", f"{self.name} had a good rest!")
#         self.update_status_callback()
#
#     def exercise(self):
#         self.training += 10
#         self.happiness += 5
#         self.hunger -= 10
#         self.weight -= 0.5
#         self.training = min(self.training, 100)
#         self.happiness = min(self.happiness, 100)
#         self.hunger = max(0, self.hunger)
#         self.weight = max(1, self.weight)
#         messagebox.showinfo("Exercise", f"{self.name} enjoyed the exercise!")
#         self.update_status_callback()
#
#     def clean(self):
#         self.cleanliness = 100
#         self.happiness += 5
#         self.happiness = min(self.happiness, 100)
#         messagebox.showinfo("Clean", f"You cleaned {self.name}!")
#         if self.sick:
#             self.cure_sickness()
#         self.update_status_callback()
#
#     def check_sickness(self):
#         if self.cleanliness < 30 and not self.sick:
#             if random.choice([True, False]):
#                 self.sick = True
#                 messagebox.showwarning("Sickness", f"Oh no! {self.name} has gotten sick due to poor cleanliness!")
#                 self.health -= 20
#                 self.health = max(0, self.health)
#
#     def cure_sickness(self):
#         if self.sick:
#             self.sick = False
#             self.health += 20
#             self.health = min(self.health, 100)
#             messagebox.showinfo("Recovery", f"{self.name} has been cured!")
#
#     def random_event(self):
#         events = [
#             {"event": "found a treasure!", "happiness": 20},
#             {"event": "got scared by a thunderstorm.", "happiness": -15},
#             {"event": "made a new friend!", "happiness": 10},
#             {"event": "ate something bad.", "health": -20},
#         ]
#         event = random.choice(events)
#         messagebox.showinfo("Random Event", f"{self.name} {event['event']}")
#         self.happiness += event.get('happiness', 0)
#         self.health += event.get('health', 0)
#         self.happiness = max(0, min(self.happiness, 100))
#         self.health = max(0, min(self.health, 100))
#
#     def status(self):
#         sick_status = "Yes" if self.sick else "No"
#         status_text = (
#             f"Life Stage: {self.life_stage}\n"
#             f"Hunger: {self.hunger}\n"
#             f"Happiness: {self.happiness}\n"
#             f"Training: {self.training}\n"
#             f"Health: {self.health}\n"
#             f"Cleanliness: {self.cleanliness}\n"
#             f"Age: {self.age} days\n"
#             f"Weight: {self.weight:.2f} kg\n"
#             f"Sick: {sick_status}\n"
#             f"Color: {self.color}\n"
#             f"Pattern: {self.pattern}\n"
#             f"Accessories: {', '.join(self.accessories) if self.accessories else 'None'}\n"
#         )
#         return status_text
#
# class Dog(Pet):
#     def characteristic(self):
#         messagebox.showinfo("Pet Info", f"{self.name} is a loyal and playful dog!")
#
#     def special_ability(self):
#         if self.life_stage == 'Teenager':
#             messagebox.showinfo("Special Ability", f"{self.name} learned to fetch!")
#         elif self.life_stage == 'Adult':
#             messagebox.showinfo("Special Ability", f"{self.name} can now guard the house!")
#         elif self.life_stage == 'Senior':
#             messagebox.showinfo("Special Ability", f"{self.name} enjoys leisurely walks.")
#
#     def special_ability_effect(self):
#         messagebox.showinfo("Special Ability", f"{self.name} fetches a rare item for you!")
#         self.happiness += 20
#         self.happiness = min(self.happiness, 100)
#
# class Cat(Pet):
#     def characteristic(self):
#         messagebox.showinfo("Pet Info", f"{self.name} is an independent and curious cat!")
#
#     def special_ability(self):
#         if self.life_stage == 'Teenager':
#             messagebox.showinfo("Special Ability", f"{self.name} learned to climb trees!")
#         elif self.life_stage == 'Adult':
#             messagebox.showinfo("Special Ability", f"{self.name} loves to nap in the sun!")
#         elif self.life_stage == 'Senior':
#             messagebox.showinfo("Special Ability", f"{self.name} appreciates quiet companionship.")
#
#     def special_ability_effect(self):
#         messagebox.showinfo("Special Ability", f"{self.name} catches a pesky mouse!")
#         self.hunger += 15
#         self.hunger = min(self.hunger, 100)
#
# class Dragon(Pet):
#     def characteristic(self):
#         messagebox.showinfo("Pet Info", f"{self.name} is a fierce and majestic dragon!")
#
#     def special_ability(self):
#         if self.life_stage == 'Teenager':
#             messagebox.showinfo("Special Ability", f"{self.name} can breathe small flames!")
#         elif self.life_stage == 'Adult':
#             messagebox.showinfo("Special Ability", f"{self.name} can fly high in the sky!")
#         elif self.life_stage == 'Senior':
#             messagebox.showinfo("Special Ability", f"{self.name} is a wise and ancient creature.")
#
#     def special_ability_effect(self):
#         messagebox.showinfo("Special Ability", f"{self.name} breathes fire to scare away threats!")
#         self.health += 25
#         self.health = min(self.health, 100)
#
# class Unicorn(Pet):
#     def characteristic(self):
#         messagebox.showinfo("Pet Info", f"{self.name} is a magical and graceful unicorn!")
#
#     def special_ability(self):
#         if self.life_stage == 'Teenager':
#             messagebox.showinfo("Special Ability", f"{self.name} can grant small wishes!")
#         elif self.life_stage == 'Adult':
#             messagebox.showinfo("Special Ability", f"{self.name} purifies water sources!")
#         elif self.life_stage == 'Senior':
#             messagebox.showinfo("Special Ability", f"{self.name} shares ancient wisdom.")
#
#     def special_ability_effect(self):
#         messagebox.showinfo("Special Ability", f"{self.name} uses magic to heal you!")
#         self.health += 30
#         self.health = min(self.health, 100)
#
# class GameManager:
#     def __init__(self, root):
#         self.root = root
#         self.pet = None
#         self.setup_ui()
#
#     def setup_ui(self):
#         self.root.title("Tamagotchi Game")
#
#         # Pet Selection Frame
#         self.selection_frame = tk.Frame(self.root)
#         tk.Label(self.selection_frame, text="Choose your pet type:").pack()
#
#         tk.Button(self.selection_frame, text="Dog", command=lambda: self.choose_pet('1')).pack()
#         tk.Button(self.selection_frame, text="Cat", command=lambda: self.choose_pet('2')).pack()
#         tk.Button(self.selection_frame, text="Dragon", command=lambda: self.choose_pet('3')).pack()
#         tk.Button(self.selection_frame, text="Unicorn", command=lambda: self.choose_pet('4')).pack()
#
#         self.selection_frame.pack()
#
#         # Main Game Frame
#         self.game_frame = tk.Frame(self.root)
#
#         # Pet Status
#         self.status_label = tk.Label(self.game_frame, text="", justify=tk.LEFT)
#         self.status_label.pack()
#
#         # Action Buttons
#         self.button_frame = tk.Frame(self.game_frame)
#         tk.Button(self.button_frame, text="Eat", command=self.feed_pet).grid(row=0, column=0)
#         tk.Button(self.button_frame, text="Sleep", command=self.pet_sleep).grid(row=0, column=1)
#         tk.Button(self.button_frame, text="Exercise", command=self.pet_exercise).grid(row=0, column=2)
#         tk.Button(self.button_frame, text="Play", command=self.pet_play).grid(row=0, column=3)
#         tk.Button(self.button_frame, text="Clean", command=self.pet_clean).grid(row=0, column=4)
#         tk.Button(self.button_frame, text="Special Ability", command=self.use_special_ability).grid(row=0, column=5)
#         tk.Button(self.button_frame, text="Quit", command=self.root.quit).grid(row=0, column=6)
#         self.button_frame.pack()
#
#     def choose_pet(self, choice):
#         name = tk.simpledialog.askstring("Pet Name", "Enter your pet's name:")
#         if not name:
#             name = "Pet"
#
#         # Customization options
#         color = tk.simpledialog.askstring("Pet Customization", "Choose a color for your pet:")
#         pattern = tk.simpledialog.askstring("Pet Customization", "Choose a pattern for your pet:")
#         accessories = tk.simpledialog.askstring("Pet Customization", "List accessories for your pet (comma-separated):")
#         accessories_list = [acc.strip() for acc in accessories.split(',')] if accessories else []
#
#         pet_args = (name, color, pattern, accessories_list, self.update_status)
#
#         if choice == '1':
#             self.pet = Dog(*pet_args)
#         elif choice == '2':
#             self.pet = Cat(*pet_args)
#         elif choice == '3':
#             self.pet = Dragon(*pet_args)
#         elif choice == '4':
#             self.pet = Unicorn(*pet_args)
#         else:
#             self.pet = Dog(*pet_args)
#
#         self.pet.characteristic()
#         self.selection_frame.pack_forget()
#         self.game_frame.pack()
#         self.update_status()
#
#     def update_status(self):
#         if self.pet:
#             status = self.pet.status()
#             self.status_label.config(text=f"{self.pet.name}'s Status:\n{status}")
#
#     def feed_pet(self):
#         if self.pet and self.pet.alive:
#             food_choice = tk.simpledialog.askstring("Feeding",
#                                                     "What would you like to feed your pet?\n1. Meal\n2. Snack")
#             if food_choice == '1':
#                 self.pet.feed('meal')
#             elif food_choice == '2':
#                 self.pet.feed('snack')
#             else:
#                 messagebox.showerror("Error", "Invalid choice.")
#             self.update_status()
#
#     def pet_sleep(self):
#         if self.pet and self.pet.alive:
#             self.pet.sleep()
#
#     def pet_exercise(self):
#         if self.pet and self.pet.alive:
#             self.pet.exercise()
#
#     def pet_play(self):
#         if self.pet and self.pet.alive:
#             self.pet.play_with()
#
#     def pet_clean(self):
#         if self.pet and self.pet.alive:
#             self.pet.clean()
#
#     def use_special_ability(self):
#         if self.pet and self.pet.alive:
#             self.pet.activate_special_ability()
#
# if __name__ == '__main__':
#     root = tk.Tk()
#     game = GameManager(root)
#     root.mainloop()





import random
import time
import threading
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

class Pet(ABC):
    LIFE_STAGES = ['Baby', 'Child', 'Teenager', 'Adult', 'Senior']

    def __init__(self, name, color, pattern, accessories, update_status_callback):
        self.name = name
        self.color = color
        self.pattern = pattern
        self.accessories = accessories
        self.hunger = 50
        self.happiness = 50
        self.training = 0
        self.health = 100
        self.cleanliness = 100
        self.age = 0
        self.weight = 5
        self.life_stage_index = 0
        self.life_stage = self.LIFE_STAGES[self.life_stage_index]
        self.alive = True
        self.sick = False
        self.update_status_callback = update_status_callback
        self.game_over = False

        # Start the time thread
        self.time_thread = threading.Thread(target=self.time_passes)
        self.time_thread.daemon = True
        self.time_thread.start()

    @abstractmethod
    def characteristic(self):
        pass

    @abstractmethod
    def special_ability(self):
        pass

    @abstractmethod
    def special_ability_effect(self):
        pass

    def activate_special_ability(self):
        if self.alive:
            self.special_ability_effect()
            self.update_status_callback()
        else:
            messagebox.showinfo("Info", f"{self.name} is not able to perform this action.")

    def time_passes(self):
        while self.alive:
            time.sleep(5)  # Time interval can be adjusted
            self.update_meters()
            self.update_status_callback()
            if random.randint(1, 5) == 1:
                self.random_event()
                self.update_status_callback()
            if not self.alive:
                self.game_over = True
                messagebox.showinfo("Game Over", f"Unfortunately, {self.name} has passed away.")
                break

    def update_meters(self):
        self.hunger -= random.randint(5, 10)
        self.happiness -= random.randint(2, 5)
        self.cleanliness -= random.randint(5, 10)
        self.health -= random.randint(0, 2)
        self.age += 1

        self.hunger = max(0, min(self.hunger, 100))
        self.happiness = max(0, min(self.happiness, 100))
        self.health = max(0, min(self.health, 100))
        self.cleanliness = max(0, min(self.cleanliness, 100))

        if self.age % 5 == 0:
            self.advance_life_stage()

        self.check_sickness()
        self.check_alive()

    def check_alive(self):
        if self.hunger <= 0 or self.health <= 0 or self.cleanliness <= 0:
            self.alive = False

    def advance_life_stage(self):
        if self.life_stage_index < len(self.LIFE_STAGES) - 1:
            self.life_stage_index += 1
            self.life_stage = self.LIFE_STAGES[self.life_stage_index]
            messagebox.showinfo("Life Stage", f"{self.name} has grown to the {self.life_stage} stage!")
            self.special_ability()

    def feed(self, food_type):
        if food_type == 'meal':
            self.hunger += 30
            self.weight += 0.5
            messagebox.showinfo("Feeding", f"{self.name} enjoyed a hearty meal!")
        elif food_type == 'snack':
            self.hunger += 10
            self.happiness += 5
            self.weight += 0.2
            messagebox.showinfo("Feeding", f"{self.name} loved the tasty snack!")
        self.hunger = min(self.hunger, 100)
        self.happiness = min(self.happiness, 100)

    def play_with(self):
        def play_game():
            number = random.randint(1, 5)
            try:
                guess = int(guess_entry.get())
                if guess == number:
                    messagebox.showinfo("Game", "You guessed it! That was fun!")
                    self.happiness += 15
                else:
                    messagebox.showinfo("Game", f"Oops! The correct number was {number}. Maybe next time!")
                    self.happiness += 5
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")
            self.hunger -= 5
            self.happiness = min(self.happiness, 100)
            self.hunger = max(0, self.hunger)
            game_window.destroy()
            self.update_status_callback()

        game_window = tk.Toplevel()
        game_window.title("Guess the Number")
        tk.Label(game_window, text="Guess a number between 1 and 5").pack()
        guess_entry = tk.Entry(game_window)
        guess_entry.pack()
        tk.Button(game_window, text="Submit", command=play_game).pack()

    def sleep(self):
        self.health += 20
        self.hunger -= 10
        self.cleanliness -= 5
        self.health = min(self.health, 100)
        self.hunger = max(0, self.hunger)
        self.cleanliness = max(0, self.cleanliness)
        messagebox.showinfo("Sleep", f"{self.name} had a good rest!")
        self.update_status_callback()

    def exercise(self):
        self.training += 10
        self.happiness += 5
        self.hunger -= 10
        self.weight -= 0.5
        self.training = min(self.training, 100)
        self.happiness = min(self.happiness, 100)
        self.hunger = max(0, self.hunger)
        self.weight = max(1, self.weight)
        messagebox.showinfo("Exercise", f"{self.name} enjoyed the exercise!")
        self.update_status_callback()

    def clean(self):
        self.cleanliness = 100
        self.happiness += 5
        self.happiness = min(self.happiness, 100)
        messagebox.showinfo("Clean", f"You cleaned {self.name}!")
        if self.sick:
            self.cure_sickness()
        self.update_status_callback()

    def check_sickness(self):
        if self.cleanliness < 30 and not self.sick:
            if random.choice([True, False]):
                self.sick = True
                messagebox.showwarning("Sickness", f"Oh no! {self.name} has gotten sick due to poor cleanliness!")
                self.health -= 20
                self.health = max(0, self.health)

    def cure_sickness(self):
        if self.sick:
            self.sick = False
            self.health += 20
            self.health = min(self.health, 100)
            messagebox.showinfo("Recovery", f"{self.name} has been cured!")

    def random_event(self):
        events = [
            {"event": "found a treasure!", "happiness": 20},
            {"event": "got scared by a thunderstorm.", "happiness": -15},
            {"event": "made a new friend!", "happiness": 10},
            {"event": "ate something bad.", "health": -20},
        ]
        event = random.choice(events)
        messagebox.showinfo("Random Event", f"{self.name} {event['event']}")
        self.happiness += event.get('happiness', 0)
        self.health += event.get('health', 0)
        self.happiness = max(0, min(self.happiness, 100))
        self.health = max(0, min(self.health, 100))

    def status(self):
        sick_status = "Yes" if self.sick else "No"
        status_text = (
            f"Life Stage: {self.life_stage}\n"
            f"Hunger: {self.hunger}\n"
            f"Happiness: {self.happiness}\n"
            f"Training: {self.training}\n"
            f"Health: {self.health}\n"
            f"Cleanliness: {self.cleanliness}\n"
            f"Age: {self.age} days\n"
            f"Weight: {self.weight:.2f} kg\n"
            f"Sick: {sick_status}\n"
            f"Color: {self.color}\n"
            f"Pattern: {self.pattern}\n"
            f"Accessories: {', '.join(self.accessories) if self.accessories else 'None'}\n"
        )
        return status_text

class Dog(Pet):
    def characteristic(self):
        messagebox.showinfo("Pet Info", f"{self.name} is a loyal and playful dog!")

    def special_ability(self):
        if self.life_stage == 'Teenager':
            messagebox.showinfo("Special Ability", f"{self.name} learned to fetch!")
        elif self.life_stage == 'Adult':
            messagebox.showinfo("Special Ability", f"{self.name} can now guard the house!")
        elif self.life_stage == 'Senior':
            messagebox.showinfo("Special Ability", f"{self.name} enjoys leisurely walks.")

    def special_ability_effect(self):
        messagebox.showinfo("Special Ability", f"{self.name} fetches a rare item for you!")
        self.happiness += 20
        self.happiness = min(self.happiness, 100)

class Cat(Pet):
    def characteristic(self):
        messagebox.showinfo("Pet Info", f"{self.name} is an independent and curious cat!")

    def special_ability(self):
        if self.life_stage == 'Teenager':
            messagebox.showinfo("Special Ability", f"{self.name} learned to climb trees!")
        elif self.life_stage == 'Adult':
            messagebox.showinfo("Special Ability", f"{self.name} loves to nap in the sun!")
        elif self.life_stage == 'Senior':
            messagebox.showinfo("Special Ability", f"{self.name} appreciates quiet companionship.")

    def special_ability_effect(self):
        messagebox.showinfo("Special Ability", f"{self.name} catches a pesky mouse!")
        self.hunger += 15
        self.hunger = min(self.hunger, 100)

class Dragon(Pet):
    def characteristic(self):
        messagebox.showinfo("Pet Info", f"{self.name} is a fierce and majestic dragon!")

    def special_ability(self):
        if self.life_stage == 'Teenager':
            messagebox.showinfo("Special Ability", f"{self.name} can breathe small flames!")
        elif self.life_stage == 'Adult':
            messagebox.showinfo("Special Ability", f"{self.name} can fly high in the sky!")
        elif self.life_stage == 'Senior':
            messagebox.showinfo("Special Ability", f"{self.name} is a wise and ancient creature.")

    def special_ability_effect(self):
        messagebox.showinfo("Special Ability", f"{self.name} breathes fire to scare away threats!")
        self.health += 25
        self.health = min(self.health, 100)

class Unicorn(Pet):
    def characteristic(self):
        messagebox.showinfo("Pet Info", f"{self.name} is a magical and graceful unicorn!")

    def special_ability(self):
        if self.life_stage == 'Teenager':
            messagebox.showinfo("Special Ability", f"{self.name} can grant small wishes!")
        elif self.life_stage == 'Adult':
            messagebox.showinfo("Special Ability", f"{self.name} purifies water sources!")
        elif self.life_stage == 'Senior':
            messagebox.showinfo("Special Ability", f"{self.name} shares ancient wisdom.")

    def special_ability_effect(self):
        messagebox.showinfo("Special Ability", f"{self.name} uses magic to heal you!")
        self.health += 30
        self.health = min(self.health, 100)

class GameManager:
    def __init__(self, root):
        self.root = root
        self.pet = None
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Tamagotchi Game")

        # Pet Selection Frame
        self.selection_frame = tk.Frame(self.root)
        tk.Label(self.selection_frame, text="Choose your pet type:").pack()

        tk.Button(self.selection_frame, text="Dog", command=lambda: self.choose_pet('1')).pack()
        tk.Button(self.selection_frame, text="Cat", command=lambda: self.choose_pet('2')).pack()
        tk.Button(self.selection_frame, text="Dragon", command=lambda: self.choose_pet('3')).pack()
        tk.Button(self.selection_frame, text="Unicorn", command=lambda: self.choose_pet('4')).pack()

        self.selection_frame.pack()

        # Main Game Frame
        self.game_frame = tk.Frame(self.root)

        # Pet Status
        self.status_label = tk.Label(self.game_frame, text="", justify=tk.LEFT)
        self.status_label.pack()

        # Action Buttons
        self.button_frame = tk.Frame(self.game_frame)
        tk.Button(self.button_frame, text="Eat", command=self.execute_command(FeedCommand)).grid(row=0, column=0)
        tk.Button(self.button_frame, text="Sleep", command=self.execute_command(SleepCommand)).grid(row=0, column=1)
        tk.Button(self.button_frame, text="Exercise", command=self.execute_command(ExerciseCommand)).grid(row=0, column=2)
        tk.Button(self.button_frame, text="Play", command=self.execute_command(PlayCommand)).grid(row=0, column=3)
        tk.Button(self.button_frame, text="Clean", command=self.execute_command(CleanCommand)).grid(row=0, column=4)
        tk.Button(self.button_frame, text="Special Ability", command=self.execute_command(SpecialAbilityCommand)).grid(row=0, column=5)
        tk.Button(self.button_frame, text="Quit", command=self.root.quit).grid(row=0, column=6)
        self.button_frame.pack()

    def execute_command(self, command_class):
        def command_function():
            if self.pet and self.pet.alive:
                command = command_class(self.pet)
                command.execute()
                self.update_status()
        return command_function

    def choose_pet(self, choice):
        name = tk.simpledialog.askstring("Pet Name", "Enter your pet's name:")
        if not name:
            name = "Pet"

        # Customization options
        color = tk.simpledialog.askstring("Pet Customization", "Choose a color for your pet:")
        pattern = tk.simpledialog.askstring("Pet Customization", "Choose a pattern for your pet:")
        accessories = tk.simpledialog.askstring("Pet Customization", "List accessories for your pet (comma-separated):")
        accessories_list = [acc.strip() for acc in accessories.split(',')] if accessories else []

        pet_args = (name, color, pattern, accessories_list, self.update_status)

        if choice == '1':
            self.pet = Dog(*pet_args)
        elif choice == '2':
            self.pet = Cat(*pet_args)
        elif choice == '3':
            self.pet = Dragon(*pet_args)
        elif choice == '4':
            self.pet = Unicorn(*pet_args)
        else:
            self.pet = Dog(*pet_args)

        self.pet.characteristic()
        self.selection_frame.pack_forget()
        self.game_frame.pack()
        self.update_status()

    def update_status(self):
        if self.pet:
            status = self.pet.status()
            self.status_label.config(text=f"{self.pet.name}'s Status:\n{status}")

if __name__ == '__main__':
    root = tk.Tk()
    game = GameManager(root)
    root.mainloop()
