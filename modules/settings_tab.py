import customtkinter as ctk
import json

class SettingsTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.settings = self.load_settings()
        self.setup_ui()

    def setup_ui(self):
        self.label = ctk.CTkLabel(self, text="Налаштування", font=("Arial", 20))
        self.label.pack(pady=20)

        self.appearance_mode_label = ctk.CTkLabel(self, text="Тема додатку:")
        self.appearance_mode_label.pack(pady=10)

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.pack(pady=10)
        self.appearance_mode_optionemenu.set(self.settings.get("appearance_mode", "System"))

        self.color_theme_label = ctk.CTkLabel(self, text="Кольорова схема:")
        self.color_theme_label.pack(pady=10)

        self.color_theme_optionemenu = ctk.CTkOptionMenu(
            self,
            values=["blue", "green", "dark-blue"],
            command=self.change_color_theme_event
        )
        self.color_theme_optionemenu.pack(pady=10)
        self.color_theme_optionemenu.set(self.settings.get("color_theme", "green"))

        self.save_button = ctk.CTkButton(self, text="Зберегти налаштування", command=self.save_settings)
        self.save_button.pack(pady=20)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        self.settings["appearance_mode"] = new_appearance_mode

    def change_color_theme_event(self, new_color_theme: str):
        ctk.set_default_color_theme(new_color_theme)
        self.settings["color_theme"] = new_color_theme

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "appearance_mode": "System",
                "color_theme": "green"
            }

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)
        print("Налаштування збережено")
