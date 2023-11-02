import customtkinter
from customtkinter import filedialog
from PyPDF2 import PdfReader
import tkinter as tk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1200x500")

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

def submit_question():
    question = question_entry.get()
    if question:
        chat_text.insert("end", f"User: {question}\n")
        # You can add your logic here to generate an answer based on the question
        answer = "Analyzer: This is a sample answer."
        chat_text.insert("end", answer + "\n")
        question_entry.delete(0, "end")

# Create a frame for the viewer on the left
viewer_frame = customtkinter.CTkFrame(master=root)
viewer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create a frame for the chatbox on the right
chat_frame = customtkinter.CTkFrame(master=root)
chat_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

root.grid_columnconfigure(0, weight=1)  # Make the viewer frame expand
root.grid_columnconfigure(1, weight=1)  # Make the chat frame expand

label = customtkinter.CTkLabel(master=viewer_frame, text="PDF Analyzer", font=("Roboto", 40))
label.pack(pady=12, padx=10)

# Upload button
upload_button = customtkinter.CTkButton(
    master=viewer_frame,
    text="Upload PDF",
    corner_radius=10,
    command=upload_pdf,
    width=200,
    height=50,
    font=("Arial", 18))
upload_button.pack(pady=30, padx=10)

# Create a Text widget to display PDF content on the left
pdf_text = tk.Text(master=viewer_frame, wrap="none")
pdf_text.pack(pady=10, padx=10, fill="both", expand=True)

# Create a Text widget for the chatbox on the right
chat_text = tk.Text(master=chat_frame, wrap="word", width=50, height=20)
chat_text.pack(pady=10, padx=10, fill="both", expand=True)

# Create an entry field for questions
question_entry = tk.Entry(master=chat_frame, width=40)
question_entry.pack(pady=10, padx=10, fill="both", expand=False)

# Create a button to submit questions
submit_button = tk.Button(master=chat_frame, text="Submit", command=submit_question)
submit_button.pack(pady=10, padx=10)

root.mainloop()
