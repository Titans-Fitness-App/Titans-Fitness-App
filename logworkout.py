import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import subprocess
import sys

DATA_FILE = "FitnessTrackerData.txt"
ctk.set_appearance_mode("white")  # Set appearance mode

class FitnessApp(ctk.CTk):
    def __init__(self, email):
        super().__init__()
        self.title("Titans Fitness Club - Log Workout")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.email = email  # Store the user's email

        # Load arrow image for the buttons
        self.arrow_image = ctk.CTkImage(Image.open("./arrow.png").resize((20, 20), Image.LANCZOS))

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side="top", fill="x", padx=20, pady=(10, 20))

        title_label = ctk.CTkLabel(button_frame, text="Log workouts", font=("Helvetica", 30))
        title_label.pack(pady=100)

        # Label for the workout type
        workout_type_label = ctk.CTkLabel(button_frame, text="Select type of workout", font=("Helvetica", 18))
        workout_type_label.pack(pady=5)

        # Dropdown for workout types
        self.workout_type_var = ctk.StringVar(value="Select Workout Type")
        self.workout_type_dropdown = ctk.CTkComboBox(button_frame, variable=self.workout_type_var, values=[
            "Plank", "Squat", "Lunge", "Wall sit", "Arm circles", "Push-up",
            "Step up", "Shoulder bridge", "Tuck jump", "Mountain climber",
            "Stair climb with bicep curl", "Deadlifts", "Leg press", "Pull up", "Bench press"
        ])
        self.workout_type_dropdown.pack(pady=5)

        # Label for the duration
        duration_label = ctk.CTkLabel(button_frame, text="Enter duration (m)", font=("Helvetica", 14))
        duration_label.pack(pady=5)

        # Entry for duration
        self.duration_entry = ctk.CTkEntry(button_frame, placeholder_text="Duration in minutes", corner_radius=10, width=300)
        self.duration_entry.pack(pady=10)

        # Save Button with arrow icon
        save_button = ctk.CTkButton(button_frame, text="Save", image=self.arrow_image, compound="right", corner_radius=10, command=self.save_workout)
        save_button.pack(pady=(10, 5))  # Add some padding for spacing

        # Dashboard Button with arrow icon
        dashboard_button = ctk.CTkButton(button_frame, text="Go to dashboard", image=self.arrow_image, compound="right", corner_radius=10, command=self.open_dashboard)
        dashboard_button.pack(pady=(5, 10))  # Add some padding for spacing

    def get_weight(self):
        """Retrieve weight from the FitnessTrackerData.txt file."""
        try:
            with open(DATA_FILE, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if self.email in line:
                        # Parse the weight from the line
                        parts = line.split(',')
                        for part in parts:
                            if "Weight:" in part:
                                weight_str = part.split(":")[1].strip().split(' ')[0]  # Get the weight value
                                return float(weight_str)  # Convert to float
        except FileNotFoundError:
            messagebox.showerror("Error", "Data file not found. Please ensure the measurements page was completed.")
            return None
        return None

    def calculate_calories_burned(self, workout_type, duration, weight):
        """Calculate calories burned based on workout type and duration."""
        # Metabolic equivalent of task (MET) values for different activities (approximate values)
        met_values = {
            "Plank": 3,
            "Squat": 5,
            "Lunge": 5,
            "Wall sit": 3,
            "Arm circles": 3,
            "Push-up": 8,
            "Step up": 4,
            "Shoulder bridge": 4,
            "Tuck jump": 8,
            "Mountain climber": 8,
            "Stair climb with bicep curl": 6,
            "Deadlifts": 6,
            "Leg press": 5,
            "Pull up": 8,
            "Bench press": 5
        }
        met = met_values.get(workout_type, 0)
        # Calculate calories burned
        calories_burned = (met * 3.5 * weight / 200) * duration
        return calories_burned

    def save_workout(self):
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        workout_type = self.workout_type_var.get()
        duration = self.duration_entry.get()

        # Validate input
        if workout_type == "Select Workout Type" or not duration.isdigit():
            messagebox.showerror("Input Error", "Please select a workout type and enter a valid duration.")
            return

        # Retrieve weight from the file
        weight = self.get_weight()
        if weight is None:
            return  # Stop if weight retrieval fails

        # Calculate calories burned
        duration_in_minutes = float(duration)
        calories_burned = self.calculate_calories_burned(workout_type, duration_in_minutes, weight)

        # Save the data to the text file, along with the user's email and calories burned
        try:
            with open(DATA_FILE, "a") as file:
                file.write(f"{self.email}, {current_date}, {workout_type}, {duration} minutes, Calories burned: {calories_burned:.2f}\n")
            # Clear the entry after saving
            self.duration_entry.delete(0, 'end')
            self.workout_type_var.set("Select Workout Type")
            messagebox.showinfo("Success", "Workout data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save workout data: {str(e)}")

    def open_dashboard(self):
        # Use subprocess to run dashboard.py and pass the user's email
        subprocess.Popen(['python', 'dashboard1.py', self.email])  # Pass the user's email to dashboard
        self.destroy()  # Close the current app

    def logout(self):
        # Print the email for debugging
        print(f"Logging out with email: {self.email}")

        # Use subprocess to run login.py and pass the user's email
        subprocess.Popen(['python', 'login.py', self.email])  # Pass the user's email to login page
        self.quit()  # Close the current app

if __name__ == "__main__":
    # Get the email passed from the previous script
    if len(sys.argv) > 1:
        user_email = sys.argv[1]
        app = FitnessApp(user_email)
        app.mainloop()
    else:
        print("No email passed")
