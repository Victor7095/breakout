from random import choice
import simpleaudio as sa
import threading


selected_sound = None
sounds = None
state = None


def set_music_state(new_state):
    global state
    state = new_state


# função para tocar som
def play(sound):
    wave_obj = sa.WaveObject.from_wave_file(sound)
    wave_obj.play()


def loop_play():
    global selected_sound
    if not selected_sound:
        selected_sound = choice(sounds)
    wave_obj = sa.WaveObject.from_wave_file(selected_sound)
    play_obj = wave_obj.play()
    while state == "playing":
        print(selected_sound)
        if not play_obj.is_playing():
            play_obj = wave_obj.play()
    play_obj.stop()


def play_background(bg_thread, new_state, psounds):
    set_music_state(new_state)
    global sounds
    sounds = psounds
    if not bg_thread:
        bg_thread = threading.Thread(target=loop_play)
        bg_thread.setDaemon(True)
        bg_thread.start()
