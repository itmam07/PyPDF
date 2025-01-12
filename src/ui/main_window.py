import customtkinter as ctk
from ui.sidebar import Sidebar
from ui.pages.files_page import FilesPage
from ui.pages.settings_page import SettingsPage
from ui.pages.result_page import ResultPage

class MainWindow:
    def __init__(self, root):
        self.root = root

        # Main layout frames
        self.sidebar = Sidebar(self.root, self.switch_page)
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.content_frame.pack(side="top", fill="both", expand=True)


        # Initialize pages
        self.pages = {
            "files": FilesPage(self.content_frame, self.switch_page),
            "settings": SettingsPage(self.content_frame),
            "result": ResultPage(self.content_frame)
        }

        self.active_page = None
        self.switch_page("files")  # Default to Files Page

    def switch_page(self, page_name, file_path=None):
        if self.active_page:
            self.active_page.pack_forget()

        self.active_page = self.pages[page_name]
        self.active_page.pack(fill="both", expand=True)

        # Load PDF dynamically if switching to the Result Page
        if page_name == "result" and file_path:
            self.pages["result"].load_pdf(file_path)
