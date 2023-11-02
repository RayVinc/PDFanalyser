import customtkinter
from customtkinter import filedialog
from PyPDF2 import PdfReader
import tkinter as tk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1000x500")

def upload_pdf():
    filepath = filedialog.askopenfilename(
        initialdir="/", title="Select file",
        filetypes=(("PDF files", "*.pdf"), ("all files", "*.*")))

    if filepath:
        print(f"File path: {filepath}")

        # Open the PDF file
        reader = PdfReader(filepath)
        text = ""

        # Loop through all the pages
        for page in reader.pages:
            text += page.extract_text()

        pdf_text.delete("1.0", "end")  # Clear any previous text
        pdf_text.insert("1.0", text)  # Insert the extracted text into the Text widget

        print("Extracted text from the PDF:")
        print(text)

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="PDF Analyzer", font=("Roboto", 40))
label.pack(pady=12, padx=10)

# Upload button
upload_button = customtkinter.CTkButton(
    master=frame,
    text="Upload PDF",
    corner_radius=10,
    command=upload_pdf,
    width=200,
    height=50,
    font=("Arial", 18))
upload_button.pack(pady=30, padx=10)

# Create a Text widget to display PDF content
pdf_text = tk.Text(master=frame, wrap="none")
pdf_text.pack(pady=10, padx=10, fill="both", expand=True)

root.mainloop()
