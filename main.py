import customtkinter
from customtkinter import filedialog
import tkinter as tk
from PyPDF2 import PdfReader
from transformers import pipeline

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1200x500")

# Create a pipeline for question-answering using a pre-trained model
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Create a frame for the viewer on the left
viewer_frame = customtkinter.CTkFrame(master=root)
viewer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create a Text widget to display PDF content on the left
pdf_text = tk.Text(viewer_frame, wrap="none")
pdf_text.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

# Create a frame for the title and buttons on the right
button_frame = customtkinter.CTkFrame(master=root)
button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

def upload_pdf():
    filepath = filedialog.askopenfilename(
        initialdir="/", title="Select file",
        filetypes=(("PDF files", "*.pdf"), ("all files", "*.*")))

    if filepath:
        print(f"File path: {filepath}")

        # Open the PDF file and extract text
        pdf_content = extract_text_from_pdf(filepath)

        pdf_text.delete("1.0", "end")  # Clear any previous text
        pdf_text.insert("1.0", pdf_content)  # Insert the extracted text into the Text widget

        print("Extracted text from the PDF:")
        print(pdf_content)

def extract_text_from_pdf(pdf_filepath):
    text = ""
    with open(pdf_filepath, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def submit_question():
    question = question_entry.get()
    if question:
        chat_text.insert("end", f"User: {question}\n")

        # Use the question-answering pipeline to answer the question
        answer = qa_pipeline(context=pdf_text.get("1.0", "end"), question=question)

        chat_text.insert("end", f"Analyzer: {answer['answer']}\n")
        question_entry.delete(0, "end")

label = customtkinter.CTkLabel(master=button_frame, text="PDF Analyzer", font=("Roboto", 40))
label.grid(row=0, column=0, pady=12, padx=10)

# Upload button
upload_button = customtkinter.CTkButton(
    master=button_frame,
    text="Upload PDF",
    corner_radius=10,
    command=upload_pdf,
    width=200,
    height=50,
    font=("Arial", 18))
upload_button.grid(row=1, column=0, pady=30, padx=10)

# Create a Text widget for the chatbox on the right
chat_text = tk.Text(button_frame, wrap="word", width=50, height=20)
chat_text.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

# Create an entry field for questions
question_entry = tk.Entry(button_frame, width=40)
question_entry.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

# Create a button to submit questions
submit_button = tk.Button(button_frame, text="Submit", command=submit_question)
submit_button.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")

# Configure column and row weights to make widgets expand properly
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
