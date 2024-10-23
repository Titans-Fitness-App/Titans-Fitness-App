import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import sys

# Set up the theme and appearance
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("dark-blue")  

class FitnessTrackerApp(ctk.CTk):
    def __init__(self, email):
        super().__init__()

        self.email = email  # Store the user's email passed from the previous page
        self.selected_fitness_goal = None  
        self.selected_focus_areas = []  # To store multiple focus areas
        self.checkboxes = {}

        self.title("Goal Setting and Focus")
        
        # Set initial window size to maximized using geometry
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        
        # Load background image
        self.background_image = Image.open("./EZ bar biceps curl.jpg")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.background_image = self.background_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_image_ctk = ctk.CTkImage(self.background_image, size=(screen_width, screen_height))

        # Main menu - Fitness Goals
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.create_main_menu()

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
        back_image = Image.open("./back-button.png").resize((30, 30), Image.LANCZOS)  # Update with your icon path
        self.back_icon = ctk.CTkImage(back_image, size=(30, 30))
        back_button = ctk.CTkButton(self.main_frame, image=self.back_icon, text="", command=self.create_main_menu, width=40)
        back_button.pack(side="top", anchor="nw", padx=10, pady=10)

        # Label for focus area
        self.label = ctk.CTkLabel(self.main_frame, text=f"Select Focus Areas for {goal}", font=("Arial", 40))
        self.label.pack(pady=40)

        # Focus area checkboxes
        focus_areas = ['Legs', 'Back', 'Shoulders', 'Arms', 'Abs', 'Butt', 'Chest', 'Full Body']
        for area in focus_areas:
            var = ctk.BooleanVar()  # Variable to hold checkbox value (True/False)
            checkbox = ctk.CTkCheckBox(self.main_frame, text=area, font=("Arial", 28), variable=var, command=lambda a=area, v=var: self.update_selection(a, v))
            checkbox.pack(pady=10)
            self.checkboxes[area] = var  # Store checkbox variable for later use

        # Load arrow image for the button (replace with the correct path to your arrow image)
        arrow_image = Image.open("img/arrow.png").resize((30, 30))  # Ensure this is the correct path
        arrow_image_tk = ImageTk.PhotoImage(arrow_image)

        # Continue button to proceed after selection with arrow next to text
        continue_button = ctk.CTkButton(self.main_frame, text="Continue", font=("Arial", 28), command=self.continue_to_next_page,
                                        image=arrow_image_tk, compound="right")  # Arrow positioned to the right
        continue_button.pack(pady=30)

    def update_selection(self, area, var):
        if var.get():
            self.selected_focus_areas.append(area)  # Add to list if checked
        else:
            self.selected_focus_areas.remove(area)  # Remove from list if unchecked

    def continue_to_next_page(self):
        # Save the selected goal, focus areas, and email address
        if self.selected_focus_areas:
            with open("FitnessTrackerData.txt", "a") as file:
                file.write(f"Email: {self.email}, Fitness Goal: {self.selected_fitness_goal}, Focus Areas: {', '.join(self.selected_focus_areas)}\n")
            print(f"Saved: Email - {self.email}, Fitness Goal - {self.selected_fitness_goal}, Focus Areas - {', '.join(self.selected_focus_areas)}")
            
            # Navigate to the measurements screen
            subprocess.Popen(['python', 'measurements.py', self.email])  # Pass the email to the measurements screen
            #self.destroy()  # Close the current window
        else:
            print("No focus areas selected.")

# Create and run the application
if __name__ == "__main__":
    user_email = sys.argv[1]  # Retrieve the email passed from the previous page
    app = FitnessTrackerApp(email=user_email)
    app.mainloop()
