import customtkinter as ctk

root = ctk.CTk()
root.geometry("1020x768")

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("light")

root.title("Genie AI")
btn1 = ctk.CTkButton(root, text="Hello")
btn1.pack()

root.mainloop()