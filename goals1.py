import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox


# Set up the theme and appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# Function to handle saving fitness data
def save_fitness_data(data, email):
    try:
        with open('FitnessTrackerData.txt', 'a') as file:
            file.write(f"Email: {email}\n{data}\n")
    except Exception as e:
        print(f"Failed to save data: {e}")


class FitnessTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.selected_fitness_goal = None
        self.selected_focus_areas = []  # To store multiple focus areas
        self.user_email = None  # To store user's email
        self.title("Goal Setting and Focus")

        # Set initial window size to maximized using geometry
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        # Load background image
        self.background_image = Image.open("img/EZ bar biceps curl.jpg")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.background_image = self.background_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_image_ctk = ctk.CTkImage(self.background_image, size=(screen_width, screen_height))

        # Main menu - Fitness Goals
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.get_user_email()  # Collect user email at startup
        self.create_main_menu()

    def get_user_email(self):
        # Prompt user for their email
        email = simpledialog.askstring("Input", "Please enter your email:")
        if email:
            self.user_email = email  # Store the email for later use
        else:
            messagebox.showwarning("Warning", "Email is required to proceed.")
            self.get_user_email()  # Prompt again if email is not provided

    def create_main_menu(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Add background label with image
        self.background_label = ctk.CTkLabel(self.main_frame, image=self.bg_image_ctk, text="")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = ctk.CTkLabel(self.main_frame, text="Select Your Fitness Goal", font=("Arial", 40))
        self.label.pack(pady=40)

        # Fitness goal buttons
        self.weight_loss_button = ctk.CTkButton(self.main_frame, text="Weight Loss", font=("Arial", 28), command=lambda: self.show_focus_areas("Weight Loss"))
        self.weight_loss_button.pack(pady=10)

        self.muscle_gain_button = ctk.CTkButton(self.main_frame, text="Muscle Gain", font=("Arial", 28), command=lambda: self.show_focus_areas("Muscle Gain"))
        self.muscle_gain_button.pack(pady=10)

        self.body_shape_button = ctk.CTkButton(self.main_frame, text="Body Shape", font=("Arial", 28), command=lambda: self.show_focus_areas("Body Shape"))
        self.body_shape_button.pack(pady=10)

        self.cardio_button = ctk.CTkButton(self.main_frame, text="Cardio", font=("Arial", 28), command=lambda: self.show_focus_areas("Cardio"))
        self.cardio_button.pack(pady=10)

    def show_focus_areas(self, goal):
        self.selected_fitness_goal = goal  # Save the selected fitness goal

        # Remove current widgets from main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Add background label with image
        self.background_label = ctk.CTkLabel(self.main_frame, image=self.bg_image_ctk, text="")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Back button with icon
        back_image = Image.open("img/back-button.png").resize((30, 30), Image.LANCZOS)  # Update with your icon path
        self.back_icon = ctk.CTkImage(back_image, size=(30, 30))
        back_button = ctk.CTkButton(self.main_frame, image=self.back_icon, text="", command=self.create_main_menu, width=40)
        back_button.pack(side="top", anchor="nw", padx=10, pady=10)

        # Label for focus area
        self.label = ctk.CTkLabel(self.main_frame, text=f"Select Focus Area for {goal}", font=("Arial", 40))
        self.label.pack(pady=40)

        # Checkboxes for focus areas
        self.checkboxes = {}
        focus_areas = ['Legs', 'Back', 'Shoulders', 'Arms', 'Abs', 'Butt', 'Chest', 'Full Body']
        for area in focus_areas:
            var = ctk.StringVar(value="")
            checkbox = ctk.CTkCheckBox(self.main_frame, text=area, variable=var)
            checkbox.pack(pady=10)
            self.checkboxes[area] = var  # Store variable for each checkbox

        # "Next" button
        next_button = ctk.CTkButton(self.main_frame, text="Next →", command=self.save_and_proceed, font=("Arial", 28))
        next_button.pack(pady=20)

    def save_and_proceed(self):
        # Gather selected focus areas
        self.selected_focus_areas = [area for area, var in self.checkboxes.items() if var.get()]

        # Save selections to file
        with open("FitnessTrackerData.txt", "a") as file:
            file.write(f"Email: {self.user_email}, Fitness Goal: {self.selected_fitness_goal}, Focus Areas: {', '.join(self.selected_focus_areas)}\n")

        # Show confirmation message
        messagebox.showinfo("Selection Complete", f"Selected Goal: {self.selected_fitness_goal}\nFocus Areas: {', '.join(self.selected_focus_areas)}")

        # Proceed to the next step
        subprocess.Popen(['python', 'measurements.py', self.user_email])  # Pass the user's email
    #    self.quit()  # Close the current app


# Create and run the application
if __name__ == "__main__":
    app = FitnessTrackerApp()
    app.mainloop()
