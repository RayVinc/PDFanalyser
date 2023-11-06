import customtkinter
from customtkinter import filedialog
from PyPDF2 import PdfReader
from PIL import Image, ImageTk
from tkinter import Canvas
import fitz #PyMuPDF
#####from transformers import pipeline

#####VR: commented out the pipeline to have faster testing during interface redesign.
#####VR: Uploaded PDF will be rendered as image. Should be an interactive PDF instead, to highlight and copy text from it

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class PDFAnalyzerApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.pdf = None
        self.photo_images = []

        # Configure column and row weights to make widgets expand properly
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.title("PDF Analyzer")
        self.after(0, lambda: self.state('zoomed'))

        # Create a pipeline for question-answering using a pre-trained model
        #####self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")  # Uncomment if using pipeline

        # Create a frame for the viewer on the left
        self.viewer_frame = customtkinter.CTkFrame(master=self)
        self.viewer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.viewer_frame.grid_rowconfigure(0, weight=1)
        self.viewer_frame.grid_columnconfigure(0, weight=1)

        # Create a Text widget to display PDF content on the left
        self.pdf_text = customtkinter.CTkTextbox(self.viewer_frame)
        self.pdf_text.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")


        # Create a frame for the title and buttons on the right
        self.button_frame = customtkinter.CTkFrame(master=self)
        self.button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(1, weight=1)
        self.button_frame.grid_rowconfigure(2, weight=90)
        self.button_frame.grid_rowconfigure(3, weight=7)
        self.button_frame.grid_rowconfigure(4, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=99)
        self.button_frame.grid_columnconfigure(1, weight=1)

        label = customtkinter.CTkLabel(master=self.button_frame, text="PDF Analyzer", font=("Roboto", 40))
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Upload button
        upload_button = customtkinter.CTkButton(
            master=self.button_frame,
            text="Upload PDF",
            corner_radius=10,
            command=self.upload_pdf,
            width=200,
            height=50,
            font=("Arial", 18))
        upload_button.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        # Create a Text widget for the chatbox on the right
        self.chat_text = customtkinter.CTkTextbox(self.button_frame)
        self.chat_text.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Create an entry field for questions
        self.question_entry = customtkinter.CTkEntry(self.button_frame, placeholder_text="Ask a question about the PDF...")
        self.question_entry.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

        # Create a button to submit questions
        self.submit_button_image = customtkinter.CTkImage(
                                                light_image=Image.open("SubmitButton2.png"), #VR: Image to be changed later
                                                dark_image=Image.open("SubmitButton2.png"),
                                                size=(50, 50))
        submit_button = customtkinter.CTkButton(self.button_frame,
                                                text="",
                                                command=self.submit_question,
                                                corner_radius=25,
                                                width=50, height=50,
                                                image=self.submit_button_image)
        submit_button.grid(row=3, column=1, pady=10, padx=10)
        submit_button.image = self.submit_button_image





    def upload_pdf(self):
        filepath = filedialog.askopenfilename(
            initialdir="/", title="Select file",
            filetypes=(("PDF files", "*.pdf"), ("all files", "*.*")))

        if filepath:
            print(f"File path: {filepath}")

            # Open the PDF file and extract text
            #####pdf_content = self.extract_text_from_pdf(filepath)
            #####self.pdf_text.delete("1.0", "end")  # Clear any previous text
            #####self.pdf_text.insert("1.0", pdf_content)  # Insert the extracted text into the Text widget

            #####print("Extracted text from the PDF:")
            #####print(pdf_content)

            pdf_content = self.extract_pdf(filepath)


    def extract_pdf(self, pdf_filepath):
        try:
            self.pdf = fitz.open(pdf_filepath)
            page = self.pdf.load_page(0)  # Load the first page (or iterate for multiple pages)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            photo = ImageTk.PhotoImage(img)
            self.photo_images.append(photo)  # Keep a reference!

            # If you haven't already created a canvas, do it here
            if not hasattr(self, 'pdf_canvas'):
                self.pdf_canvas = Canvas(self.viewer_frame, bg="#333333")
                self.pdf_canvas.grid(row=0, column=0, sticky='nsew')

            # Clear the canvas and create a new image
            self.pdf_canvas.delete("all")
            # Clear the canvas and create a new image
            self.pdf_canvas.delete("all")
            self.image_on_canvas = self.pdf_canvas.create_image(
                self.viewer_frame.winfo_width() / 2,  # Center horizontally
                self.viewer_frame.winfo_height() / 2,  # Center vertically
                image=photo,
                anchor="center"
            )

            # Set scroll region to encompass the image
            self.pdf_canvas.config(scrollregion=self.pdf_canvas.bbox("all"))
            # Bind mouse wheel event for zooming
            self.pdf_canvas.bind('<MouseWheel>', self.zoom_image)

        except Exception as e:
            print(f"Failed to open PDF: {e}")


    def zoom_image(self, event):
        if event.delta > 0:
            scale_factor = 1.1  # Zoom in
        else:
            scale_factor = 0.9  # Zoom out

        self.pdf_canvas.scale("all", event.x, event.y, scale_factor, scale_factor)
        self.pdf_canvas.config(scrollregion=self.pdf_canvas.bbox("all"))


    def extract_text_from_pdf(self, pdf_filepath): #VR: should be changed to display real PDF, not just extracted text
        text = ""
        with open(pdf_filepath, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text() or " "  # Add a space if extract_text() returns None
        return text

    def submit_question(self):
        question = self.question_entry.get()
        if question:
            self.chat_text.insert("end", f"User: {question}\n")

            answer = self.qa_pipeline(context=self.pdf_text.get("1.0", "end"), question=question)
            self.chat_text.insert("end", f"Analyzer: {answer['answer']}\n")
            self.question_entry.delete(0, "end")

app = PDFAnalyzerApp()
app.mainloop()
