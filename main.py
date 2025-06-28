# main.py
import customtkinter as ctk

# ── Global appearance ──────────────────────────────────────────────────────────
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# ── Main window ────────────────────────────────────────────────────────────────
root = ctk.CTk()
root.geometry("400x450")
root.title("Genie AI")

# ── Re-usable frames (we swap them in and out) ─────────────────────────────────
login_frame  = ctk.CTkFrame(master=root, corner_radius=10)
signup_frame = ctk.CTkFrame(master=root, corner_radius=10)

# Pack the login frame first; the sign-up frame will be packed on demand
login_frame.pack(expand=True, padx=20, pady=20)

# ── Callback helpers ───────────────────────────────────────────────────────────
def clear_frame(frame: ctk.CTkFrame) -> None:
    """Destroy all child widgets so we can rebuild the view from scratch."""
    for child in frame.winfo_children():
        child.destroy()

# ── Business-logic actions (no UI code here) ───────────────────────────────────
def handle_login(email: str, password: str) -> None:
    # TODO: Replace print() with real authentication in production
    print("Login clicked:", email, password)

def handle_signup(name: str, email: str, password: str) -> None:
    # TODO: Replace print() with persistence / API call
    print("Signup clicked:")
    print("Name:", name)
    print("Email:", email)
    print("Password:", password)

# ── UI-builder: Login screen ───────────────────────────────────────────────────
def show_login() -> None:
    signup_frame.pack_forget()                 # Hide the other frame (if visible)
    clear_frame(login_frame)                   # Start with a clean slate
    login_frame.pack(expand=True, padx=20, pady=20)

    # Title
    ctk.CTkLabel(
        login_frame,
        text="Hello, Login to Genie AI",
        font=("", 20)
    ).pack(pady=(10, 30))

    # Email
    email_entry = ctk.CTkEntry(login_frame, placeholder_text="Email", width=300)
    email_entry.pack(pady=(0, 8), padx=10)

    # Password
    password_entry = ctk.CTkEntry(
        login_frame, placeholder_text="Password", show="*", width=300
    )
    password_entry.pack(pady=(0, 8), padx=10)

    # Login button
    ctk.CTkButton(
        login_frame,
        text="Login",
        command=lambda: handle_login(email_entry.get(), password_entry.get()),
        width=300
    ).pack(pady=(0, 8), padx=10)

    # OR label
    ctk.CTkLabel(login_frame, text="OR").pack(pady=(8, 16))

    # Switch-to-Sign-Up button
    ctk.CTkButton(
        login_frame,
        text="Signup",
        command=show_signup,
        fg_color=None,
        border_color="#0078D7",
        text_color="#FFFFFF",
        width=300
    ).pack(pady=(0, 0), padx=10)

# ── UI-builder: Sign-Up screen ────────────────────────────────────────────────
def show_signup():
    chat_frame.pack_forget()
    settings_frame.pack_forget()
    signup_frame = ctk.CTkFrame(master=root)
    signup_frame.pack(fill="both", expand=True)

    ctk.CTkLabel(signup_frame, text="Sign Up", font=("Arial", 20)).pack(pady=20)

    username_entry = ctk.CTkEntry(signup_frame, placeholder_text="Username")
    username_entry.pack(pady=10)
    email_entry = ctk.CTkEntry(signup_frame, placeholder_text="Email")
    email_entry.pack(pady=10)
    password_entry = ctk.CTkEntry(signup_frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=10)

    message_label = ctk.CTkLabel(signup_frame, text="", font=("Arial", 12))
    message_label.pack(pady=10)

    def signup():
        username = username_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not email or not password:
            message_label.configure(text="All fields are required.", text_color="red")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/signup",
                json={"username": username, "email": email, "password": password}
            )
            data = response.json()

            if response.status_code == 201:
                message_label.configure(text="Signup successful! Redirecting...", text_color="green")
                signup_frame.after(1000, lambda: [signup_frame.pack_forget(), show_login()])
            else:
                message_label.configure(text=data.get("error", "Signup failed."), text_color="red")
        except Exception as e:
            message_label.configure(text=f"Error: {e}", text_color="red")

    ctk.CTkButton(signup_frame, text="Sign Up", command=signup).pack(pady=10)
    ctk.CTkButton(signup_frame, text="Go to Login", command=lambda: [signup_frame.pack_forget(), show_login()]).pack(pady=5)
    login_frame.pack_forget()                  # Hide the login frame
    clear_frame(signup_frame)
    signup_frame.pack(expand=True, padx=20, pady=20)

    # Title
    ctk.CTkLabel(
        signup_frame,
        text="Hello, Sign Up to Genie AI",
        font=("", 20)
    ).pack(pady=(20, 0))

    # Name
    name_entry = ctk.CTkEntry(signup_frame, placeholder_text="Name", width=300)
    name_entry.pack(pady=(32, 0), padx=10)

    # Email
    email_entry = ctk.CTkEntry(signup_frame, placeholder_text="Email", width=300)
    email_entry.pack(pady=(8, 0), padx=10)

    # Password
    password_entry = ctk.CTkEntry(
        signup_frame, placeholder_text="Password", show="*", width=300
    )
    password_entry.pack(pady=(8, 0), padx=10)

    # Sign-Up button
    ctk.CTkButton(
        signup_frame,
        text="Sign Up",
        command=lambda: handle_signup(
            name_entry.get(), email_entry.get(), password_entry.get()
        ),
        width=300
    ).pack(pady=(16, 0), padx=10)

    # OR label
    ctk.CTkLabel(signup_frame, text="OR").pack(pady=(8, 16))

    # Switch-to-Login button
    ctk.CTkButton(
        signup_frame,
        text="Login",
        command=show_login,
        width=300
    ).pack(pady=(0, 8), padx=10)
# ── Kick-start with the Login view ─────────────────────────────────────────────
show_login()
root.mainloop()
