import customtkinter as ctk
from modules.countdown_timer import CountdownTimer
from modules.task_timer import TaskTimer
from modules.pomodoro_timer import PomodoroTimer
from modules.settings_tab import SettingsTab

class TimerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Project Kairos")
        self.geometry("650x600")
        self.setup_ui()

    def setup_ui(self):
        self.settings = SettingsTab(self).load_settings()

        ctk.set_appearance_mode(self.settings["appearance_mode"])
        ctk.set_default_color_theme(self.settings["color_theme"])

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, expand=True, fill="both")

        self.countdown_tab = self.tabview.add("Зворотній відлік")
        self.task_tab = self.tabview.add("Таймер задач")
        self.pomodoro_tab = self.tabview.add("Pomodoro")  # New tab
        self.settings_tab = self.tabview.add("Налаштування")

        self.countdown_timer = CountdownTimer(self.countdown_tab)
        self.countdown_timer.pack(expand=True, fill="both")

        self.task_timer = TaskTimer(self.task_tab)
        self.task_timer.pack(expand=True, fill="both")

        self.pomodoro_timer = PomodoroTimer(self.pomodoro_tab)  # New timer
        self.pomodoro_timer.pack(expand=True, fill="both")

        self.settings = SettingsTab(self.settings_tab)
        self.settings.pack(expand=True, fill="both")

    def on_closing(self):
        self.task_timer.conn.close()
        self.destroy()

if __name__ == "__main__":
    app = TimerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
