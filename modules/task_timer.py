import customtkinter as ctk
import sqlite3
from datetime import datetime

class TaskTimer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.time_elapsed = 0
        self.is_running = False
        self.tasks = []
        self.db_init()
        self.load_tasks()
        self.setup_ui()
        self.update_timer()

    def setup_ui(self):
        self.label = ctk.CTkLabel(self, text="00:00:00", font=("Arial", 40))
        self.label.pack(pady=20)

        self.task_entry = ctk.CTkEntry(self, placeholder_text="Назва задачі")
        self.task_entry.pack(pady=10)

        self.start_button = ctk.CTkButton(self, text="Розпочати задачу", command=self.start_task)
        self.start_button.pack(pady=5)

        self.stop_button = ctk.CTkButton(self, text="Завершити задачу", command=self.stop_task)
        self.stop_button.pack(pady=5)

        self.tasks_label = ctk.CTkLabel(self, text="Список задач:", font=("Arial", 16))
        self.tasks_label.pack(pady=(20, 10))

        self.tasks_frame = ctk.CTkScrollableFrame(self, width=300, height=150)
        self.tasks_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.update_task_list()

    def db_init(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         duration TEXT NOT NULL,
         date TEXT NOT NULL)
        ''')
        self.conn.commit()

    def load_tasks(self):
        self.cursor.execute('SELECT name, duration, date FROM tasks ORDER BY id DESC')
        rows = self.cursor.fetchall()
        self.tasks = [f"{task[0]}: {task[1]} ({task[2]})" for task in rows]

    def start_task(self):
        if not self.is_running:
            self.is_running = True
            self.current_task = self.task_entry.get()
            self.task_entry.delete(0, 'end')

    def stop_task(self):
        if self.is_running:
            self.is_running = False
            task_time = self.format_time(self.time_elapsed)
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.tasks.insert(0, f"{self.current_task}: {task_time} ({current_date})")

            self.cursor.execute('INSERT INTO tasks (name, duration, date) VALUES (?, ?, ?)',
                                (self.current_task, task_time, current_date))
            self.conn.commit()

            self.update_task_list()
            self.time_elapsed = 0
            self.label.configure(text="00:00:00")

    def update_timer(self):
        if self.is_running:
            self.time_elapsed += 1
            self.label.configure(text=self.format_time(self.time_elapsed))
        self.after(10, self.update_timer)

    def format_time(self, time):
        minutes, remainder = divmod(time // 100, 60)
        seconds, centiseconds = divmod(remainder, 100)
        return f"{minutes:02}:{seconds:02}:{centiseconds:02}"

    def update_task_list(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        for i, task in enumerate(self.tasks, 1):
            task_label = ctk.CTkLabel(self.tasks_frame, text=f"{i}. {task}", anchor="w", justify="left")
            task_label.pack(pady=2, padx=5, fill="x")