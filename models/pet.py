import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import messagebox
import threading
import random
import time
from helpers.sound import *


class Pet(ABC):
    LIFE_STAGES = ['Baby', 'Child', 'Teenager', 'Adult', 'Senior']

    def __init__(self, name, color, pattern, accessories, update_status_callback, game_over_callback, pet_type):
        self.name = name
        self.pet_type = pet_type
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
        self.game_over_callback = game_over_callback
        self.game_over = False

    def start_time_thread(self):
        self.time_thread = threading.Thread(target=self.time_passes)
        self.time_thread.daemon = True
        self.time_thread.start()

    def get_mood(self):
        if self.happiness >= 70:
            return 'happy'
        elif self.happiness <= 30:
            return 'sad'
        else:
            return 'neutral'

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove unpicklable entries.
        if 'update_status_callback' in state:
            del state['update_status_callback']
        if 'game_over_callback' in state:
            del state['game_over_callback']
        if 'time_thread' in state:
            del state['time_thread']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Set default values for unpicklable attributes.
        self.update_status_callback = None
        self.game_over_callback = None
        self.time_thread = None

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
            time.sleep(15)
            self.update_meters()
            self.update_status_callback()
            if random.randint(1, 5) == 1:
                self.random_event()
                self.update_status_callback()
            if not self.alive:
                self.game_over = True
                self.game_over_callback()
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
        self.update_status_callback()


        # Play eating sound
        play_sound_effect(f'sounds/{self.pet_type}_eat.mp3')

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

            # Play play sound
            play_sound_effect(f'sounds/{self.pet_type}_play.mp3')

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

        # Play sleep sound
        play_sound_effect('sounds/sleep_sound.mp3')

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
            f"Accessories: {', '.join(self.accessories.split(',')) if self.accessories else 'None'}\n"
        )
        return status_text
