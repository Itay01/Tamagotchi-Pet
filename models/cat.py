from helpers.sound import play_sound_effect
from models.pet import Pet
from tkinter import messagebox


class Cat(Pet):
    def __init__(self, name, color, pattern, accessories, update_status_callback,game_over_callback, pet_type):
        super().__init__(name, color, pattern, accessories, update_status_callback, game_over_callback, pet_type)
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
