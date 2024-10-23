import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os

DATA_FILE = "FitnessTrackerData.txt"  # Assuming this is the file where workouts are saved
ctk.set_appearance_mode("white")  # Set dark appearance mode

class FitnessApp(ctk.CTk):
    def __init__(self, email):
        super().__init__()
        self.title('Titans Fitness Club - Dashboar')
        self.geometry('1366x768')
        self.attributes('-fullscreen', True)
        self.state('zoomed')
        self.configure(bg="#eff5f6")



        self.email = email  # Store the user's email for filtering the history

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Create the top frame (above left and right frames)
        top_frame = ctk.CTkFrame(self, border_width=2, height=100)
        top_frame.pack(side="top", fill="x", padx=20, pady=10)
      
        title_label = ctk.CTkLabel(top_frame, text="Dashboard", font=("Helvetica", 30))
        title_label.pack(pady=10)
       

        # Create a frame for the main section (Middle Frame to hold left and right frames)
        middle_frame = ctk.CTkFrame(self)
        middle_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        # Create a frame for the left section (Left Frame)
        left_frame = ctk.CTkFrame(middle_frame, border_width=2, width=150, height=400)
        left_frame.pack(side="left", padx=20, pady=10, fill="both", expand=True)

        # --- Left Frame Content ---
        title_label = ctk.CTkLabel(left_frame, text="Dashboard", font=("Helvetica", 30))
        title_label.pack(pady=50)

        # View History Button 
        view_history_button = ctk.CTkButton(left_frame, text="View History", corner_radius=10, command=self.view_history)
        view_history_button.pack(pady=(10, 10))  # Add some padding for spacing

        # Log Workout Button 
        logworkout_button = ctk.CTkButton(left_frame, text="Log Workouts", corner_radius=10, command=self.log_workout)
        logworkout_button.pack(pady=(10, 10))  # Add some padding for spacing

        # View Progress Button 
        view_progress_button = ctk.CTkButton(left_frame, text="View Progress", command=self.view_progress, corner_radius=10)
        view_progress_button.pack(pady=(5, 10))  # Add some padding for spacing

        # Logout Button
        logout_button = ctk.CTkButton(left_frame, text="Logout", command=self.logout, corner_radius=10)
        logout_button.pack(pady=(5, 10))  # Add some padding for spacing

        # Textbox to display workout history
        self.history_textbox = ctk.CTkTextbox(middle_frame, height=400, width=600)
        self.history_textbox.pack(pady=20)

    def log_workout(self):
        # Use subprocess to run logworkout.py
        subprocess.Popen(['python', 'logworkout.py', self.email])  # Pass the user's email to logworkout
        self.quit()  # Close the current app    

    def view_history(self):
        """View the user's goal, exercises, and workout history filtered by email."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                history_lines = file.readlines()

            # Extract the goal and exercises for the user
            user_info_lines = [line for line in history_lines if line.startswith(f"email: {self.email}")]
            user_history = [line for line in history_lines if line.startswith(self.email)]

            # Clear the text box before displaying new content
            self.history_textbox.delete('1.0', 'end')

            if user_info_lines:
                # Display the goal and exercises
                for entry in user_info_lines:
                    self.history_textbox.insert('end', entry + '\n')
            else:
                self.history_textbox.insert('end', "No goal or exercises found for your account.\n\n")

            if user_history:
                # Display the user's workout history in the textbox
                self.history_textbox.insert('end', "Workout History:\n")
                for entry in user_history:
                    self.history_textbox.insert('end', entry + '\n')
            else:
                self.history_textbox.insert('end', "No workout history found for your account.")
        else:
            messagebox.showerror("File Not Found", f"{DATA_FILE} not found. No history available.")

    def view_progress(self):
        # Functionality to view progress can be implemented here, if needed
        subprocess.Popen(['python', 'progress.py', self.email])  # Pass the user's email
        self.quit()  # Close the current app

    def logout(self):
        """Log out the user and return to the login screen."""
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            messagebox.showinfo("Logout", "You have been logged out.")
            self.quit()  # Close the current app to return to the login screen

if __name__ == "__main__":
    import sys
    user_email = sys.argv[1]  # Retrieve the user's email from command-line arguments
    app = FitnessApp(user_email)
    app.mainloop()
