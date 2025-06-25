import customtkinter as ctk

# Fadil message
# Abdullah message

# Set appearance and theme (optional)
ctk.set_appearance_mode("System")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Theme colors: "blue", "green", "dark-blue"

# Create main window
root = ctk.CTk()

# Set window size and title
root.geometry("1020x768")
root.title("CustomTkinter Multi-Screen App")

# Create both frames (screens)
home_frame = ctk.CTkFrame(master=root)
settings_frame = ctk.CTkFrame(master=root)

# --- Home Screen ---
def show_home():
    settings_frame.pack_forget()
    home_frame.pack(fill="both", expand=True)

home_label = ctk.CTkLabel(home_frame, text="Home Screen", font=("Arial", 20))
home_label.pack(pady=30)

home_button = ctk.CTkButton(home_frame, text="Go to Settings", command=lambda:show_settings())
home_button.pack()

# --- Settings Screen ---
def show_settings():
    home_frame.pack_forget()
    settings_frame.pack(fill="both", expand=True)

settings_label = ctk.CTkLabel(settings_frame, text="Settings Screen", font=("Arial", 20))
settings_label.pack(pady=30)

settings_button = ctk.CTkButton(settings_frame, text="Back to Home", command=show_home)
settings_button.pack()

# Show home screen initially
show_home()

# Run the app
root.mainloop()
