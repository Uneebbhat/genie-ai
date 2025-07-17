import customtkinter as ctk
import requests
import datetime

# ----------------------------- UI Settings -----------------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")  # Optional: try 'dark-blue', 'green'

# ----------------------------- Global Constants -----------------------------
FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_SUBTITLE = ("Segoe UI", 16, "bold")
FONT_NORMAL = ("Segoe UI", 13)
FONT_BUTTON = ("Segoe UI", 13, "bold")

# ----------------------------- Main App Window -----------------------------
root = ctk.CTk()
root.geometry("750x850")
root.title("🧞 Genie AI")

# ----------------------------- Frames -----------------------------
login_frame = ctk.CTkFrame(master=root, corner_radius=16)
signup_frame = ctk.CTkFrame(master=root, corner_radius=16)
chat_frame = ctk.CTkFrame(master=root, corner_radius=16)
settings_frame = ctk.CTkFrame(master=root, corner_radius=16)

login_frame.pack(expand=True, padx=30, pady=30)

# ----------------------------- Global State -----------------------------
user_email = None
chat_session_id = None

# ----------------------------- Utility Functions -----------------------------
def clear_frame(frame: ctk.CTkFrame):
    for child in frame.winfo_children():
        child.destroy()

def format_message(sender, message, is_user=True):
    timestamp = datetime.datetime.now().strftime("🕐 %H:%M")
    msg_type = "💬 You:" if is_user else "✨ Genie AI:"
    border = "─" * 60
    return f"\n{border}\n{msg_type} {message}\n{timestamp}\n{border}\n"

# ----------------------------- Show Login -----------------------------
def show_login():
    global user_email
    for frame in [signup_frame, chat_frame, settings_frame]:
        frame.pack_forget()
    clear_frame(login_frame)
    login_frame.pack(fill="both", expand=True, padx=30, pady=30)

    ctk.CTkLabel(login_frame, text="🔐 Login to Genie AI", font=FONT_TITLE).pack(pady=30)
    email_entry = ctk.CTkEntry(login_frame, placeholder_text="📧 Email", width=340, height=40, font=FONT_NORMAL)
    email_entry.pack(pady=10)
    password_entry = ctk.CTkEntry(login_frame, placeholder_text="🔒 Password", show="*", width=340, height=40, font=FONT_NORMAL)
    password_entry.pack(pady=10)
    message_label = ctk.CTkLabel(login_frame, text="", font=FONT_NORMAL)
    message_label.pack(pady=10)

    def login():
        nonlocal email_entry, password_entry
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        if not email or not password:
            message_label.configure(text="❌ Both fields are required.", text_color="red")
            return
        try:
            response = requests.post("http://127.0.0.1:5000/login", json={"email": email, "password": password})
            data = response.json()
            if response.status_code == 200:
                message_label.configure(text="✅ Login successful! Redirecting...", text_color="green")
                global user_email
                user_email = email
                login_frame.after(1000, show_chat)
            else:
                message_label.configure(text=data.get("error", "Login failed."), text_color="red")
        except Exception as e:
            message_label.configure(text=f"⚠ Error: {e}", text_color="red")

    ctk.CTkButton(login_frame, text="🔓 Login", command=login, width=340, height=40, font=FONT_BUTTON).pack(pady=15)
    ctk.CTkLabel(login_frame, text="────────── or ──────────").pack(pady=10)
    ctk.CTkButton(login_frame, text="📝 Go to Signup", command=show_signup, width=340, height=40).pack(pady=5)
    ctk.CTkButton(
    login_frame,
    text="🔑 Forgot Password?",
    command=show_forgot_password,
    width=340,
    height=40,
    font=FONT_BUTTON
).pack(pady=5)

