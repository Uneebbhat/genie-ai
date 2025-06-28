# main.py
from tkinter import YES
import customtkinter as ctk
import requests

# ── Global appearance ──────────────────────────────────────────────────────────
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# ── Main window ────────────────────────────────────────────────────────────────
root = ctk.CTk()
root.geometry("600x700")
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

# Global variable to store chat session ID
chat_session_id = None

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
    
    # Header with gradient-like styling
    header_frame = ctk.CTkFrame(chat_frame, fg_color=("gray90", "gray20"))
    header_frame.pack(fill="x", padx=10, pady=(10, 5))
    
    ctk.CTkLabel(header_frame, text="🤖 Genie AI Chat", font=("Arial", 22, "bold"), 
                text_color=("gray20", "white")).pack(pady=15)
    
    # Chat messages display area
    messages_frame = ctk.CTkFrame(chat_frame, fg_color=("gray95", "gray15"))
    messages_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Text widget for displaying messages with better styling
    messages_text = ctk.CTkTextbox(messages_frame, wrap="word", height=400, 
                                  font=("Arial", 11), fg_color=("white", "gray10"))
    messages_text.pack(fill="both", expand=True, padx=10, pady=10)
    messages_text.configure(state="disabled")  # Make it read-only
    
    # Input area with better styling
    input_frame = ctk.CTkFrame(chat_frame, fg_color=("gray90", "gray20"))
    input_frame.pack(fill="x", padx=10, pady=(5, 10))
    
    # Message input field with better styling
    message_input = ctk.CTkEntry(input_frame, placeholder_text="💬 Type your message here...", 
                                height=45, font=("Arial", 12))
    message_input.pack(side="left", fill="x", expand=True, padx=(15, 8), pady=12)
    
    def format_message(sender, message, is_user=True):
        """Format messages with colors and styling"""
        timestamp = "🕐 " + "Just now"
        
        if is_user:
            # User message styling
            formatted_msg = f"\n{'='*50}\n"
            formatted_msg += f" You • {timestamp}\n"
            formatted_msg += f"💬 {message}\n"
            formatted_msg += f"{'='*50}\n"
        else:
            # AI message styling
            formatted_msg = f"\n{'='*50}\n"
            formatted_msg += f"🤖 Genie AI • {timestamp}\n"
            formatted_msg += f"✨ {message}\n"
            formatted_msg += f"{'='*50}\n"
        
        return formatted_msg
    
    def send_message():
        global chat_session_id
        message = message_input.get().strip()
        if message:
            # Display user message with formatting
            messages_text.configure(state="normal")
            user_formatted = format_message("You", message, is_user=True)
            messages_text.insert("end", user_formatted)
            messages_text.configure(state="disabled")
            messages_text.see("end")  # Auto-scroll to bottom
            
            # Clear input field
            message_input.delete(0, "end")
            
            # Disable send button while processing
            send_button.configure(state="disabled")
            
            # Show typing indicator with animation
            messages_text.configure(state="normal")
            typing_msg = f"\n{'='*50}\n Genie AI • 🕐 Just now\n💭 Thinking"
            messages_text.insert("end", typing_msg)
            messages_text.configure(state="disabled")
            messages_text.see("end")
            
            # Send message to backend API
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/chat",
                    json={
                        "message": message,
                        "session_id": chat_session_id
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data.get("response", "No response received")
                    chat_session_id = data.get("session_id", chat_session_id)
                    
                    # Remove typing indicator and show actual response
                    messages_text.configure(state="normal")
                    # Remove the typing indicator
                    last_line_start = messages_text.index("end-3l linestart")
                    messages_text.delete(last_line_start, "end-1c")
                    # Add the actual response with formatting
                    ai_formatted = format_message("Genie AI", ai_response, is_user=False)
                    messages_text.insert("end", ai_formatted)
                    messages_text.configure(state="disabled")
                    messages_text.see("end")
                else:
                    error_msg = response.json().get("error", "Unknown error occurred")
                    # Remove typing indicator and show error
                    messages_text.configure(state="normal")
                    last_line_start = messages_text.index("end-3l linestart")
                    messages_text.delete(last_line_start, "end-1c")
                    error_formatted = f"\n{'='*50}\n❌ Error • 🕐 Just now\n⚠️ {error_msg}\n{'='*50}\n"
                    messages_text.insert("end", error_formatted)
                    messages_text.configure(state="disabled")
                    messages_text.see("end")
                    
            except requests.exceptions.RequestException as e:
                # Remove typing indicator and show connection error
                messages_text.configure(state="normal")
                last_line_start = messages_text.index("end-3l linestart")
                messages_text.delete(last_line_start, "end-1c")
                connection_error = f"\n{'='*50}\n❌ Connection Error • 🕐 Just now\n🌐 Unable to reach the server. Please check if the backend is running.\n{'='*50}\n"
                messages_text.insert("end", connection_error)
                messages_text.configure(state="disabled")
                messages_text.see("end")
            except Exception as e:
                # Remove typing indicator and show general error
                messages_text.configure(state="normal")
                last_line_start = messages_text.index("end-3l linestart")
                messages_text.delete(last_line_start, "end-1c")
                general_error = f"\n{'='*50}\n❌ Error • 🕐 Just now\n⚠️ {str(e)}\n{'='*50}\n"
                messages_text.insert("end", general_error)
                messages_text.configure(state="disabled")
                messages_text.see("end")
            finally:
                # Re-enable send button
                send_button.configure(state="normal")
    
    # Send button with better styling
    send_button = ctk.CTkButton(input_frame, text="🚀 Send", command=send_message, 
                               width=100, height=45, font=("Arial", 12, "bold"),
                               fg_color=("blue", "darkblue"), hover_color=("darkblue", "blue"))
    send_button.pack(side="right", padx=(8, 15), pady=12)
    
    # Bind Enter key to send message
    message_input.bind("<Return>", lambda event: send_message())
    
    # Add a beautiful welcome message
    messages_text.configure(state="normal")
    welcome_msg = f"\n{'='*50}\n Genie AI • 🕐 Just now\n✨ Welcome to Genie AI! I'm here to help you with any questions or tasks. How can I assist you today?\n{'='*50}\n"
    messages_text.insert("end", welcome_msg)
    messages_text.configure(state="disabled")


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
    # Hide all frames
    for frame in [login_frame, chat_frame, settings_frame]:
        frame.pack_forget()
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
