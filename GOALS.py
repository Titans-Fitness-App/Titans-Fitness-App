import customtkinter as ctk
from tkinter import messagebox, Canvas, Scrollbar
from PIL import ImageTk, Image
import subprocess
import sys

# Function to handle saving fitness data
def save_fitness_data(data, email):
    try:
        with open('FitnessTrackerData.txt', 'a') as file:
            file.write(f"Email: {email}\n{data}\n")
    except Exception as e:
        print(f"Failed to save data: {e}")
 
# Function to save fitness goal and selected exercises
def save_fitness_goal_and_exercises(goal, focus_area, email):
    if focus_area:
        data = f"Goal: {goal} | Exercises: {', '.join(focus_area)}"
        save_fitness_data(data, email)
        messagebox.showinfo("Success", "Fitness goal and exercises saved successfully!")
    else:
        messagebox.showwarning("Input Error", "Please select at least one exercise.")

# Function to display exercises for the selected goal
def display_exercises(goal, email):
    def save_exercise_selection():
        focus_area = [exercise_var.get() for exercise_var, checkbox in exercise_checkboxes if checkbox.get() == 1]
        save_fitness_goal_and_exercises(goal, focus_area, email)
        subprocess.Popen(['python', 'measurements.py', email])  # Pass the user's email
        quit()  # Close the current app

    # Clear current window
    for widget in root.winfo_children():
        widget.destroy()

    # Create a frame for exercises
    exercise_frame = ctk.CTkFrame(root)
    exercise_frame.pack(fill="both", expand=True)

    # Create a canvas and scrollbar for scrolling
    canvas = Canvas(exercise_frame)
    scrollbar = Scrollbar(exercise_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    exercise_checkboxes = []

    exercises_dict = {
        "Weight Loss": [
            ("Legs", r"img/Plank.jpg"),
            ("Back", r"img/Squat 1.jpg"),
            ("Shoulders", r"img/Squat 1.jpg"),
            ("Arms", r"img/Squat 1.jpg"),
            ("Abs", r"img/Squat 1.jpg"),
            ("Butt", r"img/Squat 1.jpg"),
            ("Chest", r"img/Squat 1.jpg"),
            ("Full body", r"img/Squat 1.jpg"),
        ],
        "Muscle Gain": [
           ("Legs", r"img/Plank.jpg"),
            ("Back", r"img/Squat 1.jpg"),
            ("Shoulders", r"img/Squat 1.jpg"),
            ("Arms", r"img/Squat 1.jpg"),
            ("Abs", r"img/Squat 1.jpg"),
            ("Butt", r"img/Squat 1.jpg"),
            ("Chest", r"img/Squat 1.jpg"),
            ("Full body", r"img/Squat 1.jpg"),
          
        ],
        "Body Shape": [
            ("Legs", r"img/Plank.jpg"),
            ("Back", r"img/Squat 1.jpg"),
            ("Shoulders", r"img/Squat 1.jpg"),
            ("Arms", r"img/Squat 1.jpg"),
            ("Abs", r"img/Squat 1.jpg"),
            ("Butt", r"img/Squat 1.jpg"),
            ("Chest", r"img/Squat 1.jpg"),
            ("Full body", r"img/Squat 1.jpg"),
        ],
        "Cardio": [
            ("Legs", r"img/Plank.jpg"),
            ("Back", r"img/Squat 1.jpg"),
            ("Shoulders", r"img/Squat 1.jpg"),
            ("Arms", r"img/Squat 1.jpg"),
            ("Abs", r"img/Squat 1.jpg"),
            ("Butt", r"img/Squat 1.jpg"),
            ("Chest", r"img/Squat 1.jpg"),
            ("Full body", r"img/Squat 1.jpg"),
        ]
    }

    # Get available frame dimensions
    frame_width = root.winfo_width()
    frame_height = root.winfo_height()

    row = 0
    for exercise, image_path in exercises_dict[goal]:
        exercise_var = ctk.StringVar(value=exercise)
        checkbox = ctk.IntVar()

        # Load image using PIL
        try:
            exercise_image = Image.open(image_path)
            original_width, original_height = exercise_image.size
            
            # Resize while maintaining aspect ratio
            new_width = int(frame_width * 0.95)  # Use 95% of the frame width
            aspect_ratio = original_width / original_height
            new_height = int(new_width / aspect_ratio)

            # Limit height to a percentage of frame height
            max_height = int(frame_height * 0.4)  # Use 40% of the frame height
            if new_height > max_height:
                new_height = max_height
                new_width = int(max_height * aspect_ratio)

            # Resize the image
            exercise_image = exercise_image.resize((new_width, new_height), Image.LANCZOS)
            photo = ctk.CTkImage(light_image=exercise_image, dark_image=exercise_image)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            continue

        # Create a full-width label for the image
        image_label = ctk.CTkLabel(scrollable_frame, image=photo, text="")
        image_label.image = photo  # Prevent garbage collection
        image_label.grid(row=row, column=0, padx=0, pady=0, sticky="nsew")

        # Add checkbox for exercise selection below the image
        cb = ctk.CTkCheckBox(scrollable_frame, text=exercise, variable=checkbox, font=("Helvetica", 18), text_color="black", fg_color="#ff8c00", hover_color="#ffdb58")
        cb.grid(row=row + 1, column=0, padx=0, pady=(0, 10), sticky="nsew")  # Add some space below the checkbox
        
        exercise_checkboxes.append((exercise_var, checkbox))  # Store for later use
        
        # Update grid position
        row += 2  # Move down two rows for the next image and checkbox

    # Configure grid weight for stretching
    scrollable_frame.grid_rowconfigure((0, 1), weight=1)

    # Save and Back buttons at the bottom
    button_frame = ctk.CTkFrame(root, fg_color="white")
    button_frame.pack(side="bottom", pady=20)

    ctk.CTkButton(button_frame, text="Save", command=save_exercise_selection, font=("Helvetica", 18), width=200, height=40, fg_color="#00bfff", hover_color="#add8e6").pack(side="left", padx=10)
    ctk.CTkButton(button_frame, text="Back", command=reset_to_goal_screen, font=("Helvetica", 18), width=200, height=40, fg_color="#ffa500", hover_color="#ffcc99").pack(side="right", padx=10)

# Function to display the goal selection screen
def reset_to_goal_screen():
    for widget in root.winfo_children():
        widget.destroy()

    # Display background image
    background_label = ctk.CTkLabel(root, image=background_image, text="")
    background_label.place(relwidth=1, relheight=1)

    # Create goal selection buttons
    ctk.CTkLabel(root, text="Select Your Fitness Goal", font=("Helvetica", 28, "bold"), text_color="black").pack(pady=30)
    ctk.CTkButton(root, text="Weight Loss", command=lambda: display_exercises("Weight Loss", email), font=("Helvetica", 20), width=300, height=60, fg_color="#ff8c00", hover_color="#ffdb58", text_color="white").pack(pady=15)
    ctk.CTkButton(root, text="Muscle Gain", command=lambda: display_exercises("Muscle Gain", email), font=("Helvetica", 20), width=300, height=60, fg_color="#00bfff", hover_color="#add8e6", text_color="white").pack(pady=15)
    ctk.CTkButton(root, text="Body Shape", command=lambda: display_exercises("Body Shape", email), font=("Helvetica", 20), width=300, height=60, fg_color="#32cd32", hover_color="#98fb98", text_color="white").pack(pady=15)
    ctk.CTkButton(root, text="Cardio", command=lambda: display_exercises("Cardio", email), font=("Helvetica", 20), width=300, height=60, fg_color="#ff4500", hover_color="#ff6347", text_color="white").pack(pady=15)

# Main application window
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Goal Setting and Focus")

# Make the window full-screen and resizable
root.state('zoomed')
root.resizable(True, True)

# Load and display the background image
try:
    original_image = Image.open(r"img/Background image.jpg")  # Update to your background image path
    background_image = ctk.CTkImage(light_image=original_image, dark_image=original_image, size=(root.winfo_screenwidth(), root.winfo_screenheight()))
except Exception as e:
    print(f"Error loading background image: {e}")

# Assuming email is passed via command line arguments
if len(sys.argv) > 1:
    email = sys.argv[1]
    reset_to_goal_screen()
else:
    print("Email not provided")

root.mainloop()