# ----------------------------- Show Signup -----------------------------
def show_signup():
    for frame in [login_frame, chat_frame, settings_frame]:
        frame.pack_forget()
    clear_frame(signup_frame)
    signup_frame.pack(fill="both", expand=True, padx=30, pady=30)

    ctk.CTkLabel(signup_frame, text="📝 Create Your Genie AI Account", font=FONT_TITLE).pack(pady=30)
    name_entry = ctk.CTkEntry(signup_frame, placeholder_text="👤 Full Name", width=340, height=40, font=FONT_NORMAL)
    name_entry.pack(pady=8)
    email_entry = ctk.CTkEntry(signup_frame, placeholder_text="📧 Email", width=340, height=40, font=FONT_NORMAL)
    email_entry.pack(pady=8)
    password_entry = ctk.CTkEntry(signup_frame, placeholder_text="🔒 Password", show="*", width=340, height=40, font=FONT_NORMAL)
    password_entry.pack(pady=8)
    message_label = ctk.CTkLabel(signup_frame, text="", font=FONT_NORMAL)
    message_label.pack(pady=10)

    def signup():
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        if not name or not email or not password:
            message_label.configure(text="❌ All fields are required.", text_color="red")
            return
        try:
            response = requests.post("http://127.0.0.1:5000/signup", json={"username": name, "email": email, "password": password})
            data = response.json()
            if response.status_code == 201:
                global user_email
                user_email = email
                message_label.configure(text="✅ Signup successful! Redirecting...", text_color="green")
                signup_frame.after(1000, show_chat)
            else:
                message_label.configure(text=data.get("error", "Signup failed."), text_color="red")
        except Exception as e:
            message_label.configure(text=f"⚠ Error: {e}", text_color="red")

    ctk.CTkButton(signup_frame, text="✅ Sign Up", command=signup, width=340, height=40, font=FONT_BUTTON).pack(pady=15)
    ctk.CTkLabel(signup_frame, text="────────── or ──────────").pack(pady=10)
    ctk.CTkButton(signup_frame, text="🔙 Go to Login", command=show_login, width=340, height=40).pack(pady=5)

def show_forgot_password():
    for frame in [login_frame, signup_frame, chat_frame, settings_frame]:
        frame.pack_forget()
    clear_frame(login_frame)
    login_frame.pack(fill="both", expand=True, padx=30, pady=30)

    ctk.CTkLabel(login_frame, text="🔑 Reset Your Password", font=FONT_TITLE).pack(pady=30)

    email_entry = ctk.CTkEntry(login_frame, placeholder_text="📧 Your Email", width=340, height=40, font=FONT_NORMAL)
    email_entry.pack(pady=10)

    new_password_entry = ctk.CTkEntry(login_frame, placeholder_text="🔒 New Password", show="*", width=340, height=40, font=FONT_NORMAL)
    new_password_entry.pack(pady=10)

    message_label = ctk.CTkLabel(login_frame, text="", font=FONT_NORMAL)
    message_label.pack(pady=10)

    def reset_password():
        email = email_entry.get().strip()
        new_password = new_password_entry.get().strip()
        if not email or not new_password:
            message_label.configure(text="❌ Both fields are required.", text_color="red")
            return
        try:
            response = requests.post(
                "http://127.0.0.1:5000/reset-password",
                json={"email": email, "new_password": new_password}
            )
            data = response.json()
            if response.status_code == 200:
                message_label.configure(text="✅ Password reset! Go to login.", text_color="green")
            else:
                message_label.configure(text=data.get("error", "Reset failed."), text_color="red")
        except Exception as e:
            message_label.configure(text=f"⚠ Error: {e}", text_color="red")

    ctk.CTkButton(login_frame, text="🔄 Reset Password", command=reset_password, width=340, height=40, font=FONT_BUTTON).pack(pady=15)
    ctk.CTkButton(login_frame, text="🔙 Back to Login", command=show_login, width=340, height=40).pack(pady=5)

