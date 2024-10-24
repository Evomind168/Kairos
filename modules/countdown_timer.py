import customtkinter as ctk

class CountdownTimer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()
        self.time_left = 0
        self.is_running = False
        self.is_paused = False
        self.update_timer()

    def setup_ui(self):
        self.label = ctk.CTkLabel(self, text="00:00:00", font=("Arial", 40))
        self.label.pack(pady=20)

        self.entry = ctk.CTkEntry(self, placeholder_text="Час (секунди)")
        self.entry.pack(pady=10)

        self.start_button = ctk.CTkButton(self, text="Старт", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.pause_button = ctk.CTkButton(self, text="Пауза", command=self.pause_timer)
        self.pause_button.pack(pady=5)

        self.reset_button = ctk.CTkButton(self, text="Скидання", command=self.reset_timer)
        self.reset_button.pack(pady=5)

    def start_timer(self):
        if not self.is_running:
            try:
                if not self.is_paused:
                    self.time_left = int(float(self.entry.get()) * 100)
                self.is_running = True
                self.is_paused = False
                self.entry.delete(0, 'end')
            except ValueError:
                self.label.configure(text="Невірний ввід")

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            self.is_paused = True

    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.time_left = 0
        self.label.configure(text="00:00:00")

    def update_timer(self):
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            minutes, seconds = divmod(self.time_left // 100, 60)
            centiseconds = self.time_left % 100
            self.label.configure(text=f"{minutes:02}:{seconds:02}:{centiseconds:02}")
        elif self.time_left == 0 and self.is_running:
            self.is_running = False
            self.label.configure(text="Час вийшов!")

        self.after(10, self.update_timer)
