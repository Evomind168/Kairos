import customtkinter as ctk

class PomodoroTimer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pomodoro_length = 25 * 60  # 25 minutes by default
        self.short_break_length = 5 * 60  # 5 minutes by default
        self.long_break_length = 15 * 60  # 15 minutes by default
        self.pomodoros_completed = 0
        self.current_timer = self.pomodoro_length
        self.is_running = False
        self.setup_ui()
        self.update_timer()

    def setup_ui(self):
        self.label = ctk.CTkLabel(self, text="25:00", font=("Arial", 40))
        self.label.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Готові почати Pomodoro?", font=("Arial", 16))
        self.status_label.pack(pady=10)

        # Time settings frame
        self.time_settings_frame = ctk.CTkFrame(self)
        self.time_settings_frame.pack(pady=10)

        # Pomodoro time setting
        self.pomodoro_time_frame = ctk.CTkFrame(self.time_settings_frame)
        self.pomodoro_time_frame.pack(pady=5)

        self.pomodoro_time_label = ctk.CTkLabel(self.pomodoro_time_frame, text="Час роботи (хв):")
        self.pomodoro_time_label.pack(side="left", padx=5)

        self.pomodoro_time_entry = ctk.CTkEntry(self.pomodoro_time_frame, width=50)
        self.pomodoro_time_entry.insert(0, "25")
        self.pomodoro_time_entry.pack(side="left", padx=5)

        # Short break time setting
        self.short_break_frame = ctk.CTkFrame(self.time_settings_frame)
        self.short_break_frame.pack(pady=5)

        self.short_break_label = ctk.CTkLabel(self.short_break_frame, text="Коротка перерва (хв):")
        self.short_break_label.pack(side="left", padx=5)

        self.short_break_entry = ctk.CTkEntry(self.short_break_frame, width=50)
        self.short_break_entry.insert(0, "5")
        self.short_break_entry.pack(side="left", padx=5)

        # Long break time setting
        self.long_break_frame = ctk.CTkFrame(self.time_settings_frame)
        self.long_break_frame.pack(pady=5)

        self.long_break_label = ctk.CTkLabel(self.long_break_frame, text="Довга перерва (хв):")
        self.long_break_label.pack(side="left", padx=5)

        self.long_break_entry = ctk.CTkEntry(self.long_break_frame, width=50)
        self.long_break_entry.insert(0, "15")
        self.long_break_entry.pack(side="left", padx=5)

        # Set time button
        self.set_time_button = ctk.CTkButton(self.time_settings_frame, text="Встановити час",
                                             command=self.set_pomodoro_times)
        self.set_time_button.pack(pady=10)

        # Control buttons frame
        self.control_buttons_frame = ctk.CTkFrame(self)
        self.control_buttons_frame.pack(pady=10)

        self.start_button = ctk.CTkButton(self.control_buttons_frame, text="Старт", command=self.start_timer)
        self.start_button.pack(side="bottom", padx=5, pady=7)

        self.stop_button = ctk.CTkButton(self.control_buttons_frame, text="Стоп", command=self.stop_timer)
        self.stop_button.pack(side="bottom", padx=5, pady=7)

        self.reset_button = ctk.CTkButton(self.control_buttons_frame, text="Скинути", command=self.reset_pomodoro)
        self.reset_button.pack(side="bottom", padx=5, pady=7)

        self.pomodoro_count_label = ctk.CTkLabel(self, text="Завершені Pomodoro: 0", font=("Arial", 14))
        self.pomodoro_count_label.pack(pady=10)

    def set_pomodoro_times(self):
        try:
            new_pomodoro_time = int(self.pomodoro_time_entry.get())
            new_short_break = int(self.short_break_entry.get())
            new_long_break = int(self.long_break_entry.get())

            if new_pomodoro_time > 0 and new_short_break > 0 and new_long_break > 0:
                self.pomodoro_length = new_pomodoro_time * 60
                self.short_break_length = new_short_break * 60
                self.long_break_length = new_long_break * 60
                self.current_timer = self.pomodoro_length
                minutes, seconds = divmod(self.current_timer, 60)
                self.label.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.status_label.configure(text=f"Час встановлено: Робота - {new_pomodoro_time} хв, "
                                                 f"Коротка перерва - {new_short_break} хв, "
                                                 f"Довга перерва - {new_long_break} хв")
            else:
                self.status_label.configure(text="Будь ласка, введіть додатні числа для всіх значень")
        except ValueError:
            self.status_label.configure(text="Будь ласка, введіть коректні числа для всіх значень")

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.status_label.configure(text="Pomodoro в процесі")
            self.set_time_button.configure(state="disabled")
            self.reset_button.configure(state="disabled")

    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.status_label.configure(text="Pomodoro зупинено")
            self.set_time_button.configure(state="normal")
            self.reset_button.configure(state="normal")

    def reset_pomodoro(self):
        self.is_running = False
        self.pomodoros_completed = 0
        self.current_timer = self.pomodoro_length
        minutes, seconds = divmod(self.current_timer, 60)
        self.label.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.status_label.configure(text="Готові почати Pomodoro?")
        self.pomodoro_count_label.configure(text="Завершені Pomodoro: 0")
        self.set_time_button.configure(state="normal")

    def update_timer(self):
        if self.is_running and self.current_timer > 0:
            self.current_timer -= 1
            minutes, seconds = divmod(self.current_timer, 60)
            self.label.configure(text=f"{minutes:02d}:{seconds:02d}")
        elif self.current_timer == 0:
            self.is_running = False
            self.set_time_button.configure(state="normal")
            self.reset_button.configure(state="normal")
            if self.status_label.cget("text") == "Pomodoro в процесі":
                self.pomodoros_completed += 1
                self.pomodoro_count_label.configure(text=f"Завершені Pomodoro: {self.pomodoros_completed}")

                if self.pomodoros_completed % 4 == 0:
                    self.current_timer = self.long_break_length
                    self.status_label.configure(text="Довга перерва")
                else:
                    self.current_timer = self.short_break_length
                    self.status_label.configure(text="Коротка перерва")
            else:
                self.current_timer = self.pomodoro_length
                self.status_label.configure(text="Готові почати Pomodoro?")

        self.after(1000, self.update_timer)
