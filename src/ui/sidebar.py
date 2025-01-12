import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, switch_page_callback):
        super().__init__(master, width=60, corner_radius=0)
        self.switch_page_callback = switch_page_callback

        # Logo Button (Styled)
        self.logo_button = ctk.CTkButton(
            self,
            text="PyPDF",               # App name
            corner_radius=10,           # Softer corners
            fg_color="#445760",         # Slightly different color for distinction
            hover_color="#556670",      # Subtle hover effect
            text_color="white",         # White text for contrast
            font=("Arial", 20, "bold"), # Larger bold font
            height=60,                  # Taller for emphasis
            state="disabled"            # Disabled to prevent clicks
        )
        self.logo_button.pack(pady=(20, 15), padx=10)

        # Files Page Button
        self.files_button = ctk.CTkButton(
            self,
            text="Files",
            corner_radius=8,
            command=lambda: self.switch_page_callback("files")
        )
        self.files_button.pack(pady=5, padx=5)

        # Settings Page Button
        self.settings_button = ctk.CTkButton(
            self,
            text="Settings",
            corner_radius=8,
            command=lambda: self.switch_page_callback("settings")
        )
        self.settings_button.pack(pady=5, padx=5)
