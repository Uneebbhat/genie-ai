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
def show_signup() -> None:
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
