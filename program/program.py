import json
import pyautogui
import time
import sys
from pathlib import Path
from vosk import Model, KaldiRecognizer
import pyaudio
import keyboard
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
    # Convert number words to their numeric string representation.
    numeric_string = ""
    for word in words:
        if word in number_mapping:
            numeric_string += number_mapping[word]
    return numeric_string

def process_number(numeric_string):
    # Process the numeric string to ensure it is in the correct format.
    if len(numeric_string) == 5:
        return numeric_string[:3] 
    elif len(numeric_string) == 4: 
        return '0' + numeric_string[:2]
    else:
        return numeric_string

def listen_and_type(update_status):
    # Listen for a command map the command and type it out)
    print("Initializing PyAudio...")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    print("PyAudio initialized and stream started.")

    update_status("Listening for command...")
    
    while True:
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            command = result_dict.get('text', '').strip()
            if command:
                print(f"Recognized command: {command}")
                words = command.lower().split()
                abbreviated_command = []
                numeric_string = ""

                for word in words:
                    mapped_word = command_mapping.get(word)
                    if mapped_word:
                        abbreviated_command.append(mapped_word)
                    else:
                        numeric_string += convert_numbers_to_string([word])
                        numeric_string = process_number(numeric_string)

                final_abbreviation = ';' + ''.join(abbreviated_command) + numeric_string
                print(f"Mapped command: {final_abbreviation}")

                update_status(f"You said: {command} (Mapped: {final_abbreviation})")
                time.sleep(1)

                pyautogui.write(final_abbreviation + '\n', interval=0.1)
                print("Command typed.")

                break

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Stream stopped and PyAudio terminated.")

def start_listening(update_status):
    # Wait for the 'END' key press and call listen_and_type function
    print(f"Waiting for 'END' key press to start listening...")
    while True:
        keyboard.wait('end') # change to verible when we have a settings page
        print("'END' key pressed. Starting to listen...") # change 'end' to a verible when we have a settings page
        listen_and_type(update_status)