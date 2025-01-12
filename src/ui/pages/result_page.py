import customtkinter as ctk
from pdf2image import convert_from_path
from PIL import ImageTk

class ResultPage(ctk.CTkFrame):
    def __init__(self, master, file_path=None):
        super().__init__(master)
        self.file_path = file_path

        # Title
        self.title_label = ctk.CTkLabel(self, text="Merged PDF", font=("Arial", 20))
        self.title_label.pack(pady=10)

        # Scrollable Frame for PDF Preview
        self.preview_frame = ctk.CTkScrollableFrame(self)
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def load_pdf(self, file_path):
        self.file_path = file_path

        # Clear any previous previews
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        # Convert and display the PDF pages
        images = convert_from_path(self.file_path)
        for img in images:
            img = img.resize((600, int(600 * img.height / img.width)))
            img_tk = ImageTk.PhotoImage(img)
            label = ctk.CTkLabel(self.preview_frame, image=img_tk, text="")
            label.image = img_tk
            label.pack(pady=10)