# ----------------------------- Show Chat -----------------------------
def show_chat():
    for frame in [login_frame, signup_frame, settings_frame]:
        frame.pack_forget()
    clear_frame(chat_frame)
    chat_frame.pack(fill="both", expand=True, padx=30, pady=30)

    # Header
    header = ctk.CTkFrame(chat_frame)
    header.pack(fill="x", padx=10, pady=(10, 5))
    ctk.CTkLabel(header, text="🧞 Genie AI Chat", font=FONT_TITLE).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(header, text="⚙ Settings", command=show_settings, width=120, height=35).pack(side="right", padx=10)

    # Messages
    messages_frame = ctk.CTkFrame(chat_frame)
    messages_frame.pack(fill="both", expand=True, padx=10, pady=5)
    messages_text = ctk.CTkTextbox(messages_frame, wrap="word", font=FONT_NORMAL)
    messages_text.pack(fill="both", expand=True, padx=10, pady=10)
    messages_text.configure(state="disabled")

    # Input Section
    input_frame = ctk.CTkFrame(chat_frame)
    input_frame.pack(fill="x", padx=10, pady=(5, 10))
    message_input = ctk.CTkEntry(input_frame, placeholder_text="💬 Type your message here...", height=45, font=FONT_NORMAL)
    message_input.pack(side="left", fill="x", expand=True, padx=(15, 8), pady=12)

    def send_message():
        global chat_session_id
        message = message_input.get().strip()
        if not message:
            return
        messages_text.configure(state="normal")
        messages_text.insert("end", format_message("You", message, is_user=True))
        messages_text.insert("end", "\n✨ Genie AI is thinking...\n")
        messages_text.configure(state="disabled")
        messages_text.see("end")
        message_input.delete(0, "end")
        try:
            response = requests.post("http://127.0.0.1:5000/chat", json={"message": message, "session_id": chat_session_id}, timeout=30)
            data = response.json()
            chat_session_id = data.get("session_id", chat_session_id)
            reply = data.get("response", "No response received.")
        except Exception as e:
            reply = f"⚠ Error: {str(e)}"
        messages_text.configure(state="normal")
        messages_text.insert("end", format_message("Genie AI", reply, is_user=False))
        messages_text.configure(state="disabled")
        messages_text.see("end")

    ctk.CTkButton(input_frame, text="🚀 Send", command=send_message, width=100, height=45, font=FONT_BUTTON).pack(side="right", padx=(8, 15), pady=12)
    message_input.bind("<Return>", lambda event: send_message())

    messages_text.configure(state="normal")
    messages_text.insert("end", format_message("Genie AI", "✨ Welcome to Genie AI! How can I assist you today?", is_user=False))
    messages_text.configure(state="disabled")

# ----------------------------- Show Settings -----------------------------
def show_settings():
    global user_email
    if not user_email:
        show_login()
        return
    for frame in [login_frame, signup_frame, chat_frame]:
        frame.pack_forget()
    clear_frame(settings_frame)
    settings_frame.pack(fill="both", expand=True, padx=30, pady=30)

    ctk.CTkLabel(settings_frame, text="👤 Profile Settings", font=FONT_TITLE).pack(pady=30)

    try:
        response = requests.get("http://127.0.0.1:5000/user", params={"email": user_email}, timeout=5)
        data = response.json() if response.status_code == 200 else {}
        current_name = data.get("username", "")
        current_email = data.get("email", user_email)
    except Exception:
        current_name = ""
        current_email = user_email

    name_entry = ctk.CTkEntry(settings_frame, placeholder_text="Full Name", width=340)
    name_entry.insert(0, current_name)
    name_entry.pack(pady=8)

    email_entry = ctk.CTkEntry(settings_frame, placeholder_text="Email", width=340)
    email_entry.insert(0, current_email)
    email_entry.pack(pady=8)

    password_entry = ctk.CTkEntry(settings_frame, placeholder_text="New Password", show="*", width=340)
    password_entry.pack(pady=8)

    message_label = ctk.CTkLabel(settings_frame, text="", font=FONT_NORMAL)
    message_label.pack(pady=8)

    def save_profile():
        global user_email
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        payload = {"email": user_email}
        if name and name != current_name:
            payload["new_name"] = name
        if email and email != current_email:
            payload["new_email"] = email
        if password:
            payload["password"] = password
        try:
            response = requests.put("http://127.0.0.1:5000/update-profile", json=payload)
            if response.status_code == 200:
                if "new_email" in payload:
                    user_email = payload["new_email"]
                message_label.configure(text="✅ Profile updated successfully!", text_color="green")
            else:
                message_label.configure(text="❌ Update failed.", text_color="red")
        except Exception as e:
            message_label.configure(text=f"⚠ Error: {str(e)}", text_color="red")

    ctk.CTkButton(settings_frame, text="💾 Save Changes", command=save_profile, width=340, font=FONT_BUTTON).pack(pady=12)
    ctk.CTkButton(settings_frame, text="🔙 Back to Chat", command=show_chat, width=340).pack(pady=6)
    ctk.CTkButton(settings_frame, text="🚪 Logout", command=show_login, width=340, fg_color="#EF4444", hover_color="#DC2626").pack(pady=12)

# ----------------------------- Start App -----------------------------
show_login()
root.mainloop()
