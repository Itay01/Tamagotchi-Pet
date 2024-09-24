import random
import time
import threading
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
import os
import pickle
import pygame
import datetime


pygame.init()
pygame.mixer.init()


def play_background_music(mood='neutral'):
    pygame.mixer.music.stop()
    if mood == 'happy':
        music_file = 'sounds/happy_music.mp3'
    elif mood == 'sad':
        music_file = 'sounds/sad_music.mp3'
    else:
        current_hour = datetime.datetime.now().hour
        if 6 <= current_hour < 18:
            music_file = 'sounds/day_music.mp3'
        else:
            music_file = 'sounds/night_music.mp3'
    try:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)  # Loop indefinitely
    except Exception as e:
        print(f"Error playing background music: {e}")

def play_sound_effect(sound_file):
    try:
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
    except Exception as e:
        print(f"Error playing sound effect: {e}")


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

    def __init__(self, name, color, pattern, accessories, update_status_callback, game_over_callback):
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
        self.game_over_callback = game_over_callback
        self.game_over = False

    def start_time_thread(self):
        self.time_thread = threading.Thread(target=self.time_passes)
        self.time_thread.daemon = True
        self.time_thread.start()

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

class Dog(Pet):
    def __init__(self, name, color, pattern, accessories, update_status_callback, game_over_callback):
        super().__init__(name, color, pattern, accessories, update_status_callback, game_over_callback)
        # Unique attribute
        self.favorite_toy = "Ball"

    def characteristic(self):
        messagebox.showinfo("Pet Info", f"{self.name} is a loyal and playful dog!")
        # Play dog sound
        play_sound_effect('sounds/dog_bark.mp3')

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

    # Unique method
    def fetch_favorite_toy(self):
        messagebox.showinfo("Fetch", f"{self.name} excitedly fetches the {self.favorite_toy}!")
        self.happiness += 10
        self.happiness = min(self.happiness, 100)
        self.update_status_callback()

class Cat(Pet):
    def __init__(self, name, color, pattern, accessories, update_status_callback, game_over_callback):
        super().__init__(name, color, pattern, accessories, update_status_callback, game_over_callback)
        # Unique attribute
        self.claw_sharpness = 50  # Scale from 0 to 100

    def characteristic(self):
        messagebox.showinfo("Pet Info", f"{self.name} is an independent and curious cat!")
        # Play cat sound
        play_sound_effect('sounds/cat_meow.mp3')

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

    # Unique method
    def sharpen_claws(self):
        messagebox.showinfo("Sharpen Claws", f"{self.name} sharpens its claws.")
        self.claw_sharpness += 20
        self.claw_sharpness = min(self.claw_sharpness, 100)
        self.update_status_callback()

