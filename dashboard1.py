import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import subprocess
import os
import sys
import matplotlib.pyplot as plt
from datetime import datetime

DATA_FILE = "FitnessTrackerData.txt"  # Assuming this is the file where workouts are saved

# Function to calculate calories burned based on workout type and duration
def calculate_calories_burned(workout_type, duration):
    calories_per_minute = {
        "Plank": 3, "Squat": 5, "Lunge": 4, "Wall sit": 3, "Arm circles": 4, "Push-up": 7,
        "Step up": 5, "Shoulder bridge": 4, "Tuck jump": 6, "Mountain climber": 8,
        "Stair climb with bicep curl": 6, "Deadlifts": 6, "Leg press": 5, "Pull up": 7, "Bench press": 6,
    }
    return calories_per_minute.get(workout_type, 0) * duration

# Function to load the user's workout data from the file
def load_workout_data(email):
    workout_data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(', ')
                if parts[0] == email:  # Check if the line matches the user's email
                    date_str = parts[1]
                    workout_type = parts[2]
                    duration = int(parts[3].split()[0])
                    calories_burned = calculate_calories_burned(workout_type, duration)
                    workout_data.append((datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"), workout_type, duration, calories_burned))
    return workout_data

# Function to display the line graph for progress
def show_progress_line_graph(email):
    workout_data = load_workout_data(email)

    if not workout_data:
        messagebox.showinfo("No Data", "No workout data available for this user.")
        return

    # Extract the dates, durations, and calories
    dates = [data[0] for data in workout_data]
    durations = [data[2] for data in workout_data]  # Change to index 2 for duration
    calories = [data[3] for data in workout_data]   # Change to index 3 for calories
    workout_types = [data[1] for data in workout_data]  # Get workout types

    # Create a line graph for calories burned and duration
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(dates, durations, label='Duration (minutes)', color='blue', marker='o')
    ax.plot(dates, calories, label='Calories Burned', color='orange', marker='o')

    ax.set_xlabel('Workout Dates')
    ax.set_ylabel('Value')
    ax.set_title('Calories Burned and Workout Duration')
    ax.legend()
    ax.grid(True)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to handle logout
def logout():
    if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
        messagebox.showinfo("Logout", "You have been logged out.")
        root.quit()  # Close the current app to return to the login screen
        subprocess.Popen(['python', 'Login.py'])  # Launch the login page

# Function to update active page highlight
def set_active(button):
    for btn in nav_buttons:
        btn.configure(fg_color="black", text_color="white")
    button.configure(fg_color="white", text_color="black")

# Hover effect for buttons
def on_hover(button, enter):
    if enter:
        button.configure(fg_color="gray")
    else:
        button.configure(fg_color="black")

# Create the main dashboard window
def create_dashboard(email):
    global root, main_content_frame, progress_frame, recent_workouts_textbox, progress_label, profile_label
    # Initialize custom tkinter
    ctk.set_appearance_mode("light")  # Options: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

    root = ctk.CTk()  # Main window
    root.title("Fitness Tracker Dashboard")
    # Set the window size to full screen
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

    # --- Main layout ---

    # Frame for side navigation
    side_nav_frame = ctk.CTkFrame(root, width=200, corner_radius=0, fg_color="darkgray")
    side_nav_frame.pack(side="left", fill="y")

    # Header Frame (User Profile)
    profile_frame = ctk.CTkFrame(side_nav_frame, height=150, fg_color="black", corner_radius=0)
    profile_frame.pack(fill="x")

    # Add user profile picture (using the same profile icon as the login button)
    profile_picture_icon = ctk.CTkImage(light_image=Image.open("icons/profile.png"), size=(80, 80))
    profile_picture = ctk.CTkLabel(profile_frame, image=profile_picture_icon, text="", width=80, height=80)
    profile_picture.pack(pady=10)

    # Corrected profile label with user name
    profile_label = ctk.CTkLabel(profile_frame, text=email, font=ctk.CTkFont(size=14, weight="bold"), text_color="white")
    profile_label.pack(pady=5)

    # --- Side navigation buttons ---
    global nav_buttons
    nav_buttons = []

    def create_button(text, command, icon=None):
        button = ctk.CTkButton(
            side_nav_frame, text=text, font=ctk.CTkFont(size=14),
            command=lambda: [command(), set_active(button)], fg_color="black", text_color="white",
            image=icon, compound="left"
        )
        button.pack(pady=10, padx=10, fill="x")
        button.bind("<Enter>", lambda event: on_hover(button, True))
        button.bind("<Leave>", lambda event: on_hover(button, False))
        nav_buttons.append(button)
        return button

    # Load icons using CTkImage
    logout_icon = ctk.CTkImage(light_image=Image.open("icons/logout.png"), size=(20, 20))
    workout_icon = ctk.CTkImage(light_image=Image.open("icons/workout.png"), size=(20, 20))
    progress_icon = ctk.CTkImage(light_image=Image.open("icons/progress.png"), size=(20, 20))
    history_icon = ctk.CTkImage(light_image=Image.open("icons/history.png"), size=(20, 20))
    lessons_icon = ctk.CTkImage(light_image=Image.open("icons/workout_lessons.png"), size=(20, 20))
    settings_icon = ctk.CTkImage(light_image=Image.open("icons/workout_lessons.png"), size=(20, 20))

    # Add buttons with active page functionality
    logout_button = create_button("Logout", logout, icon=logout_icon)
    workout_log_button = create_button("Log Workout", lambda: log_workout(email), icon=workout_icon)
    view_progress_button = create_button("View Progress", lambda: show_progress_line_graph(email), icon=progress_icon)
    view_recent_workouts_button = create_button("View Recent Workouts", lambda: load_recent_workouts(email), icon=history_icon)
    workouts_lessons_button = create_button("Workout Lessons", lambda: workout_lessons(email), icon=lessons_icon)
    settings_button = create_button("Settings", lambda: workout_lessons(email), icon=settings_icon)

    # Highlight the login button as the default active
    set_active(logout_button)

    # --- Main content area ---
    main_content_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="white")
    main_content_frame.pack(side="right", expand=True, fill="both")

    # Main content title
    main_content_label = ctk.CTkLabel(main_content_frame, text="Welcome to Your Fitness Tracker", font=ctk.CTkFont(size=24, weight="bold"), text_color="Navy")
    main_content_label.pack(pady=30)

    # Green section for progress display
    progress_frame = ctk.CTkFrame(main_content_frame, fg_color="lightgreen", height=250, width=600, corner_radius=10)
    progress_frame.pack(pady=20)

    # Label for progress section
    progress_label = ctk.CTkLabel(progress_frame, text="Progress Overview", font=ctk.CTkFont(size=20, weight="bold"))
    progress_label.pack(pady=10)

    # Textbox for recent workouts (hidden initially)
    recent_workouts_textbox = ctk.CTkTextbox(progress_frame, height=200, width=600)
    recent_workouts_textbox.pack(pady=10)
    recent_workouts_textbox.pack_forget()  # Hidden initially

def workout_lessons(email):
    subprocess.Popen([sys.executable, 'exercises.py', email])  # Ensure the email is passed if needed

def log_workout(email):
    subprocess.Popen([sys.executable, 'logworkout.py', email])  # Ensure the email is passed if needed

def load_recent_workouts(email):
    """Load and display recent workouts for the user."""
    recent_workouts_textbox.pack()  # Show the textbox

    # Hide the progress label when viewing recent workouts
    progress_label.pack_forget()

    recent_workouts_textbox.delete('1.0', ctk.END)  # Clear existing text
    workout_data = load_workout_data(email)

    if workout_data:
        for date, workout_type, duration, calories in workout_data:
            recent_workouts_textbox.insert(ctk.END, f"Date: {date.strftime('%Y-%m-%d')}, Type: {workout_type}, Duration: {duration} mins, Calories: {calories}\n")
    else:
        recent_workouts_textbox.insert(ctk.END, "No recent workouts found.")

# Start the application
if __name__ == "__main__":
    # Expecting the email to be passed as an argument
    if len(sys.argv) > 1:
        email = sys.argv[1]
        create_dashboard(email)
    else:
        print("Email not provided.")

    root.mainloop()
