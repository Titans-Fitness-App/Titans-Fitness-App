import customtkinter as ctk
import tkinter.messagebox as tkmb
import subprocess

# Set the appearance mode and default color theme
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

# Create the main app window
app = ctk.CTk()
app.title("Titans Fitness Club - Login")

# Set the window size to full screen
app.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}+0+0")

# Create a main frame to hold all widgets with a matching background
main_frame = ctk.CTkFrame(app, fg_color="dark gray")
main_frame.pack(expand=True, fill="both")

# Function to get user data from the file
def get_user_data():
    user_data = {}
    try:
        with open("FitnessTrackerData.txt", "r") as file:
            for line in file:
                # Split by commas
                parts = line.strip().split(", ")
                if len(parts) == 3:  # Ensure correct number of elements
                    try:
                        # Split by ": " to get key-value pairs
                        name = parts[0].split(": ")[1]
                        email = parts[1].split(": ")[1]
                        password = parts[2].split(": ")[1]
                        user_data[email] = {"name": name, "password": password}
                    except IndexError:
                        print(f"Error parsing line: {line}. Skipping.")
                else:
                    print(f"Line format incorrect: {line}. Skipping.")
    except FileNotFoundError:
        print("FitnessTrackerData.txt not found. No user data available.")
    
    return user_data

# Login function
def login():
    email = username_entry.get()
    password = password_entry.get()

    # Load the user data from the file
    users = get_user_data()

    # Check if the email exists and password matches
    if email in users:
        if users[email]["password"] == password:
            tkmb.showinfo(title="Login Successful", message=f"Welcome {users[email]['name']}!")
            # Pass the email to the dashboard page
            subprocess.Popen(['python', 'dashboard1.py', email])  # Pass the user's email
            app.destroy()  # Close the current app
        else:
            tkmb.showerror(title="Login Failed", message="Invalid password")
    else:
        tkmb.showerror(title="Login Failed", message="Invalid email")

# Function to open the registration window
def open_registration_window():
    import Register  # Import the Register module
    Register.open_registration_window(app)

# Label for the app title
label = ctk.CTkLabel(main_frame, text="Login", font=("Helvetica", 24, "bold"), text_color="black")
label.pack(pady=20)

# Email entry
username_entry = ctk.CTkEntry(main_frame, placeholder_text="Username (email)", width=300)
username_entry.pack(pady=12)

# Password entry
password_entry = ctk.CTkEntry(main_frame, placeholder_text="Password", show="*", width=300)
password_entry.pack(pady=12)

# Login button
login_button = ctk.CTkButton(main_frame, text="Login", command=login, width=300, fg_color="black", text_color="white")
login_button.pack(pady=12)

# Forgot password label
forgot_password = ctk.CTkLabel(main_frame, text="Forgot Password?", cursor="hand2", text_color="white")
forgot_password.pack(pady=12)

# Register label
register_label = ctk.CTkLabel(main_frame, text="Don't have an account? Register here", cursor="hand2", text_color="white")
register_label.pack(pady=12)
register_label.bind("<Button-1>", lambda e: open_registration_window())

# Start the application
app.mainloop()
