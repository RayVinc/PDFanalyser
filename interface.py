import customtkinter
from customtkinter import filedialog
from PyPDF2 import PdfReader
import tkinter as tk
import fitz  # pip install PyMuPDF Pillow

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

# Maximize window or set dimensions
root.after(0, lambda:root.state('zoomed'))
#root.geometry("1000x500")

# Configure columns
root.grid_columnconfigure(0, weight=2)  # 2/3 of the window
root.grid_columnconfigure(1, weight=1)  # 1/3 of the window
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

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

        # pdf_text.delete("1.0", "end")  # Clear any previous text
        # pdf_text.insert("1.0", text)  # Insert the extracted text into the Text widget

        print("Extracted text from the PDF:")
        print(text)

        # Destroy the upload button after the PDF is uploaded
        upload_button.destroy()
        label.destroy()

        # Frame for PDF display
        pdf_text = customtkinter.CTkTextbox(master=root, wrap="none", font=("Arial", 24))
        #pdf_text.pack(side=customtkinter.LEFT, pady=10, padx=10, fill="both", expand=True)
        pdf_text.grid(row=0, column=0, sticky='nesw', padx=5, pady=5)


        # Frame for chatbox
        chat_frame = customtkinter.CTkFrame(master=root)
        #chat_frame.pack(side=customtkinter.RIGHT, fill=customtkinter.BOTH, expand=True, padx=5, pady=5)
        chat_frame.grid(row=0, column=1, sticky='n', padx=5, pady=5)
        chat_frame.grid_rowconfigure(1, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)

        # Chat display (Text widget)
        chat_display = customtkinter.CTkTextbox(master=chat_frame, wrap=customtkinter.WORD)
        #chat_display.pack(side=customtkinter.RIGHT, fill=customtkinter.BOTH, expand=True, padx=5, pady=5)
        chat_display.grid(row=0, column=1, sticky='n', padx=5, pady=5)

        # Entry widget for typing messages
        chat_entry = customtkinter.CTkEntry(master=chat_frame)
        #chat_entry.pack(side=customtkinter.RIGHT, fill=customtkinter.BOTH, expand=True, padx=5, pady=5)
        chat_entry.grid(row=2, column=1, sticky='s', padx=5, pady=5)

frame = customtkinter.CTkFrame(master=root)
#frame.pack(pady=20, padx=60, fill="both", expand=True)
frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

label = customtkinter.CTkLabel(master=frame, text="PDF Analyzer", font=("Roboto", 40))
#label.pack(pady=12, padx=10)
label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

# Upload button
upload_button = customtkinter.CTkButton(
    master=frame,
    text="Upload PDF",
    corner_radius=10,
    command=upload_pdf,
    width=200,
    height=50,
    font=("Arial", 18))
#upload_button.pack(pady=30, padx=10)
upload_button.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

# # Create a Text widget to display PDF content
# pdf_text = customtkinter.CTkTextbox(master=frame, wrap="none", font=("Arial", 24))
# pdf_text.pack(pady=10, padx=10, fill="both", expand=True)



root.mainloop()
