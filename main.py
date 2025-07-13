from tkinter import filedialog
import customtkinter as ctk
import requests
from bson.json_util import dumps

# ✅ Change 1: Changed color theme to green
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry("600x700")
root.title("Genie AI")

login_frame = ctk.CTkFrame(master=root, corner_radius=10)
signup_frame = ctk.CTkFrame(master=root, corner_radius=10)
chat_frame = ctk.CTkFrame(master=root, corner_radius=10)
settings_frame = ctk.CTkFrame(master=root, corner_radius=10)
login_frame.pack(expand=True, padx=20, pady=20)

user_email = None
chat_session_id = None

def clear_frame(frame: ctk.CTkFrame) -> None:
    for child in frame.winfo_children():
        child.destroy()

def show_settings():
    global user_email
    if not user_email:
        show_login()
        return
    for frame in [login_frame, signup_frame, chat_frame]:
        frame.pack_forget()
    clear_frame(settings_frame)
    settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(settings_frame, text="👤 Profile & Settings", font=("Arial", 22, "bold")).pack(pady=20)
    try:
        response = requests.get("http://127.0.0.1:5000/user", params={"email": user_email}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            current_name = data.get("username", "")
            current_email = data.get("email", "")
        else:
            current_name = ""
            current_email = user_email or ""
    except Exception:
        current_name = ""
        current_email = user_email or ""
    name_entry = ctk.CTkEntry(settings_frame, placeholder_text="Name", width=300)
    name_entry.insert(0, current_name)
    name_entry.pack(pady=8)
    email_entry = ctk.CTkEntry(settings_frame, placeholder_text="Email", width=300)
    email_entry.insert(0, current_email)
    email_entry.pack(pady=8)
    password_entry = ctk.CTkEntry(settings_frame, placeholder_text="New Password", show="*", width=300)
    password_entry.pack(pady=8)
    message_label = ctk.CTkLabel(settings_frame, text="", font=("Arial", 12))
    message_label.pack(pady=5)

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
                message_label.configure(text="✅ Profile updated successfully!", text_color="green")
                if "new_email" in payload:
                    user_email = payload["new_email"]
            else:
                message_label.configure(text="❌ Update failed.", text_color="red")
        except Exception as e:
            message_label.configure(text=f"⚠ Error: {str(e)}", text_color="red")

    ctk.CTkButton(settings_frame, text="💾 Save Changes", command=save_profile, width=300).pack(pady=16)
    ctk.CTkButton(settings_frame, text="🚪 Logout", command=show_login, width=300, fg_color="red").pack(pady=20)
    ctk.CTkButton(settings_frame, text="🔙 Back to Chat", command=show_chat, width=300).pack(pady=8)

def show_chat():
    for frame in [login_frame, signup_frame, settings_frame]:
        frame.pack_forget()
    clear_frame(chat_frame)
    chat_frame.pack(fill="both", expand=True, padx=20, pady=20)

    header_frame = ctk.CTkFrame(chat_frame, fg_color=("gray90", "gray20"))
    header_frame.pack(fill="x", padx=10, pady=(10, 5))

    ctk.CTkLabel(header_frame, text="🧞 Genie AI Chat", font=("Arial", 22, "bold"),
                 text_color=("gray20", "white")).pack(side="left", padx=10, pady=10)

    settings_btn = ctk.CTkButton(header_frame, text="⚙ Settings", width=100, height=32,
                                 font=("Arial", 16), command=show_settings)
    settings_btn.pack(side="right", padx=10, pady=10)

    messages_frame = ctk.CTkFrame(chat_frame, fg_color=("gray95", "gray15"))
    messages_frame.pack(fill="both", expand=True, padx=10, pady=5)

    messages_text = ctk.CTkTextbox(messages_frame, wrap="word", height=400,
                                   font=("Arial", 16), fg_color=("white", "gray10"))
    messages_text.pack(fill="both", expand=True, padx=10, pady=10)
    messages_text.configure(state="disabled")

    input_frame = ctk.CTkFrame(chat_frame, fg_color=("gray90", "gray20"))
    input_frame.pack(fill="x", padx=10, pady=(5, 10))

    message_input = ctk.CTkEntry(input_frame, placeholder_text="💬 Type your message here...",
                                 height=45, font=("Arial", 16))
    message_input.pack(side="left", fill="x", expand=True, padx=(15, 8), pady=12)

    def format_message(sender, message, is_user=True):
        timestamp = "🕐 Just now"
        msg_type = "💬" if is_user else "✨"
        return f"\n{'='*50}\n {sender} • {timestamp}\n{msg_type} {message}\n{'='*50}\n"

    def send_message():
        global chat_session_id
        message = message_input.get().strip()
        if not message:
            return
        messages_text.configure(state="normal")
        messages_text.insert("end", format_message("You", message, is_user=True))
        messages_text.insert("end", "Genie AI • 🕐 Just now\n💭 Thinking...\n")
        messages_text.configure(state="disabled")
        messages_text.see("end")
        message_input.delete(0, "end")
        try:
            response = requests.post("http://127.0.0.1:5000/chat",
                                     json={"message": message, "session_id": chat_session_id}, timeout=30)
            if response.status_code == 200:
                data = response.json()
                chat_session_id = data.get("session_id", chat_session_id)
                reply = data.get("response", "No response received")
            else:
                reply = response.json().get("error", "Unknown error occurred")
        except Exception as e:
            reply = f"⚠ Error: {str(e)}"
        messages_text.configure(state="normal")
        messages_text.insert("end", format_message("Genie AI", reply, is_user=False))
        messages_text.configure(state="disabled")
        messages_text.see("end")

    # ✅ Change 2: Send button has rounded corners
    send_button = ctk.CTkButton(
        input_frame,
        text="🚀 Send",
        command=send_message,
        width=100,
        height=45,
        font=("Arial", 12, "bold"),
        fg_color=("blue", "darkblue"),
        hover_color=("darkblue", "blue"),
        corner_radius=10  # Rounded edges
    )

    ctk.CTkButton(input_frame, text="👤 Profile", command=show_profile, width=100, height=45,
                  font=("Arial", 12)).pack(side="right", padx=(0, 8), pady=12)

    send_button.pack(side="right", padx=(8, 15), pady=12)
    message_input.bind("<Return>", lambda event: send_message())

    messages_text.configure(state="normal")
    welcome_msg = format_message("Genie AI", "✨ Welcome to Genie AI! How can I assist you today?", is_user=False)
    messages_text.insert("end", welcome_msg)
    messages_text.configure(state="disabled")

def show_login():
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
        global user_email
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        if not email or not password:
            message_label.configure(text="Both fields are required.", text_color="red")
            return
        try:
            response = requests.post("http://127.0.0.1:5000/login", json={"email": email, "password": password})
            data = response.json()
            if response.status_code == 200:
                user_email = email
                message_label.configure(text="Login successful! Redirecting...", text_color="green")
                login_frame.after(1000, show_chat)
            else:
                message_label.configure(text=data.get("error", "Login failed."), text_color="red")
        except Exception as e:
            message_label.configure(text=f"Error: {e}", text_color="red")

    ctk.CTkButton(login_frame, text="Login", command=login, width=300).pack(pady=10)
    ctk.CTkLabel(login_frame, text="OR").pack(pady=(8, 8))
    ctk.CTkButton(login_frame, text="Go to Signup", command=show_signup, width=300).pack(pady=(0, 8))

def show_signup():
    for frame in [login_frame, chat_frame, settings_frame]:
        frame.pack_forget()
    clear_frame(signup_frame)
    signup_frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(signup_frame, text="Sign Up", font=("Arial", 20)).pack(pady=20)
    name_entry = ctk.CTkEntry(signup_frame, placeholder_text="Name", width=300)
    name_entry.pack(pady=(8, 0), padx=10)
    email_entry = ctk.CTkEntry(signup_frame, placeholder_text="Email", width=300)
    email_entry.pack(_
