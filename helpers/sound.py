import pygame
import datetime

prev_mood = "neutral"

def play_background_music(mood='neutral', is_init_game=False):
    global prev_mood
    if mood == prev_mood and not is_init_game: return

    pygame.mixer.music.stop()
    if mood == 'happy':
        prev_mood = mood
        music_file = 'sounds/happy_music.mp3'
    elif mood == 'sad':
        prev_mood = mood
        music_file = 'sounds/sad_music.mp3'
    else:
        current_hour = datetime.datetime.now().hour
        if 6 <= current_hour < 18:
            music_file = 'sounds/day_music.mp3'
        else:
            music_file = 'sounds/night_music.mp3'
    try:
        sound = pygame.mixer.Sound(music_file)
        channel = pygame.mixer.Channel(0)  # Use channel 0 for background music
        channel.play(sound, loops=-1)  # Play in a loop to keep background music going
    except Exception as e:
        print(f"Error playing background music: {e}")

def play_sound_effect(sound_file):
    try:
        sound = pygame.mixer.Sound(sound_file)
        channel = pygame.mixer.Channel(1)  # Use channel 1 for sound effects
        channel.play(sound)
    except Exception as e:
        print(f"Error playing sound effect: {e}")
