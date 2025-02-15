import os
import json
import pyautogui
import time
import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from vosk import Model, KaldiRecognizer
import pyaudio
import keyboard  # Import the keyboard library
import threading
from command_mapping import command_mapping, number_mapping

# Define the model path relative to the script's location
if getattr(sys, 'frozen', False):  # If the app is frozen (running as .exe)
    base_path = Path(sys._MEIPASS)
else:  # If running as a script
    base_path = Path(__file__).parent

model_path = base_path / "vosk-model-small-en-us-0.15"

if not model_path.exists():
    print(f"Model not found in {model_path}. Please ensure it is included in the bundle.")
    sys.exit(1)

print("Loading model...")
model = Model(str(model_path))
recognizer = KaldiRecognizer(model, 16000)
print("Model loaded successfully.")

def convert_numbers_to_string(words):
    """Convert number words to their numeric string representation."""
    numeric_string = ""
    for word in words:
        if word in number_mapping:
            numeric_string += number_mapping[word]
    return numeric_string

def process_number(numeric_string):
    if len(numeric_string) == 5:
        return numeric_string[:3] 
    elif len(numeric_string) == 4: 
        return '0' + numeric_string[:2]
    else:
        return numeric_string

def listen_and_type():
    print("Initializing PyAudio...")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    print("PyAudio initialized and stream started.")

    status_label.config(text="Listening for command...")
    
    while True:
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            command = result_dict.get('text', '').strip()  # Strip any leading/trailing whitespace
            if command:
                print(f"Recognized command: {command}")
                # Split the command into words and map them
                words = command.lower().split()
                abbreviated_command = []
                numeric_string = ""

                for word in words:
                    mapped_word = command_mapping.get(word)
                    if mapped_word:
                        abbreviated_command.append(mapped_word)
                    else:
                        numeric_string += convert_numbers_to_string([word])  # Convert numbers separately
                        numeric_string = process_number(numeric_string)

                # Join the abbreviations and numeric string
                final_abbreviation = ';' + ''.join(abbreviated_command) + numeric_string
                print(f"Mapped command: {final_abbreviation}")

                status_label.config(text=f"You said: {command} (Mapped: {final_abbreviation})")
                time.sleep(1)

                # Type the command
                pyautogui.write(final_abbreviation + '\n', interval=0.1)
                print("Command typed.")

                break

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Stream stopped and PyAudio terminated.")

def start_listening():
    print("Waiting for 'END' key press to start listening...")
    while True:
        keyboard.wait('end')  # Wait for the END key to be pressed
        print("'END' key pressed. Starting to listen...")
        listen_and_type()  # Start listening when the END key is pressed

# Create the main window
print("Creating main window...")
root = tk.Tk()
root.title("Voice Command Input for Vice ATC Simulator")

frame = tk.Frame(root)
frame.pack(pady=20)

status_label = tk.Label(frame, text="Press 'END' to start listening", font=("Arial", 14))
status_label.pack(pady=10)

# Start the listening loop in a separate thread
print("Starting listener thread...")
listener_thread = threading.Thread(target=start_listening, daemon=True)
listener_thread.start()

print("Starting main loop...")
root.mainloop()
