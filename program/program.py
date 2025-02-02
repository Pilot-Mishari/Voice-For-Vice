import os
import json
import pyautogui
import time
import tkinter as tk
from tkinter import messagebox
from vosk import Model, KaldiRecognizer
import pyaudio
import keyboard  # Import the keyboard library
import threading

# Define the model path relative to the script's location
if getattr(sys, 'frozen', False):  # If the app is frozen (running as .exe)
    model_path = Path(sys._MEIPASS) / "vosk-model-small-en-us-0.15"
else:  # If running as a script
    model_path = Path(__file__).parent / "vosk-model-small-en-us-0.15"  # Current directory

if not model_path.exists():
    print(f"Model not found in {model_path}. Please ensure it is in the same directory as the script.")
    exit(1)

model = Model(str(model_path))

# Mapping commands to abbreviations
command_mapping = {
    #Headings
    "turn": "H",
    "left": "H",
    "Right": "R",
    "Heading": "H",
    "Head": "H",
    "fly": "H",
    "flight": "H",
    "flooding": "H",
    "fighting": "H",
    "Hheading": "H",
    "play hanging": "H",

    #speeds
    "speed": "S",
    "speeds": "S",
    "reduce": "S",
    "increse": "S",
    "slow": "S",

    #altuides
    "cromatina": "C",
    "chrome": "C",
    "descendant maintained": "C",
    "clementine": "C",
    "climb": "C",
    "maintain": "C",
    "desend": "C",
    "climate change": "C",
    "crime": "C",
    "clamp": "C",
    "clam": "C",
    "client": "C",

    #next controller
    "contact depature": "FC",
    "depart": "FC",

    #tower
    "tower": "TO",
    "contact tower": "TO",

    #locliser
    "intercept": "I",
    "locliser": "I",
    "inter": "I",
    "sept": "I",

    #directs
    "direct": "D",
    "procedure": "D",
    "proceed": "D"
}

# Mapping number words to their integer values
number_mapping = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "hundred": "100",
    "thousand": "1000"
}

def convert_numbers_to_string(words):
    """Convert number words to their numeric string representation."""
    numeric_string = ""
    for word in words:
        if word in number_mapping:
            numeric_string += number_mapping[word]
    return numeric_string

def listen_and_type():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    status_label.config(text="Listening for command...")
    
    while True:
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            command = result_dict.get('text', '').strip()  # Strip any leading/trailing whitespace
            if command:
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

                # Join the abbreviations and numeric string
                final_abbreviation = ';' + ''.join(abbreviated_command) + numeric_string

                status_label.config(text=f"You said: {command} (Mapped: {final_abbreviation})")
                time.sleep(1)

                # Type the command and press Enter
                pyautogui.typewrite(final_abbreviation + '\n')
                pyautogui.press('enter')  # Simulate pressing the Enter key

                break

    stream.stop_stream()
    stream.close()
    p.terminate()

def start_listening():
    while True:
        keyboard.wait('end')  # Wait for the END key to be pressed
        listen_and_type()  # Start listening when the END key is pressed

# Create the main window
root = tk.Tk()
root.title("Voice Command Input for Vice ATC Simulator")

frame = tk.Frame(root)
frame.pack(pady=20)

status_label = tk.Label(frame, text="Press 'END' to start listening", font=("Arial", 14))
status_label.pack(pady=10)

# Start the listening loop in a separate thread
listener_thread = threading.Thread(target=start_listening, daemon=True)
listener_thread.start()

root.mainloop()
