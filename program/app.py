import customtkinter as ctk
import threading
from program import start_listening

# Create the main window
print("Creating main window...")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Voice for Vice")
root.minsize(300, 150)
root.geometry("300x150")
root.resizable(False, False)

# Create a frame for the main content
frame = ctk.CTkFrame(root)
frame.pack(pady=10, padx=10, fill="both", expand=True)
frame.pack_propagate(False)
frame.configure(height=60)

# Status label
status_label = ctk.CTkLabel(frame, text="Press 'END' to start listening", font=("Arial", 14), wraplength=250) # replace 'end' with a verible after we have the settings page
status_label.pack(pady=(0, 10), expand=True)

# function to update the status label
def update_status(message):
    status_label.configure(text=message) # update the status label with the "message", to update the status label: update_status("your message here")

# Function to open the settings window
def open_settings():
    settings_window = ctk.CTkToplevel(root)
    settings_window.title("Settings")
    root.minsize(300, 200)
    settings_window.geometry("300x200")
    root.resizable(False, False)
    settings_window.attributes("-topmost", True)

# Function to open the approaches window
def open_approaches():
    approaches_window = ctk.CTkToplevel(root)
    approaches_window.title("Approaches")
    root.minsize(300, 200)
    approaches_window.geometry("300x200")
    root.resizable(False, False)
    approaches_window.attributes("-topmost", True)

# Create a frame for the buttons to keep them separated from the status label
button_frame = ctk.CTkFrame(root, fg_color="transparent")
button_frame.pack(pady=(0, 10), padx=10, fill="x")

# Approaches button
approaches_button = ctk.CTkButton(button_frame, text="Approaches", command=open_approaches)
approaches_button.pack(side="left", padx=(0, 5))

# Settings button
settings_button = ctk.CTkButton(button_frame, text="Settings", command=open_settings)
settings_button.pack(side="right", padx=(5, 0))

# Start the listening loop in a separate thread
print("Starting listener thread...")
listener_thread = threading.Thread(target=start_listening, args=(update_status,), daemon=True)
listener_thread.start()

print("Starting main loop...")
root.mainloop()
