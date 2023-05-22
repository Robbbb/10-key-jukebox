import time
import os
import RPi.GPIO as GPIO
from pygame import mixer
# python /home/pi/critter/ButtonTriggerProgram.py 
# Audio files
audio_files = ["/home/pi/critter/audio1.mp3","/home/pi/critter/audio2.mp3","/home/pi/critter/audio3.mp3","/home/pi/critter/audio4.mp3","/home/pi/critter/audio5.mp3","/home/pi/critter/audio6.mp3","/home/pi/critter/audio7.mp3","/home/pi/critter/audio8.mp3","/home/pi/critter/audio9.mp3","/home/pi/critter/audio10.mp3"]

# Button GPIO pins
button_pins = [4, 17, 27]

# LED GPIO pins
led_pins = [14, 15, 18]

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Initialize GPIO and set button and LED directions
for button_pin in button_pins:
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for led_pin in led_pins:
    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.output(led_pin, GPIO.LOW)

# Initialize Pygame mixer
mixer.init()
mixer.music.set_volume(0.5)

# Button press detection and audio playback
def button_press(index):
    file_path = audio_files[index]
    print(f"Button {index} pressed. Playing {file_path}", end='')

    if mixer.music.get_busy() and mixer.music.get_pos() > 0:
        stop_audio()
        print("Audio playback stopped.")
    else:
        play_audio(file_path)
        # print("Audio playback started.")

        # Light up the corresponding LED
        GPIO.output(led_pins[index], GPIO.HIGH)
        print(f"LED {index} on")


# Play audio file
def play_audio(file_path):
    mixer.music.load(file_path)
    mixer.music.play()
    global current_file_index
    current_file_index = audio_files.index(file_path)


# Stop audio playback
def stop_audio():
    mixer.music.stop()

# Initialize button state and timing variables
button_states = [True] * len(button_pins)
button_last_times = [0.0] * len(button_pins)

# Initialize LED states
led_states = [False] * len(led_pins)

# Boot-up LED test
print("Boot-up LED test")
for i, led_pin in enumerate(led_pins):
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(led_pin, GPIO.LOW)
    # time.sleep(0.5)
print("DONE!")

# Initialize current_file_index
current_file_index = -1

# Main loop
while True:
    for i, button_pin in enumerate(button_pins):
        button_state = GPIO.input(button_pin)

        if button_state != button_states[i]:
            if button_state:  # Button released
                if time.time() - button_last_times[i] > 0.05:  # Minimum 50ms release time
                    button_press(i)
            else:  # Button pressed
                button_last_times[i] = time.time()

        button_states[i] = button_state

    # Check if the audio playback has finished
    if not mixer.music.get_busy() and current_file_index != -1:
        GPIO.output(led_pins[current_file_index], GPIO.LOW)
        print(f"Audio playback of file {current_file_index} has finished. LED OFF")
        current_file_index = -1

    time.sleep(0.01)

GPIO.cleanup() # Cleanup all GPIO