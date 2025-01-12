import customtkinter as ctk
from tkinter import filedialog
from settings_manager import load_settings, save_settings

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Load existing settings
        self.settings = load_settings()

        # Layout Config
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Settings", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Appearance Mode
        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:")
        self.appearance_mode_label.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        
        self.appearance_mode_var = ctk.StringVar(value=self.settings["appearance_mode"])
        self.light_mode_button = ctk.CTkRadioButton(self, text="Light Mode", variable=self.appearance_mode_var, value="light", command=self.change_appearance_mode)
        self.dark_mode_button = ctk.CTkRadioButton(self, text="Dark Mode", variable=self.appearance_mode_var, value="dark", command=self.change_appearance_mode)
        
        self.light_mode_button.grid(row=1, column=1, pady=5, padx=10)
        self.dark_mode_button.grid(row=2, column=1, pady=5, padx=10)

        # Preview Page Size
        self.page_size_label = ctk.CTkLabel(self, text="Preview Page Size:")
        self.page_size_label.grid(row=3, column=0, pady=5, padx=10, sticky="w")
        
        self.page_size_var = ctk.StringVar(value=self.settings["preview_page_size"])
        self.small_page_button = ctk.CTkRadioButton(self, text="Small", variable=self.page_size_var, value="small", command=self.change_page_size)
        self.medium_page_button = ctk.CTkRadioButton(self, text="Medium", variable=self.page_size_var, value="medium", command=self.change_page_size)
        self.large_page_button = ctk.CTkRadioButton(self, text="Large", variable=self.page_size_var, value="large", command=self.change_page_size)
        
        self.small_page_button.grid(row=3, column=1, pady=5, padx=10)
        self.medium_page_button.grid(row=4, column=1, pady=5, padx=10)
        self.large_page_button.grid(row=5, column=1, pady=5, padx=10)

        # Default Save Path
        self.default_path_label = ctk.CTkLabel(self, text="Default Save Path:")
        self.default_path_label.grid(row=6, column=0, pady=5, padx=10, sticky="w")
        
        self.path_button = ctk.CTkButton(self, text="Choose Path", command=self.set_default_path)
        self.path_button.grid(row=6, column=1, pady=5, padx=10)

        # Show current path
        self.path_display = ctk.CTkLabel(self, text=self.settings["default_save_path"] or "No path selected", wraplength=250)
        self.path_display.grid(row=7, column=0, columnspan=2, pady=5)

    def change_appearance_mode(self):
        mode = self.appearance_mode_var.get()
        ctk.set_appearance_mode(mode)
        self.settings["appearance_mode"] = mode
        save_settings(self.settings)

    def change_page_size(self):
        size = self.page_size_var.get()
        self.settings["preview_page_size"] = size
        save_settings(self.settings)

    def set_default_path(self):
        folder = filedialog.askdirectory()
        if folder:
            self.settings["default_save_path"] = folder
            self.path_display.configure(text=folder)
            save_settings(self.settings)
