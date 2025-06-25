import customtkinter as ctk

# Fadil message
# Abdullah message

# Set appearance and theme (optional)
ctk.set_appearance_mode("Light")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Theme colors: "blue", "green", "dark-blue"

# Create main window
root = ctk.CTk()

# Set window size and title
root.geometry("1366x668")
root.title("Genie AI")

# Create both frames (screens)
chat_frame = ctk.CTkFrame(master=root)
settings_frame = ctk.CTkFrame(master=root)

# --- Chat Screen ---
def show_chat():
    settings_frame.pack_forget()
    chat_frame.pack(fill="both", expand=True)

    # Clear previous widgets in chat_frame (if any)
    for widget in chat_frame.winfo_children():
        widget.destroy()

    # Chat display area (top)
    chat_display = ctk.CTkTextbox(chat_frame, height=400, state="disabled", font=("Arial", 14))
    chat_display.pack(fill="both", expand=True, padx=20, pady=(20, 10))

    # Input area (bottom)
    input_frame = ctk.CTkFrame(chat_frame)
    input_frame.pack(fill="x", side="bottom", padx=20, pady=(0, 20))

    user_entry = ctk.CTkEntry(
        input_frame,
        placeholder_text="Type your message...",
        font=("Arial", 14),
        bg_color="#f0f0f0"
    )
    user_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    def send_message():
        message = user_entry.get().strip()
        if message:
            chat_display.configure(state="normal")
            chat_display.insert("end", f"You: {message}\n")
            chat_display.configure(state="disabled")
            chat_display.see("end")  # Scroll to the end
            user_entry.delete(0, "end")

    send_button = ctk.CTkButton(input_frame, text="Send", width=80, command=send_message)
    send_button.pack(side="right")

    # Optional: Bind Enter key to send message
    user_entry.bind("<Return>", lambda event: send_message())

home_label = ctk.CTkLabel(chat_frame, text="Chat", font=("Arial", 20))
home_label.pack_forget()  # No longer needed, replaced by chat_display

# Show home screen initially
show_chat()

# Run the app
root.mainloop()
