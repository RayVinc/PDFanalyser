import customtkinter
from customtkinter import filedialog
from PyPDF2 import PdfReader

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

        # open the PDF file
        with open(filepath, "rb") as f:
            reader = PdfReader(f)
            text = ""

            # loop through all the pages
            for i in range(reader.numPages):
                page = reader.getPage(i)
                text += page.extractText()

            print("Extracted text from the PDF:")
            print(text)

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text = "PDF Analyser", font=("Roboto", 40))
label.pack(pady=12, padx=10)

# upload button
upload_button = customtkinter.CTkButton(
    master=root, 
    text="Upload PDF", 
    corner_radius=10, 
    command=upload_pdf,
    width=200,
    height=50,
    font=("Arial", 18))
upload_button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
upload_button.pack(pady=30, padx=10)

root.mainloop()