# main.py
from tkinter import YES
import customtkinter as ctk
import requests

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
chat_frame = ctk.CTkFrame(master=root, corner_radius=10)
settings_frame = ctk.CTkFrame(master=root, corner_radius=10)

# Pack the login frame first; the sign-up frame will be packed on demand
login_frame.pack(expand=True, padx=20, pady=20)

# ── Callback helpers ───────────────────────────────────────────────────────────
def clear_frame(frame: ctk.CTkFrame) -> None:
    """Destroy all child widgets so we can rebuild the view from scratch."""
    for child in frame.winfo_children():
        child.destroy()


def handle_signup(name: str, email: str, password: str, message_label, signup_frame) -> None:
    try:
        response = requests.post(
            "http://127.0.0.1:5000/signup",
            json={"username": name, "email": email, "password": password}
        )
        data = response.json()
        if response.status_code == 201:
            message_label.configure(text="Signup successful! Redirecting...", text_color="green")
            signup_frame.after(1000, show_chat)
        else:
            message_label.configure(text=data.get("error", "Signup failed."), text_color="red")
    except Exception as e:
        message_label.configure(text=f"Error: {e}", text_color="red")

# ── UI-builder: Login screen ───────────────────────────────────────────────────
def show_chat():
    # Hide all other frames
    for frame in [login_frame, signup_frame, settings_frame]:
        frame.pack_forget()
    clear_frame(chat_frame)
    chat_frame.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(chat_frame, text="Welcome to Genie AI Chat!", font=("Arial", 20)).pack(pady=20)
    # Add your chat widgets here


def show_login():
    # Hide all frames
    for frame in [signup_frame, chat_frame, settings_frame]:
        frame.pack_forget()
    clear_frame(login_frame)
    login_frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(login_frame, text="Login", font=("Arial", 20)).pack(pady=20)

    email_entry = ctk.CTkEntry(login_frame, placeholder_text="Email", width=300)
    email_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=300)
    password_entry.pack(pady=10)

    message_label = ctk.CTkLabel(login_frame, text="", font=("Arial", 12))
    message_label.pack(pady=10)

    def login():
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not email or not password:
            message_label.configure(text="Both fields are required.", text_color="red")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/login",
                json={"email": email, "password": password}
            )
            data = response.json()

            if response.status_code == 200:
                message_label.configure(text="Login successful! Redirecting...", text_color="green")
                login_frame.after(1000, show_chat)
            else:
                message_label.configure(text=data.get("error", "Login failed."), text_color="red")
        except Exception as e:
            message_label.configure(text=f"Error: {e}", text_color="red")

    ctk.CTkButton(login_frame, text="Login", command=login, width=300).pack(pady=10)
    ctk.CTkLabel(login_frame, text="OR").pack(pady=(8, 8))
    ctk.CTkButton(login_frame, text="Go to Signup", command=lambda: show_signup(), width=300).pack(pady=(0, 8))


# Start with login screen
show_login()

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
    signup_frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(signup_frame, text="Sign Up", font=("Arial", 20)).pack(pady=20)

    name_entry = ctk.CTkEntry(signup_frame, placeholder_text="Name", width=300)
    name_entry.pack(pady=(8, 0), padx=10)

    email_entry = ctk.CTkEntry(signup_frame, placeholder_text="Email", width=300)
    email_entry.pack(pady=(8, 0), padx=10)

    password_entry = ctk.CTkEntry(signup_frame, placeholder_text="Password", show="*", width=300)
    password_entry.pack(pady=(8, 0), padx=10)

    message_label = ctk.CTkLabel(signup_frame, text="", font=("Arial", 12))
    message_label.pack(pady=10)

    ctk.CTkButton(
        signup_frame,
        text="Sign Up",
        command=lambda: handle_signup(
            name_entry.get(), email_entry.get(), password_entry.get(), message_label, signup_frame
        ),
        width=300
    ).pack(pady=(16, 0), padx=10)

    ctk.CTkLabel(signup_frame, text="OR").pack(pady=(8, 8))
    ctk.CTkButton(
        signup_frame,
        text="Go to Login",
        command=show_login,
        width=300
    ).pack(pady=(0, 8), padx=10)
# ── Kick-start with the Login view ─────────────────────────────────────────────
show_login()
root.mainloop()
