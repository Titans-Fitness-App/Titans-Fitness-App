import customtkinter as ctk
from tkinter import messagebox
import subprocess  # Import subprocess to run the other script
from PIL import Image

DATA_FILE = "FitnessData.txt"
# customkinter.set_appearance_mode("darker")
# customkinter.set_default_theme("darke-blue")


class FitnessApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Measurements")
        self.geometry("800x600")

        self.workouts = []

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = ctk.CTkLabel(self, text="Measurements", font=("Helvetica", 24))
        title_label.pack(pady=30)

        # Label for the weight
        weight_label = ctk.CTkLabel(self, text="Enter your weight (kg)", font=("Helvetica", 14))
        weight_label.pack(pady=10)

        # Entry for weight
        self.weight_entry = ctk.CTkEntry(self, placeholder_text="Weight in kg", corner_radius=10, width=300)
        self.weight_entry.pack(pady=10)

        # Label for the height
        height_label = ctk.CTkLabel(self, text="Enter your height (m)", font=("Helvetica", 14))
        height_label.pack(pady=10)

        # Entry for height
        self.height_entry = ctk.CTkEntry(self, placeholder_text="Height in meters", corner_radius=10, width=300)
        self.height_entry.pack(pady=10)

        # Calculate BMI Button
        calculate_button = ctk.CTkButton(self, text="Continue", command=self.calculate_bmi, corner_radius=10)
        calculate_button.pack(pady=20, ipadx=10, ipady=5)

        # Exit Button
        exit_button = ctk.CTkButton(self, text="Exit", command=self.quit, corner_radius=10, fg_color="red")
        exit_button.pack(pady=10, ipadx=10, ipady=5)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

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

            # Store the result
            self.workouts.append({
                "weight": weight,
                "height": height,
                "bmi": bmi,
                "category": category
            })

            # Save the result to a file
            with open(DATA_FILE, "a") as file:
                file.write(f"Weight: {weight} kg, Height: {height} m, BMI: {bmi:.2f}, Category: {category}\n")

            # Show the result to the user
            messagebox.showinfo("BMI Result", f"Your BMI is {bmi:.2f} ({category})")

            # Open schedule.py immediately after the message box
            self.open_schedule()

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def open_schedule(self):
        # Use subprocess to run schedule.py
        subprocess.Popen(['python', 'schedule.py'])  # Adjust this line as needed for your environment
        self.quit()  # Close the current app

if __name__ == "__main__":
    app = FitnessApp()
    app.mainloop()
