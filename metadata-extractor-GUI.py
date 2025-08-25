from tkinter import filedialog, messagebox
from metadata_extractor import extract_metadata
import customtkinter
from metadata_extractor import extract_metadata

# button functionality
def select_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        output.insert("0.0", f"Selected file: {extract_metadata(filepath)}\n")

def clear_output():
    output.delete("0.0", "end")

# GUI setup
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("720x480")
app.title("Metadata Extractor for jpg/pdf")

title = customtkinter.CTkLabel(app, text="Select a valid filepath for a pdf or jpg/jpeg file")
title.pack(padx=10, pady=10)

file_button = customtkinter.CTkButton(app, text="Select File", command=select_file)
file_button.pack(pady=10)

output = customtkinter.CTkTextbox(app, height=300, width=600)
output.pack(padx=10, pady=10)

clear_button = customtkinter.CTkButton(app, text="Clear Output", command=clear_output)
clear_button.pack(pady=5)

app.mainloop()