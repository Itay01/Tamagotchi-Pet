from helpers.sound import play_sound_effect
from models.pet import Pet
from tkinter import messagebox


class Dog(Pet):
    def __init__(self, name, color, pattern, accessories, update_status_callback, game_over_callback, pet_type):
        super().__init__(name, color, pattern, accessories, update_status_callback, game_over_callback, pet_type)
        # Unique attribute
        self.favorite_toy = "Ball"

    def get_mood(self):
        """Dog-specific mood logic."""
        return super().get_mood()

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
