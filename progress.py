import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import subprocess


DATA_FILE = "FitnessTrackerData.txt"

class ProgressApp(ctk.CTk):
    def __init__(self, email):
        super().__init__()
        self.title(" Titans Fiteness Club - Progress Tracking")
        self.geometry("800x600")
        self.email = email
        self.workout_data = []  # List to hold workout data

        # Load data from the file
        self.load_workout_data()
        
        # Create UI elements
        self.create_widgets()

    def load_workout_data(self):
        try:
            with open(DATA_FILE, "r") as file:
                for line in file:
                    parts = line.strip().split(', ')
                    if parts[0] == self.email:  # Check if the email matches
                        date_str = parts[1]  # Date is at index 1
                        workout_type = parts[2]  # Workout type is at index 2
                        duration = int(parts[3].split()[0])  # Duration is at index 3
                        calories_burned = self.calculate_calories_burned(workout_type, duration)
                        self.workout_data.append((datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"), duration, calories_burned))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def calculate_calories_burned(self, workout_type, duration):
        # Basic example of calories burned per minute per workout type
        calories_per_minute = {
            "Plank": 3,
            "Squat": 5,
            "Lunge": 4,
            "Wall sit": 3,
            "Arm circles": 4,
            "Push-up": 7,
            "Step up": 5,
            "Shoulder bridge": 4,
            "Tuck jump": 6,
            "Mountain climber": 8,
            "Stair climb with bicep curl": 6,
            "Deadlifts": 6,
            "Leg press": 5,
            "Pull up": 7,
            "Bench press": 6,
        }
        return calories_per_minute.get(workout_type, 0) * duration

    def create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Workout Progress", font=("Helvetica", 24))
        title_label.pack(pady=20)

        # Button to show the graph
        show_graph_button = ctk.CTkButton(self, text="Show Progress Graph", command=self.show_progress_graph)
        show_graph_button.pack(pady=20)

          # Button to go back to the dashboard
        show_graph_button = ctk.CTkButton(self, text="Go back to dashboard", command=self.dashboard)
        show_graph_button.pack(pady=20)


    def dashboard(self):
        subprocess.Popen(['python', 'dashboard1.py', user_email])  # Pass the user's email
        quit()  # Close the current app

    def show_progress_graph(self):
        if not self.workout_data:
            messagebox.showinfo("No Data", "No workout data available for this user.")
            return

        dates = [data[0] for data in self.workout_data]
        durations = [data[1] for data in self.workout_data]
        calories = [data[2] for data in self.workout_data]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, durations, label='Duration (minutes)', color='blue', marker='o')
        plt.plot(dates, calories, label='Calories Burned', color='orange', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title('Workout Progress')
        plt.legend()
        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_email = sys.argv[1]
        app = ProgressApp(user_email)
        app.mainloop()
    else:
        print("No email passed")
