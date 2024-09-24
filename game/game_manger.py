import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from helpers.sound import *
import os
import pickle
from tkinter.ttk import Progressbar

from models.cat import Cat
from models.dog import Dog


class GameManager:
    def __init__(self, root):
        self.root = root
        self.pet = None
        self.center_window(320, 500)
        play_background_music(is_init_game=True)

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
            self.pet = Dog(pet_name, color, pattern, accessories, self.update_status, self.on_pet_death, "dog")
        elif pet_type == "cat":
            self.pet = Cat(pet_name, color, pattern, accessories, self.update_status, self.on_pet_death, "cat")

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
