import customtkinter as ctk
import threading
from program import start_listening
import keyboard
import settings

# Create the main window
print("Creating main window...")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Voice for Vice")
root.minsize(300, 150)
root.geometry("300x150")
root.resizable(False, False)
root.attributes("-topmost", True)

# Create a frame for the main content
frame = ctk.CTkFrame(root)
frame.pack(pady=10, padx=10, fill="both", expand=True)

# Status label
status_label = ctk.CTkLabel(frame, text=f"Press {settings.ptt_key} to start listening", font=("Arial", 14), wraplength=250)
status_label.pack(pady=(0, 10), expand=True)

# function to update the status label
def update_status(message):
    status_label.configure(text=message) # update the status label with the "message", to update the status label: update_status("your message here")

# Function to open the settings window
def open_settings():
    settings_window = ctk.CTkToplevel(root)
    settings_window.title("Settings")
    settings_window.minsize(300, 265)
    settings_window.geometry("300x265")
    settings_window.resizable(True, True) # change to false when we have a settings page
    settings_window.attributes("-topmost", True)

    # Function to handle PTT key setup
    def setup_ptt_key():
        settings.ptt_key
        ptt_button.configure(text="Press any key!")
            
        # Listen for a key press
        def on_key_press(keyboard_event):
            settings.ptt_key = keyboard_event.name  # Save the pressed key as the PTT key
            keyboard.unhook_all()  # Stop listening for keys after one is pressed
            ptt_button.configure(text=f"PTT key set to: {settings.ptt_key}")
            update_status(f"Press {settings.ptt_key} to start listening")
            print(f"PTT key set to: {settings.ptt_key}")

            # Restart listening for the new PTT key
            listener_thread = threading.Thread(target=start_listening, args=(update_status,), daemon=True)
            listener_thread.start()

        keyboard.on_press(on_key_press)  # Listen for any key press

    # Appearance settings
    settings_appearance_frame = ctk.CTkFrame(settings_window, fg_color="transparent", width=300, height=100)
    settings_appearance_frame.pack(pady=(10, 5), padx=10)
    settings_appearance_frame.pack_propagate(False)

    settings_appearance_label = ctk.CTkLabel(settings_appearance_frame, text="Appearance Settings", font=("Arial", 14))
    settings_appearance_label.pack(pady=0, padx=10)

    appearance_button_frame = ctk.CTkFrame(settings_appearance_frame, fg_color="transparent")
    appearance_button_frame.pack(pady=(10, 0), padx=0, fill="x")

    dark_button = ctk.CTkButton(appearance_button_frame, text="Dark", width=80, corner_radius=15, command=lambda: ctk.set_appearance_mode("dark"))
    dark_button.pack(side="left", pady=5, padx=(10, 0))

    light_button = ctk.CTkButton(appearance_button_frame, text="Light", width=80, corner_radius=15, command=lambda: ctk.set_appearance_mode("light"))
    light_button.pack(side="left", pady=5, padx=10)

    auto_button = ctk.CTkButton(appearance_button_frame, text="Auto", width=80, corner_radius=15, command=lambda: ctk.set_appearance_mode("auto"))
    auto_button.pack(side="right", pady=5, padx=(0, 10))

    # Push to talk settings
    settings_ptt_frame = ctk.CTkFrame(settings_window, fg_color="transparent", width=300, height=100)
    settings_ptt_frame.pack(pady=(5, 5), padx=10)
    settings_ptt_frame.pack_propagate(False)

    settings_ptt_label = ctk.CTkLabel(settings_ptt_frame, text="Push-To-Talk Settings", font=("Arial", 14))
    settings_ptt_label.pack(pady=0, padx=10)

    ptt_button_frame = ctk.CTkFrame(settings_ptt_frame, fg_color="transparent")
    ptt_button_frame.pack(pady=(10, 0), padx=0, fill="x")

    ptt_button = ctk.CTkButton(ptt_button_frame, text="Select your PTT key", width=80, corner_radius=15, command=setup_ptt_key)
    ptt_button.pack(pady=5, padx=10)

    # Save button frame
    save_button_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
    save_button_frame.pack(pady=(2, 0), padx=10, fill="both")

    save_button = ctk.CTkButton(save_button_frame, text="Save", command=settings_window.destroy)
    save_button.pack(side="right", pady=0, padx=0)

# Function to open the approaches window
def open_approaches():
    approaches_window = ctk.CTkToplevel(root)
    approaches_window.title("Approaches")
    approaches_window.minsize(300, 200)
    approaches_window.geometry("300x200")
    approaches_window.resizable(False, False)
    approaches_window.attributes("-topmost", True)

# Create a frame for the buttons to keep them separated from the status label
main_button_frame = ctk.CTkFrame(root, fg_color="transparent")
main_button_frame.pack(pady=(0, 10), padx=10, fill="x")

# Approaches button
approaches_button = ctk.CTkButton(main_button_frame, text="Approaches", command=open_approaches)
approaches_button.pack(side="left", padx=(0, 5))

# Settings button
settings_button = ctk.CTkButton(main_button_frame, text="Settings", command=open_settings)
settings_button.pack(side="right", padx=(5, 0))

# Start the listening loop in a separate thread
print("Starting listener thread...")
listener_thread = threading.Thread(target=start_listening, args=(update_status,), daemon=True)
listener_thread.start()

print("Starting main loop...")
root.mainloop()
