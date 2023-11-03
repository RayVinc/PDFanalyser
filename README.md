This tool is supposed to resemble a local tool that functions quite similarly to https://www.chatpdf.com/ , so users don't have to upload files to websites to use a tool.

The tool is utilising an LLM on a pdf that helps you find stuff in a pdf and answers questions for you.

To **display the actual PDF file** (not just its text content) within a Tkinter application, we can use an external library like *PyMuPDF* (also known as fitz). This library allows you to render PDF pages as images, which you can then display in your Tkinter application using the *PhotoImage* or *ImageTk.PhotoImage* classes.

UI will be built with *customtkinter*, an extension of the regular *tkinter* that allows for more modern looking interfaces.

The LLM will be built utilizing open source LLMs like *haystack*.



# Planned Layout
![planned layout](interface_layout.png)



# The User Interface So Far

![pdfUI2](https://github.com/UKVeteran/PDFanalyser/assets/39216339/1dc1e681-5c98-4f6c-a1b0-b553eb27bcfc)



# What To Do?

Preprocessing Text: Implement text preprocessing techniques to clean and normalize the text before feeding it to the question-answering model. This can include tasks like lowercasing, punctuation removal, and stemming/lemmatization.

Natural Language Understanding (NLU): Integrate a Natural Language Understanding (NLU) component to better understand user queries. You can use libraries like spaCy or NLTK for tasks such as part-of-speech tagging, named entity recognition, and sentiment analysis.

Context Handling: Improve the chatbot's ability to maintain context in the conversation. Store previous user interactions and use that context to answer follow-up questions or maintain a coherent conversation.

Error Handling: Implement better error handling to gracefully handle unexpected input and provide meaningful responses when the chatbot doesn't understand a query.

Feedback Loop: Allow users to provide feedback on the chatbot's responses. This feedback can be used to train and improve the chatbot over time.

Multimodal Support: If your PDF viewer can handle images, consider adding support for processing images within PDFs. You can use Optical Character Recognition (OCR) to extract text from images.

Advanced Question-Answering Models: Experiment with more advanced question-answering models or fine-tune them on domain-specific data for improved accuracy.
