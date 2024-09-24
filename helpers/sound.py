import pygame
import datetime

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
