import customtkinter as ctk
from ui.main_window import MainWindow
from settings_manager import load_settings

def main():
    # Load user settings
    settings = load_settings()

    # Apply appearance mode from settings
    ctk.set_appearance_mode(settings.get("appearance_mode", "Dark"))
    ctk.set_default_color_theme("dark-blue")


    app = ctk.CTk()
    app.title("PDF Merger")
    app.geometry("1000x600")
    
    MainWindow(app)
    app.mainloop()

if __name__ == "__main__":
    main()
