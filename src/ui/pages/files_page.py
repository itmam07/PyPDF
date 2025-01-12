import os
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PyPDF2 import PdfMerger
from pdf2image import convert_from_path
from PIL import ImageTk
from settings_manager import load_settings

class FilesPage(ctk.CTkFrame):
    def __init__(self, master, switch_page_callback):
        super().__init__(master)
        self.switch_page_callback = switch_page_callback

        self.pdf_files = []
        self.file_buttons = []
        self.selected_files = set()
        self.preview_images = []

        # Layout Config
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # File List Frame
        self.file_list_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.file_list_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        # Button Panel
        self.button_panel = ctk.CTkFrame(self, corner_radius=10)
        self.button_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

        # Add Files Button
        self.add_button = ctk.CTkButton(self.button_panel, text="Add PDF Files", width=200, height=50, corner_radius=8, command=self.add_files)
        self.add_button.pack(pady=(20, 10), padx=10)

        # Remove Selected Button
        self.remove_button = ctk.CTkButton(self.button_panel, text="Remove", width=200, height=50, corner_radius=8, state="disabled", command=self.remove_selected)
        self.remove_button.pack(pady=(0, 10), padx=10)

        # Preview Selected Button
        self.preview_button = ctk.CTkButton(self.button_panel, text="Preview", width=200, height=50, corner_radius=8, state="disabled", command=self.preview_selected)
        self.preview_button.pack(pady=(0, 10), padx=10)

        # Clear All Button
        self.clear_button = ctk.CTkButton(self.button_panel, text="Clear All", width=200, height=50, corner_radius=8, state="disabled", command=self.clear_all_files)
        self.clear_button.pack(pady=(0, 10), padx=10)

        # Merge PDFs Button
        self.merge_button = ctk.CTkButton(self.button_panel, text=" > Merge <", width=200, height=50, corner_radius=8, command=self.merge_pdfs)
        self.merge_button.pack(side="bottom", pady=(20, 20), padx=10)

        # Preview Window
        self.preview_window = None

        # Initial Button States
        self.update_button_states()

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self._add_file_button(file)
        self.update_button_states()

    def _add_file_button(self, file_path):
        file_name = os.path.basename(file_path)
        file_button = ctk.CTkButton(self.file_list_frame, text=file_name, width=600, height=50, anchor="w", fg_color="#2a2d2e", corner_radius=8, command=lambda f=file_path: self.toggle_selection(f))
        file_button.pack(pady=5, padx=10, fill="x")
        self.file_buttons.append((file_path, file_button))

    def toggle_selection(self, file_path):
        for path, button in self.file_buttons:
            if path == file_path:
                if file_path in self.selected_files:
                    self.selected_files.remove(file_path)
                    button.configure(fg_color="#2a2d2e")
                else:
                    self.selected_files.add(file_path)
                    button.configure(fg_color="#445760")
        self.update_button_states()

    def update_button_states(self):
        state = "normal" if self.selected_files else "disabled"
        self.remove_button.configure(state=state)
        self.preview_button.configure(state="normal" if len(self.selected_files) == 1 else "disabled")
        self.clear_button.configure(state="normal" if self.pdf_files else "disabled")

    def remove_selected(self):
        for file in list(self.selected_files):
            if file in self.pdf_files:
                idx = self.pdf_files.index(file)
                self.pdf_files.remove(file)
                self.file_buttons[idx][1].destroy()
                del self.file_buttons[idx]
                self.selected_files.remove(file)
        self.update_button_states()

    def preview_selected(self):
        if not self.selected_files:
            messagebox.showinfo("No Selection", "No files selected for preview.")
            return

        selected_file = list(self.selected_files)[0]

        # Load settings to apply page size
        settings = load_settings()
        page_size = settings.get("preview_page_size", "medium")

        # Define size scaling
        size_scale = {"small": 0.5, "medium": 0.75, "large": 1.0}
        scale_factor = size_scale.get(page_size, 0.75)

        # Open Preview Window
        self.preview_window = ctk.CTkToplevel(self)
        self.preview_window.title("PDF Preview")
        self.preview_window.geometry("600x800")

        preview_frame = ctk.CTkScrollableFrame(self.preview_window)
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Convert PDF to Images
        self.preview_images = convert_from_path(selected_file)
        for img in self.preview_images:
            # Apply scaling from settings
            new_width = int(550 * scale_factor)
            new_height = int(new_width * img.height / img.width)
            img = img.resize((new_width, new_height))

            img_tk = ImageTk.PhotoImage(img)
            label = ctk.CTkLabel(preview_frame, image=img_tk, text="")
            label.image = img_tk
            label.pack(pady=10)

    def refresh_file_list(self):
        """Refreshes the file list UI after merging or modifying files."""
        for _, button in self.file_buttons:
            button.destroy()
        self.file_buttons.clear()
        for file_path in self.pdf_files:
            self._add_file_button(file_path)
        self.update_button_states()

    def merge_pdfs(self):
        if len(self.selected_files) < 2:
            messagebox.showwarning("Not Enough Files", "Please select at least two PDF files to merge.")
            return

        # Load the default save path from settings
        settings = load_settings()
        default_save_path = settings.get("default_save_path", os.path.expanduser("~/Documents"))

        # Suggest default filename and path
        suggested_filename = os.path.join(default_save_path, "merged.pdf")

        # Save file dialog with default path
        output_file = filedialog.asksaveasfilename(
            initialdir=default_save_path,
            initialfile="merged.pdf",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if not output_file:
            return

        merger = PdfMerger()
        try:
            for pdf in self.selected_files:
                merger.append(pdf)
            merger.write(output_file)
            merger.close()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while merging PDFs:\n{e}")

        finally:
            self.selected_files.clear()
            self.refresh_file_list()
            self.switch_page_callback("result", output_file)

    def clear_all_files(self):
        if messagebox.askyesno("Clear All Files", "Are you sure you want to remove all files?"):
            for _, button in self.file_buttons:
                button.destroy()
            self.pdf_files.clear()
            self.file_buttons.clear()
            self.selected_files.clear()
            self.update_button_states()
