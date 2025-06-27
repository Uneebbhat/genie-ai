import customtkinter as ctk

# --- Setup appearance and theme ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#  Create main window 
root = ctk.CTk()
root.geometry("400x450")
root.title("Genie AI")

#  Creating the main login frame 
login_frame = ctk.CTkFrame(master=root, corner_radius=10)
login_frame.pack(expand=True, padx=20, pady=20)

#  Login Functions
def on_login():
    print("Login clicked:", email_entry.get(), password_entry.get())

def on_signup():
    print("Signup clicked")

# --- Build Login UI ---
def show_login():
    # Title
    title_label = ctk.CTkLabel(login_frame, text="Hello, Login to Genie AI", font=("", 20))
    title_label.pack(pady=(10, 30))

    # Email
    global email_entry
    email_entry = ctk.CTkEntry(login_frame, placeholder_text="Email", width=300)
    email_entry.pack(pady=(0, 8), padx=10)  # Top=0, Bottom=8

    # Password
    global password_entry
    password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=300)
    password_entry.pack(pady=(0, 8), padx=10)

    # Login Button
    login_btn = ctk.CTkButton(login_frame, text="Login", command=on_login, width=300)
    login_btn.pack(pady=(0, 8), padx=10)

    # OR label
    or_label = ctk.CTkLabel(login_frame, text="OR")
    or_label.pack(pady=(8, 16))  # 8 above, 16 below

    # Signup Button
    signup_btn = ctk.CTkButton(
        login_frame,
        text="Signup",
        command=on_signup,
        fg_color=None,
        border_color="#0078D7",
        text_color="#FFFFFF",
        width=300
    )
    signup_btn.pack(pady=(0, 0), padx=10)

#  Call login screen setup 
show_login()

# --- Start the GUI loop ---
root.mainloop()