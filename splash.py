import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import time
import pygame

class SplashScreen:
    def __init__(self, duration=9000):
        self.duration = duration
        self.splash = ctk.CTk()
        self.splash.geometry(f"{self.splash.winfo_screenwidth()}x{self.splash.winfo_screenheight()}")
        self.splash.title("Welcome to Titans Fitness Club")
        self.splash.attributes('-fullscreen', True)

        # Set background color
        self.splash.configure(fg_color="dark gray")

        # Play background music
        self.play_music()

        # Load and resize logo image
        self.load_logo()

        # Create a frame to center content
        center_frame = ctk.CTkFrame(self.splash, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Display the logo
        if self.logo_photo:
            self.logo_label = ctk.CTkLabel(center_frame, image=self.logo_photo, text="")
            self.logo_label.pack(pady=(0, 20))

        # Overlay text
        self.overlay_label = ctk.CTkLabel(center_frame, text="Titans Fitness", font=("Helvetica", 40, "bold"), text_color="black")
        self.overlay_label.pack(pady=(0, 20))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(center_frame, width=300, fg_color="white", progress_color="black")
        self.progress_bar.pack(pady=(0, 20))
        self.progress_bar.set(0)

        # Version label
        version_label = ctk.CTkLabel(self.splash, text="Version 1.0", font=("Helvetica", 12), text_color="white")
        version_label.place(relx=0.95, rely=0.98, anchor="se")

        # Skip button
        skip_button = ctk.CTkButton(self.splash, text="Skip", command=self.close, fg_color="black", text_color="white")
        skip_button.place(relx=0.95, rely=0.05, anchor="ne")

        # Start loading animation
        self.splash.after(100, self.load_animation)

    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load("gym-phonk.mp3")  # Ensure the file exists
        pygame.mixer.music.play(-1)  # Play music in a loop

    def load_logo(self):
        try:
            logo_image = Image.open("img/train.jpg")
            logo_image = logo_image.resize((300, 300))  # Adjust size as needed
            self.logo_photo = ImageTk.PhotoImage(logo_image)
        except FileNotFoundError:
            print("Logo image not found. Using text instead.")
            self.logo_photo = None

    def load_animation(self):
        steps = 100
        interval = self.duration / steps
        for i in range(steps):
            time.sleep(interval / 1000)  # Convert milliseconds to seconds
            self.progress_bar.set((i + 1) / steps)
            self.splash.update_idletasks()

        # End the splash screen
        self.close()

    def close(self):
        pygame.mixer.music.stop()
        self.splash.destroy()
        try:
            subprocess.Popen(["python", "Login.py"])  # Run the login screen
        except FileNotFoundError:
            print("Login.py not found. Please check the file name and path.")

    def run(self):
        self.splash.mainloop()

if __name__ == "__main__":
    splash_screen = SplashScreen(duration=9000)
    splash_screen.run()
