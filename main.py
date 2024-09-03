import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk 
from PyPDF2 import PdfMerger
from tkPDFViewer import tkPDFViewer as pdf

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("800x600")
        self.root.configure(bg="#1c1c1c")
        
        # Header Section
        self.header = ttk.Frame(self.root)
        self.header.pack(fill=tk.X, pady=10)
        
        self.title_label = ttk.Label(self.header, text="PDF Merger", font=("Helvetica", 18))
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        self.settings_button = ttk.Button(self.header, text="Settings", command=self.open_settings)
        self.settings_button.pack(side=tk.RIGHT, padx=10)
        
        # File Explorer & List Section
        self.file_frame = ttk.Frame(self.root)
        self.file_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.file_listbox = tk.Listbox(self.file_frame, selectmode=tk.EXTENDED, bg="#333", fg="#fff", font=("Helvetica", 12))
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        self.file_scrollbar = ttk.Scrollbar(self.file_frame, orient="vertical")
        self.file_scrollbar.config(command=self.file_listbox.yview)
        self.file_listbox.config(yscrollcommand=self.file_scrollbar.set)
        self.file_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        
        self.add_file_button = ttk.Button(self.file_frame, text="Add PDF Files", command=self.add_files)
        self.add_file_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.remove_file_button = ttk.Button(self.file_frame, text="Remove Selected", command=self.remove_files)
        self.remove_file_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # PDF Preview Section
        self.preview_frame = ttk.Frame(self.root)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.preview_label = ttk.Label(self.preview_frame, text="PDF Preview", font=("Helvetica", 14))
        self.preview_label.pack(pady=5)
        
        self.pdf_viewer = pdf.ShowPdf()
        self.pdf_display = self.pdf_viewer.pdf_view(self.preview_frame, width=60, height=30)
        self.pdf_display.pack(pady=10)
        
        # Output Section
        self.output_frame = ttk.Frame(self.root)
        self.output_frame.pack(fill=tk.X, pady=10)
        
        self.output_label = ttk.Label(self.output_frame, text="Output File Name", font=("Helvetica", 12))
        self.output_label.pack(side=tk.LEFT, padx=10)
        
        self.output_entry = ttk.Entry(self.output_frame, width=40)
        self.output_entry.pack(side=tk.LEFT, padx=10)
        self.output_entry.insert(0, "Merged_PDF.pdf")
        
        self.output_button = ttk.Button(self.output_frame, text="Choose Directory", command=self.choose_directory)
        self.output_button.pack(side=tk.RIGHT, padx=10)
        
        self.merge_button = ttk.Button(self.output_frame, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.pack(side=tk.RIGHT, padx=10)
        
        # Footer Section
        self.footer = ttk.Frame(self.root)
        self.footer.pack(fill=tk.X, pady=10)
        
        self.progress = ttk.Progressbar(self.footer, orient=tk.HORIZONTAL, mode='determinate', length=100)
        self.progress.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.status_label = ttk.Label(self.footer, text="Ready", font=("Helvetica", 10))
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
    def open_settings(self):
        messagebox.showinfo("Settings", "Settings window placeholder")
    
    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for file in files:
            self.file_listbox.insert(tk.END, file)
    
    def remove_files(self):
        selected_files = self.file_listbox.curselection()
        for index in reversed(selected_files):
            self.file_listbox.delete(index)
    
    def choose_directory(self):
        directory = filedialog.askdirectory()
        self.output_directory = directory
    
    def merge_pdfs(self):
        files = list(self.file_listbox.get(0, tk.END))
        if not files:
            messagebox.showwarning("No Files", "Please add PDF files to merge.")
            return
        
        output_file = self.output_entry.get()
        if not output_file.endswith(".pdf"):
            output_file += ".pdf"
        
        output_path = os.path.join(self.output_directory, output_file)
        
        merger = PdfMerger()
        
        for file in files:
            merger.append(file)
        
        with open(output_path, "wb") as f_out:
            merger.write(f_out)
        
        self.status_label.config(text="Merging Completed!")
        messagebox.showinfo("Merge Complete", f"PDFs merged into {output_file}")

if __name__ == "__main__":
    root = ThemedTk(theme="black")
    app = PDFMergerApp(root)
    root.mainloop()
