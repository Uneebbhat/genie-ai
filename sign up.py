import customtkinter as ctk

# --- Setup appearance and theme ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# --- Create main window ---
root = ctk.CTk()
root.geometry("400x450")
root.title("Genie AI")

# --- Create frames ---
signup_frame = ctk.CTkFrame(master=root, corner_radius=10)
signup_frame.pack(expand=True, padx=20, pady=20)

login_frame = ctk.CTkFrame(master=root, corner_radius=10)
# (You can pack login_frame later if needed)

# --- Login Function ---
def on_login():
    print("Login clicked:", email_entry.get(), password_entry.get())

# --- Build Login UI ---
def show_login():
    # Title
    title_label = ctk.CTkLabel(login_frame, text="Hello, Login to Genie AI", font=("", 20))
    title_label.pack(pady=(10, 30))

# --- Sign-Up Function ---
def on_signup():
    print("Signup clicked:")
    print("Name:", name_entry.get())
    print("Email:", email_entry.get())
    print("Password:", password_entry.get())

# --- Show Sign-Up UI ---
def show_signup():
    # Title
    title_label = ctk.CTkLabel(signup_frame, text="Hello, Sign Up to Genie AI", font=("", 20))
    title_label.pack(pady=(20, 0))  # Top padding from frame

    # Name Input
    global name_entry
    name_entry = ctk.CTkEntry(signup_frame, placeholder_text="Name", width=300)
    name_entry.pack(pady=(32, 0), padx=10)

    # Email Input
    global email_entry
    email_entry = ctk.CTkEntry(signup_frame, placeholder_text="Email", width=300)
    email_entry.pack(pady=(8, 0), padx=10)

    # Password Input
    global password_entry
    password_entry = ctk.CTkEntry(signup_frame, placeholder_text="Password", show="*", width=300)
    password_entry.pack(pady=(8, 0), padx=10)

    # Sign Up Button
    signup_btn = ctk.CTkButton(signup_frame, text="Sign Up", command=on_signup, width=300)
    signup_btn.pack(pady=(16, 0), padx=10)

    # OR label
    or_label = ctk.CTkLabel(signup_frame, text="OR")
    or_label.pack(pady=(8, 16))  # 8 above, 16 below

    # Login Button
    login_btn = ctk.CTkButton(signup_frame, text="Login", command=on_login, width=300)
    login_btn.pack(pady=(0, 8), padx=10)

# --- Load Sign-Up UI ---
show_signup()

# --- Start the GUI ---
root.mainloop()
