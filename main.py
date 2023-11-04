import customtkinter
from customtkinter import filedialog
import tkinter as tk
from transformers import pipeline
import fitz  # PyMuPDF

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1400x700")

qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

viewer_frame = customtkinter.CTkFrame(master=root)
viewer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

pdf_text = tk.Text(viewer_frame, wrap="none", width=80, height=20)
pdf_text.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

button_frame = customtkinter.CTkFrame(master=root)
button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

def upload_pdf():
    filepath = filedialog.askopenfilename(
        initialdir="/", title="Select file",
        filetypes=(("PDF files", "*.pdf"), ("all files", "*.*")))

    if filepath:
        print(f"File path: {filepath}")

        display_entire_pdf(filepath)

        print("PDF displayed")

def display_entire_pdf(pdf_filepath):
    pdf_text.delete("1.0", "end")  # Clear previous text

    pdf_document = fitz.open(pdf_filepath)

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        pdf_text.insert("end", text)

def submit_question():
    question = question_entry.get()
    if question:
        chat_text.insert("end", f"User: {question}\n")

        answer = qa_pipeline(context=pdf_text.get("1.0", "end"), question=question)

        chat_text.insert("end", f"Analyzer: {answer['answer']}\n")
        question_entry.delete(0, "end")

label = customtkinter.CTkLabel(master=button_frame, text="PDF Analyzer", font=("Arial", 32))
label.grid(row=0, column=0, pady=12, padx=10)

upload_button = customtkinter.CTkButton(
    master=button_frame,
    text="Upload PDF",
    corner_radius=10,
    command=upload_pdf,
    width=200,
    height=50,
    font=("Arial", 18)
)
upload_button.grid(row=1, column=0, pady=30, padx=10)

chat_text = tk.Text(button_frame, wrap="word", width=80, height=10)
chat_text.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

question_entry = tk.Entry(button_frame, width=40)
question_entry.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

submit_button = tk.Button(button_frame, text="Submit", command=submit_question)
submit_button.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
