import customtkinter as ctk
from tkinter import messagebox, simpledialog
import subprocess
from PIL import Image, ImageTk
from datetime import datetime

DATA_FILE = "FitnessData.txt"
USER_FILE = "Users.txt"  # File to store usernames and passwords
ctk.set_appearance_mode("dark")  # Set dark appearance mode

class FitnessApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Fitness App")
        self.geometry("800x1000")
        
        self.username = None  # Store the username of the logged-in user
        self.create_login_window()  # Create the login window

    def create_login_window(self):
        # Create a simple login dialog
        self.username = simpledialog.askstring("Login", "Enter your username:")
        if self.username:
            self.create_widgets()  # If username is entered, create main app widgets
        else:
            messagebox.showerror("Login Error", "Username cannot be empty.")
            self.quit()  # Exit if no username is provided

    def create_widgets(self):
        # Create the top frame (above left and right frames)
        top_frame = ctk.CTkFrame(self, border_width=2, height=100)
        top_frame.pack(side="top", fill="x", padx=20, pady=10)

        # Load and display the gym image
        gym_image = Image.open("img/gym.jpg")  # Replace with your image path
        gym_image = gym_image.resize((800, 300))  # Match the window width (800px)
        gym_photo = ImageTk.PhotoImage(gym_image)

        image_label = ctk.CTkLabel(top_frame, image=gym_photo, text="")
        image_label.image = gym_photo  # Keep a reference to prevent garbage collection
        image_label.pack(side="left", fill="x", expand=True, padx=20)

        # Create a frame for the main section (Middle Frame to hold left and right frames)
        middle_frame = ctk.CTkFrame(self)
        middle_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        # Create a frame for the left section (Left Frame)
        left_frame = ctk.CTkFrame(middle_frame, fg_color="#a28655", border_color="#8DC6F3", border_width=2, width=150, height=400)
        left_frame.pack(side="left", padx=20, pady=10, fill="both", expand=True)

        # --- Left Frame Content ---
        title_label = ctk.CTkLabel(left_frame, text="Log workouts", font=("Helvetica", 24))
        title_label.pack(pady=5)

        # Label for the workout type
        workout_type_label = ctk.CTkLabel(left_frame, text="Select type of workout", font=("Helvetica", 14))
        workout_type_label.pack(pady=5)

        # Dropdown for workout types
        self.workout_type_var = ctk.StringVar(value="Select Workout Type")
        self.workout_type_dropdown = ctk.CTkComboBox(left_frame, variable=self.workout_type_var, values=["Plank", "Squat", "Lunge", "Wall sit", "Arm circles", "Push-up", "Step up", "Shoulder bridge", "Tuck jump", "Mountain climber", "Stair climb with bicep curl", "Deadlifts", "Leg press", "Pull up", "Bench press"])
        self.workout_type_dropdown.pack(pady=10)

        # Label for the duration
        duration_label = ctk.CTkLabel(left_frame, text="Enter duration (m)", font=("Helvetica", 14))
        duration_label.pack(pady=5)

        # Entry for duration
        self.duration_entry = ctk.CTkEntry(left_frame, placeholder_text="Duration in minutes", corner_radius=10, width=300)
        self.duration_entry.pack(pady=5)

        # Create a frame for the buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side="top", fill="x", padx=20, pady=(10, 20))

        # Save Button 
        save_button = ctk.CTkButton(button_frame, text="Save", corner_radius=10, command=self.save_workout)
        save_button.pack(pady=(10, 5))  # Add some padding for spacing

        # Dashboard Button 
        dashboard_button = ctk.CTkButton(button_frame, text="View My Workouts", command=self.view_workouts, corner_radius=10)
        dashboard_button.pack(pady=(5, 10))  # Add some padding for spacing

    def save_workout(self):
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        workout_type = self.workout_type_var.get()
        duration = self.duration_entry.get()

        # Validate input
        if workout_type == "Select Workout Type" or not duration.isdigit():
            messagebox.showerror("Input Error", "Please select a workout type and enter a valid duration.")
            return

        # Save the data to the text file with username
        with open(DATA_FILE, "a") as file:
            file.write(f"{self.username}, {current_date}, {workout_type}, {duration} minutes\n")

        # Clear the entry after saving
        self.duration_entry.delete(0, 'end')
        self.workout_type_var.set("Select Workout Type")
        messagebox.showinfo("Success", "Workout data saved successfully!")

    def view_workouts(self):
        user_workouts = []
        with open(DATA_FILE, "r") as file:
            for line in file:
                if line.startswith(self.username):
                    user_workouts.append(line.strip())

        if user_workouts:
            workouts_string = "\n".join(user_workouts)
            messagebox.showinfo("My Workouts", f"Your Workouts:\n{workouts_string}")
        else:
            messagebox.showinfo("My Workouts", "No workouts logged.")

    def open_dashboard(self):
        # Use subprocess to run dashboard.py
        subprocess.Popen(['python', 'dashboard.py'])  # Adjust this line as needed for your environment
        self.quit()  # Close the current app

if __name__ == "__main__":
    app = FitnessApp()
    app.mainloop()