class GameManager:
    def __init__(self, root):
        self.root = root
        self.pet = None
        self.center_window(320, 500)
        play_background_music()

        if os.path.exists('saved_game.pkl'):
            with open('saved_game.pkl', 'rb') as f:
                self.pet = pickle.load(f)
            # Set the callbacks
            self.pet.update_status_callback = self.update_status
            self.pet.game_over_callback = self.on_pet_death
            self.pet.start_time_thread()
            if self.pet.alive:
                self.start_game()
                self.update_status()
            else:
                os.remove('saved_game.pkl')
                self.setup_ui()
        else:
            self.setup_ui()

    def center_window(self, width, height):
        """Centers the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate x and y coordinates to center the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.title("Tamagotchi Game")

    def setup_ui(self):
        self.root.geometry("400x650")
        self.root.title("Tamagotchi Game - Pet Selection")

        # Pet Selection Frame
        self.selection_frame = tk.Frame(self.root)
        self.selection_frame.pack(pady=20, padx=20)

        # Title Label
        self.title_label = tk.Label(self.selection_frame, text="Welcome to Tamagotchi!",
                                    font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        # Instructions Label
        self.instruction_label = tk.Label(self.selection_frame, text="Create your pet to start the journey",
                                          font=("Helvetica", 12))
        self.instruction_label.pack(pady=5)

        # Pet Name Entry
        self.name_label = tk.Label(self.selection_frame, text="Enter your pet's name:",
                                   font=("Helvetica", 12))
        self.name_label.pack(pady=5)

        self.name_entry = tk.Entry(self.selection_frame, font=("Helvetica", 12), width=20)
        self.name_entry.pack(pady=5)

        # Pet Color Entry
        self.color_label = tk.Label(self.selection_frame, text="Choose a color for your pet:",
                                    font=("Helvetica", 12))
        self.color_label.pack(pady=5)

        self.color_entry = tk.Entry(self.selection_frame, font=("Helvetica", 12), width=20)
        self.color_entry.pack(pady=5)

        # Pet Pattern Entry
        self.pattern_label = tk.Label(self.selection_frame, text="Choose a pattern for your pet:",
                                      font=("Helvetica", 12))
        self.pattern_label.pack(pady=5)

        self.pattern_entry = tk.Entry(self.selection_frame, font=("Helvetica", 12), width=20)
        self.pattern_entry.pack(pady=5)

        # Pet Accessories Entry
        self.accessories_label = tk.Label(self.selection_frame, text="List accessories for your pet (comma-separated):",
                                          font=("Helvetica", 12))
        self.accessories_label.pack(pady=5)

        self.accessories_entry = tk.Entry(self.selection_frame, font=("Helvetica", 12), width=20)
        self.accessories_entry.pack(pady=5)

        # Pet Type Selection
        self.pet_type_label = tk.Label(self.selection_frame, text="Choose your pet type:",
                                       font=("Helvetica", 12))
        self.pet_type_label.pack(pady=10)

        self.pet_type_var = tk.StringVar(value="dog")

        # Adding images/icons for pet types
        dog_image = Image.open("dog.jpeg").resize((50, 50))  # Replace with actual path to the image
        dog_photo = ImageTk.PhotoImage(dog_image)
        cat_image = Image.open("cat.jpeg").resize((50, 50))  # Replace with actual path to the image
        cat_photo = ImageTk.PhotoImage(cat_image)

        self.dog_radio = tk.Radiobutton(self.selection_frame, text="Dog", variable=self.pet_type_var, value="dog",
                                        font=("Helvetica", 12), image=dog_photo, compound="left")
        self.dog_radio.image = dog_photo  # Keep a reference to the image to avoid garbage collection
        self.dog_radio.pack(pady=5)

        self.cat_radio = tk.Radiobutton(self.selection_frame, text="Cat", variable=self.pet_type_var, value="cat",
                                        font=("Helvetica", 12), image=cat_photo, compound="left")
        self.cat_radio.image = cat_photo  # Keep a reference to the image to avoid garbage collection
        self.cat_radio.pack(pady=5)

        # Start Button
        self.start_button = tk.Button(self.selection_frame, text="Start", font=("Helvetica", 14, "bold"),
                                      bg="#4CAF50", fg="white", width=15, command=self.start_game)
        self.start_button.pack(pady=20)

    def start_game(self):
        pet_name = self.name_entry.get()
        pattern = self.pattern_entry.get()
        accessories = self.accessories_entry.get()
        color = self.color_entry.get()
        pet_type = self.pet_type_var.get()

        if not pet_name:
            messagebox.showwarning("Input Error", "Please enter a name for your pet.")
            return

        if pet_type == "dog":
            self.pet = Dog(pet_name, color, pattern, accessories, self.update_status, self.on_pet_death)
        elif pet_type == "cat":
            self.pet = Cat(pet_name, color, pattern, accessories, self.update_status, self.on_pet_death)

        self.pet.characteristic()
        self.selection_frame.pack_forget()
        self.setup_game_ui()
        self.update_status()
        self.pet.start_time_thread()

    def setup_game_ui(self):
        # Status Frame
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(pady=10)

        # Status label for displaying overall status text
        self.status_label = tk.Label(self.status_frame, text="", font=("Arial", 12), justify="left", anchor="w")
        self.status_label.pack(pady=5)

        # Hunger Label and Progress Bar
        self.hunger_label = tk.Label(self.status_frame, text="Hunger")
        self.hunger_label.pack(pady=5)
        self.hunger_bar = Progressbar(self.status_frame, orient="horizontal", length=200, mode="determinate")
        self.hunger_bar.pack(pady=5)

        # Happiness Label and Progress Bar
        self.happiness_label = tk.Label(self.status_frame, text="Happiness")
        self.happiness_label.pack(pady=5)
        self.happiness_bar = Progressbar(self.status_frame, orient="horizontal", length=200, mode="determinate")
        self.happiness_bar.pack(pady=5)

        # Health Label and Progress Bar
        self.health_label = tk.Label(self.status_frame, text="Health")
        self.health_label.pack(pady=5)
        self.health_bar = Progressbar(self.status_frame, orient="horizontal", length=200, mode="determinate")
        self.health_bar.pack(pady=5)

        # Button Frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        # Control Buttons
        self.feed_button = tk.Button(self.button_frame, text="Feed Meal", command=lambda: self.pet.feed('meal'))
        self.snack_button = tk.Button(self.button_frame, text="Feed Snack", command=lambda: self.pet.feed('snack'))
        self.play_button = tk.Button(self.button_frame, text="Play", command=self.pet.play_with)
        self.sleep_button = tk.Button(self.button_frame, text="Sleep", command=self.pet.sleep)
        self.exercise_button = tk.Button(self.button_frame, text="Exercise", command=self.pet.exercise)
        self.clean_button = tk.Button(self.button_frame, text="Clean", command=self.pet.clean)
        self.quit_button = tk.Button(self.button_frame, text="Quit", command=self.quit_game)

        # Arrange buttons in a grid layout
        self.feed_button.grid(row=0, column=0, padx=5, pady=5)
        self.snack_button.grid(row=0, column=1, padx=5, pady=5)
        self.play_button.grid(row=1, column=0, padx=5, pady=5)
        self.sleep_button.grid(row=1, column=1, padx=5, pady=5)
        self.exercise_button.grid(row=2, column=0, padx=5, pady=5)
        self.clean_button.grid(row=2, column=1, padx=5, pady=5)
        self.quit_button.grid(row=2, column=2, padx=5, pady=5)

    def update_status(self):
        if self.pet:
            self.status_label.config(text=self.pet.status())
            self.hunger_bar["value"] = self.pet.hunger
            self.happiness_bar["value"] = self.pet.happiness
            self.health_bar["value"] = self.pet.health

            # Update mood music
            mood = self.pet.get_mood()
            play_background_music(mood)

    def unique_action(self):
        if self.pet and self.pet.alive:
            if isinstance(self.pet, Dog):
                self.pet.fetch_favorite_toy()
            elif isinstance(self.pet, Cat):
                self.pet.sharpen_claws()
            self.update_status()

    def on_pet_death(self):
        # Delete the saved game file
        if os.path.exists('saved_game.pkl'):
            os.remove('saved_game.pkl')
        messagebox.showinfo("Game Over", f"Unfortunately, {self.pet.name} has passed away.")
        # Return to pet selection
        self.game_frame.pack_forget()
        self.setup_pet_selection()

    def quit_game(self):
        if self.pet and self.pet.alive:
            with open('saved_game.pkl', 'wb') as f:
                pickle.dump(self.pet, f)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    GameManager(root)
    root.mainloop()
