import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
from PIL import Image, ImageTk, ImageFilter

DATA_FILE = "FitnessTrackerData.txt"

class FitnessApp(ctk.CTk):
    def __init__(self, email):
        super().__init__()
        self.title("Titans Fitness Club - Measurements")
        # Set the window size to full screen
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        # Store email
        self.email = email  

        # Load and blur background image
        self.bg_image = Image.open("./gym1.jpg")  # Replace with your image file path
        self.bg_image_blur = self.bg_image.filter(ImageFilter.GaussianBlur(radius=5))  # Apply Gaussian blur
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image_blur)

        # Load arrow image for buttons
        self.arrow_image = ImageTk.PhotoImage(Image.open("./arrow.png").resize((20, 20)))

        # Create background label with the blurred image
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image_tk)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ** Add an image to the top-left corner **
        # Load the image you want to place at the top-left corner
        self.logo_image = Image.open("./back-icon.png").resize((50, 50))  # Adjust size as needed
        self.logo_image_tk = ImageTk.PhotoImage(self.logo_image)

        # Create label for the logo image and place it at the top-left
        self.logo_label = ctk.CTkLabel(self, image=self.logo_image_tk, text="")  # Empty text for just the image
        self.logo_label.place(x=20, y=20)  # Adjust the x, y coordinates for positioning

        # Bind click event to the logo label
        self.logo_label.bind("<Button-1>", self.go_back)

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = ctk.CTkLabel(self, text="Measurements", font=("Helvetica", 24))
        title_label.pack(pady=30)

        # Create the main frame and center it, with increased width
        main_frame = ctk.CTkFrame(self, fg_color="#737371", width=800)  # Increased width
        main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

        # Gender selection
        gender_label = ctk.CTkLabel(main_frame, text="Select your gender", text_color="white", font=("Helvetica", 14))
        gender_label.pack(pady=10)

        self.gender_var = ctk.StringVar(value="Male")  # Default to Male
        male_radio = ctk.CTkRadioButton(main_frame, text_color="white", text="Male", variable=self.gender_var, value="Male", corner_radius=36)
        female_radio = ctk.CTkRadioButton(main_frame, text="Female", text_color="white", variable=self.gender_var, value="Female", corner_radius=36)
        male_radio.pack(pady=5)
        female_radio.pack(pady=5)

        # Weight entry
        weight_label = ctk.CTkLabel(main_frame, text_color="white", text="Enter your weight (kg)", font=("Helvetica", 14))
        weight_label.pack(pady=10)

        self.weight_entry = ctk.CTkEntry(main_frame, placeholder_text="Weight in kg", corner_radius=10, width=300)
        self.weight_entry.pack(pady=10)

        # Height entry
        height_label = ctk.CTkLabel(main_frame, text="Enter your height (m)", text_color="white", font=("Helvetica", 14))
        height_label.pack(pady=10)

        self.height_entry = ctk.CTkEntry(main_frame, placeholder_text="Height in meters", corner_radius=10, width=300)
        self.height_entry.pack(pady=10)

        # Age entry
        age_label = ctk.CTkLabel(main_frame, text="Enter your age", text_color="white", font=("Helvetica", 14))
        age_label.pack(pady=10)

        self.age_entry = ctk.CTkEntry(main_frame, placeholder_text="Age", corner_radius=10, width=300)
        self.age_entry.pack(pady=10)

        # Continue button with arrow
        continue_button = ctk.CTkButton(main_frame, text="Continue", image=self.arrow_image, compound="right", command=self.calculate_bmi, corner_radius=10)
        continue_button.pack(pady=20)

    def go_back(self, event):
        # Close the current application and return to the previous screen
        self.destroy()  # This assumes you want to close this window, returning to the previous one

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            gender = self.gender_var.get()
            age = self.age_entry.get()

            if height <= 0:
                raise ValueError("Height must be greater than 0")

            # Calculate BMI
            bmi = weight / (height ** 2)

            # Categorize the BMI result
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
            elif 25 <= bmi < 30:
                category = "Overweight"
            else:
                category = "Obesity"

            # Save the result to a file along with the email
            with open(DATA_FILE, "a") as file:
                file.write(f"Email: {self.email}, Weight: {weight} kg, Height: {height} m, BMI: {bmi:.2f}, Category: {category}, Gender: {gender}, Age: {age} |\n")

            # Show the result to the user
            messagebox.showinfo("BMI Result", f"Your BMI is {bmi:.2f} ({category})")

            # Open logworkout.py, passing the email
            self.open_logworkout()

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def open_logworkout(self):
        # Use subprocess to run logworkout.py and pass the email
        subprocess.Popen(['python', 'logworkout.py', self.email])  
        self.destroy()

if __name__ == "__main__": 
    if len(sys.argv) > 1 and sys.argv[1]:  # Check if email is provided
        user_email = sys.argv[1]
    else:
        raise ValueError("No email provided. Please register first.")  # Raise an error for clarity

    app = FitnessApp(user_email)
    app.mainloop()
